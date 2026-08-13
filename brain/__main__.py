"""CLI: python -m brain run|stats  (run from ~/Desktop/code/feedwall)."""

import argparse
import re
import sys
import time

from . import config, db, freshrss, score, stocklake


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
        if item["id"] in known or not item["title"]:
            continue
        if item["title"].lower().startswith(config.TITLE_SKIP_PREFIXES):
            continue
        if re.match(config.TITLE_SKIP_RE, item["title"].strip()):
            continue
        if re.match(config.URL_SKIP_RE, item["url"]):
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
    starred_ids = 0
    for item in client.starred():
        if item["id"] not in known:
            is_paper = item["category"] == config.PAPERS_CATEGORY
            try:
                verdict = score.score_item(item, papers_prompt if is_paper else system_prompt)
            except Exception:
                verdict = {"lane": "other", "score": 7.0, "tldr": ""}
            if is_paper:
                verdict["lane"] = "papers"
            elif item["category"] == config.BENCHMARKS_CATEGORY:
                verdict["lane"] = "benchmarks"
            db.upsert_item(con, item, verdict["lane"], verdict["score"], verdict["tldr"])
        db.mark_starred(con, item["id"])
        starred_ids += 1

    lake = stocklake.ingest(con)

    db.set_meta(con, "last_run", str(int(time.time())))
    con.commit()
    print(f"run complete: {fetched} fetched, {scored} newly scored, "
          f"{starred_ids} starred synced, {lake} lake signals -> {config.DB_PATH}")


def cmd_stats(args):
    con = db.connect()
    total = con.execute("SELECT COUNT(*) c FROM items").fetchone()["c"]
    print(f"items scored: {total}")
    for row in con.execute(
        "SELECT lane, COUNT(*) c, ROUND(AVG(score),1) avg FROM items "
        "GROUP BY lane ORDER BY c DESC"
    ):
        print(f"  {row['lane']:<12} {row['c']:>5}  avg {row['avg']}")
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
