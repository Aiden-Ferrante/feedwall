#!/usr/bin/env python3
"""feedwall wall — read-only dashboard over brain-data/curated.sqlite.

Zero-dependency stdlib server (same idiom as vaultwriter/video-dashboard).
    python3 dashboard/server.py [--port 8975] [--host 0.0.0.0]

    GET /            HTML wall (top-5 + lane columns, auto-refreshes)
    GET /api/wall    {"top": [...], "lanes": {lane: [...]}, "scored": n}
    GET /health      {"status": "ok", "items": n}
"""
import argparse
import json
import os
import sys
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from brain import config, db  # noqa: E402

LANE_LABELS = {
    "papers": "Papers", "benchmarks": "Benchmarks", "ai-ml": "AI/ML",
    "systems": "Systems/GPU",
    "markets": "Markets", "causal-stats": "Causal & Stats",
    "data-eng": "Data Eng", "tech": "Tech", "other": "Other",
}


def wall_data(hours: int) -> dict:
    con = db.connect()
    since = int(time.time()) - hours * 3600
    row = lambda r: {  # noqa: E731
        "title": r["title"], "url": r["url"], "tldr": r["tldr"],
        "score": r["score"], "lane": r["lane"], "feed": r["feed"],
        "published": r["published"],
    }
    # papers stay in their own column; the top strip is for news
    top = [row(r) for r in db.top_since(con, since, 25)
           if r["score"] >= 5.0 and r["lane"] != "papers"][:5]
    lanes = {}
    for lane in config.LANES:
        rows = con.execute(
            "SELECT * FROM items WHERE lane=? AND MAX(published, scored_at)>=? "
            "ORDER BY score DESC, published DESC LIMIT 8", (lane, since)
        ).fetchall()
        lanes[lane] = [row(r) for r in rows]
    scored = con.execute(
        "SELECT COUNT(*) c FROM items WHERE scored_at >= ?", (since,)
    ).fetchone()["c"]
    con.close()
    return {"top": top, "lanes": lanes, "scored": scored,
            "labels": LANE_LABELS, "hours": hours}



# The fleet's shared tokens and header chrome, inlined at startup. A sibling
# directory is not a guarantee, so a missing file costs the palette and nothing
# else — an admin page that will not render because a stylesheet moved is worse
# than one that renders in its own colours.
FLEET_CSS_PATH = Path(
    os.environ.get("FLEET_UI_CSS", Path.home() / "Desktop/code/fleet-ui/fleet.css"))
try:
    FLEET_CSS = FLEET_CSS_PATH.read_text(encoding="utf-8")
except OSError:
    FLEET_CSS = ""

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>feedwall</title><style>/*FLEET*/
:root{--bg:var(--fleet-bg);--panel:var(--fleet-surface);
--border:var(--fleet-border);--fg:var(--fleet-text);
--muted:var(--fleet-text-faint);--accent:var(--fleet-accent);}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);
font-family:-apple-system,'Segoe UI',Roboto,sans-serif;
font-size:var(--fleet-text-body);line-height:1.5}
main{padding:24px;max-width:72rem;margin:0 auto}
h1{margin:0 0 4px}h1 span{color:var(--accent)}
.sub{color:var(--muted);font-size:var(--fleet-text-meta);margin-bottom:20px}
.top{display:flex;flex-direction:column;gap:10px;margin-bottom:28px}
.card{background:var(--panel);border:1px solid var(--border);border-radius:8px;
padding:12px 16px}
.card a{color:var(--fg);text-decoration:none;font-weight:600}
.card a:hover{color:var(--accent)}
.tldr{color:var(--muted);font-size:var(--fleet-text-meta);margin-top:4px}
.meta{font-size:var(--fleet-text-meta);color:var(--muted);margin-top:6px}
.badge{display:inline-block;background:color-mix(in srgb, var(--accent) 20%, transparent);color:var(--accent);font-family:var(--fleet-font-mono);
border-radius:10px;padding:0 8px;font-weight:700;margin-right:8px}
.lanes{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.lane{background:var(--panel);border:1px solid var(--border);border-radius:8px;
padding:12px}
.lane h2{font-size:var(--fleet-text-title);margin:0 0 8px;color:var(--accent)}
.lane ul{list-style:none;margin:0;padding:0}
.lane li{padding:6px 0;border-top:1px solid var(--border);font-size:var(--fleet-text-meta)}
.lane li:first-child{border-top:0}
.lane a{color:var(--fg);text-decoration:none}.lane a:hover{color:var(--accent)}
.s{color:var(--muted);font-size:var(--fleet-text-micro);font-family:var(--fleet-font-mono);margin-right:6px}
.quiet{color:var(--muted);font-style:italic;font-size:var(--fleet-text-meta)}
</style></head><body>
<header class="fleet-header"><div class="fleet-header-inner">
  <nav class="fleet-apps" aria-label="Fleet" id="fleetnav"><p class="fleet-wordmark">fleet</p></nav>
  <div class="fleet-sections">
    <h1 class="fleet-brand">feed<span>wall</span></h1>
    <div class="fleet-actions"><p class="fleet-sub" id="sub">loading…</p></div>
  </div>
</div></header>
<main>
<div class="top" id="top"></div>
<div class="lanes" id="lanes"></div>
</main>
<script>
/* Tier one, built client-side because this page is one static string. Ports are
   resolved against whoever is reading — feedwall binds 0.0.0.0 and gets opened
   over the tailnet, where a literal localhost points at the reading machine.
   Keep in step with code/fleet-ui/apps.js; PLATFORM.md Wave 3 retires the copy. */
const FLEET_APPS = [
  ['shipyard','Shipyard',8845],['mission-control','Control',9090],
  ['vault-dashboard','Vault',8989],['learnhub','Learn',3001],
  ['feedwall','Feed',8975],
];
(() => {
  const nav = document.getElementById('fleetnav');
  for (const [id, label, port] of FLEET_APPS) {
    if (id === 'feedwall') {
      const cur = document.createElement('span');
      cur.className = 'fleet-app'; cur.setAttribute('aria-current','page');
      cur.textContent = label; nav.appendChild(cur);
    } else {
      const a = document.createElement('a');
      a.className = 'fleet-app';
      a.href = `${location.protocol}//${location.hostname}:${port}`;
      a.textContent = label; nav.appendChild(a);
    }
  }
})();
async function load(){
  const d = await (await fetch('/api/wall')).json();
  document.getElementById('sub').textContent =
    d.scored + ' items scored in the last ' + d.hours + 'h · ' +
    new Date().toLocaleString();
  const top = document.getElementById('top');
  top.innerHTML = d.top.length ? '' : '<div class="quiet">Nothing cleared the bar — quiet window.</div>';
  for (const it of d.top){
    top.insertAdjacentHTML('beforeend',
      `<div class="card"><span class="badge">${it.score.toFixed(0)}</span>
       <a href="${it.url}" target="_blank">${it.title}</a>
       <div class="tldr">${it.tldr}</div>
       <div class="meta">${d.labels[it.lane]||it.lane} · ${it.feed}</div></div>`);
  }
  const lanes = document.getElementById('lanes'); lanes.innerHTML='';
  for (const [lane, items] of Object.entries(d.lanes)){
    const rows = items.length ? items.map(it =>
      `<li><span class="s">${it.score.toFixed(0)}</span>
       <a href="${it.url}" target="_blank">${it.title}</a></li>`).join('')
      : '<li class="quiet">quiet</li>';
    lanes.insertAdjacentHTML('beforeend',
      `<div class="lane"><h2>${d.labels[lane]}</h2><ul>${rows}</ul></div>`);
  }
}
load(); setInterval(load, 5*60*1000);
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *_a):
        pass

    def do_GET(self):
        path = urllib.parse.urlparse(self.path)
        if path.path in ("/", "/index.html"):
            self._send(200, PAGE.replace("/*FLEET*/", FLEET_CSS).encode(),
                       "text/html; charset=utf-8")
        elif path.path == "/api/wall":
            hours = int(dict(urllib.parse.parse_qsl(path.query)).get("hours", 24))
            self._send(200, wall_data(hours))
        elif path.path == "/health":
            con = db.connect()
            row = con.execute(
                "SELECT COUNT(*) c, MAX(scored_at) newest FROM items"
            ).fetchone()
            con.close()
            newest = row["newest"]
            freshness = {}
            if newest:
                freshness["scored"] = time.strftime(
                    "%Y-%m-%dT%H:%M:%S%z", time.localtime(newest)
                )
            # Platform health shape (ok/checks/freshness); items kept for old callers.
            self._send(200, {
                "ok": row["c"] > 0,
                "checks": {"db": True},
                "freshness": freshness,
                "status": "ok",
                "items": row["c"],
            })
        else:
            self._send(404, {"error": "not found"})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default=os.environ.get("FEEDWALL_WALL_HOST", "0.0.0.0"))
    ap.add_argument("--port", type=int,
                    default=int(os.environ.get("FEEDWALL_WALL_PORT", "8975")))
    args = ap.parse_args()
    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"feedwall wall on http://{args.host}:{args.port}", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()


if __name__ == "__main__":
    main()
