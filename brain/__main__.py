"""CLI: python -m brain run|stats  (run from the repo root)."""

import argparse
import re
import sys
import time

from . import config, db, freshrss, score, stocklake

FALLBACK_SCORE = 7.0  # stored for a starred item the model failed to score


def skip_reason(item: dict):
    """Deterministic pre-filter: why an item never reaches the scorer, or None.

    Runs before any model call, so feed noise costs nothing and can't be
    mis-scored. Rules live in config (TITLE_SKIP_*, URL_SKIP_RE).
    """
    title = (item.get("title") or "").strip()
    if not title:
        return "no title"
    if title.lower().startswith(config.TITLE_SKIP_PREFIXES):
        return "ci/nightly tag"
    if re.match(config.TITLE_SKIP_RE, title):
        return "build-number release"
    if re.match(config.URL_SKIP_RE, item.get("url") or ""):
        return "translated duplicate"
    return None


def cmd_run(args):
    con = db.connect()
    client = freshrss.Client()

    starred_seen = db.starred_examples(con)
    system_prompt = score.build_system_prompt(starred_seen)
    papers_prompt = score.build_system_prompt(starred_seen, papers=True)

    since = int(time.time()) - args.hours * 3600
    known = db.known_ids(con)

    fetched = scored = papers_scored = 0
    for item in client.unread(newer_than_unix=since, max_items=args.limit * 3):
        fetched += 1
        if item["id"] in known or skip_reason(item):
            continue
        if scored >= args.limit:
            break
        is_paper = item["category"] == config.PAPERS_CATEGORY
        if is_paper and papers_scored >= config.PAPERS_MAX_PER_RUN:
            continue
        try:
            verdict = score.score_item(item, papers_prompt if is_paper else system_prompt)
        except Exception as e:  # one bad item must not kill the run
            print(f"  ! scoring failed for {item['title'][:60]}: {e}", file=sys.stderr)
            continue
        if is_paper:
            verdict["lane"] = "papers"  # papers never leak into news lanes
            papers_scored += 1
        elif item["category"] == config.BENCHMARKS_CATEGORY:
            verdict["lane"] = "benchmarks"  # see config: the hint alone leaks to ai-ml
        db.upsert_item(con, item, verdict["lane"], verdict["score"], verdict["tldr"])
        scored += 1
        if scored % 25 == 0:
            con.commit()
            print(f"  scored {scored}...")

    # sync stars (taste signal)
    starred_ids = fallbacks = 0
    for item in client.starred():
        if item["id"] not in known:
            is_paper = item["category"] == config.PAPERS_CATEGORY
            source = "model"
            try:
                verdict = score.score_item(item, papers_prompt if is_paper else system_prompt)
            except Exception as e:
                # A starred item must still be stored (it is a taste signal),
                # so it gets a default score, labelled as such.
                print(f"  ! scoring failed for starred {item['title'][:60]}: {e}; "
                      f"storing fallback score {FALLBACK_SCORE}", file=sys.stderr)
                verdict = {"lane": "other", "score": FALLBACK_SCORE, "tldr": ""}
                source = "fallback"
                fallbacks += 1
            if is_paper:
                verdict["lane"] = "papers"
            elif item["category"] == config.BENCHMARKS_CATEGORY:
                verdict["lane"] = "benchmarks"
            db.upsert_item(con, item, verdict["lane"], verdict["score"], verdict["tldr"],
                           score_source=source)
        db.mark_starred(con, item["id"])
        starred_ids += 1

    lake = stocklake.ingest(con)

    db.set_meta(con, "last_run", str(int(time.time())))
    con.commit()
    print(f"run complete: {fetched} fetched, {scored} newly scored, "
          f"{starred_ids} starred synced ({fallbacks} fallback scores), "
          f"{lake} lake signals -> {config.DB_PATH}")


def cmd_stats(args):
    con = db.connect()
    total = con.execute("SELECT COUNT(*) c FROM items").fetchone()["c"]
    print(f"items scored: {total}")
    for row in con.execute(
        "SELECT lane, COUNT(*) c, ROUND(AVG(score),1) avg FROM items "
        "GROUP BY lane ORDER BY c DESC"
    ):
        print(f"  {row['lane']:<12} {row['c']:>5}  avg {row['avg']}")
    print("by score source:")
    for row in con.execute(
        "SELECT COALESCE(score_source, 'unknown') src, COUNT(*) c FROM items "
        "GROUP BY src ORDER BY c DESC"
    ):
        print(f"  {row['src']:<12} {row['c']:>5}")
    print("\ntop 10 (last 48h):")
    for r in db.top_since(con, int(time.time()) - 48 * 3600, 10):
        print(f"  [{r['score']:.1f}] ({r['lane']}) {r['title'][:80]}")


def main():
    p = argparse.ArgumentParser(prog="brain")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="fetch unread, score new items, sync stars")
    r.add_argument("--limit", type=int, default=200, help="max new items to score")
    r.add_argument("--hours", type=int, default=48, help="lookback window")
    r.set_defaults(fn=cmd_run)
    s = sub.add_parser("stats", help="show scoring stats")
    s.set_defaults(fn=cmd_stats)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
