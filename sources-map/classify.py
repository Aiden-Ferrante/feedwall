"""Map feedwall's FreshRSS feeds onto the 9-subject tree + tier facet."""
import html, json, subprocess

SUBJECTS = ["economy","markets","politics","geopolitics","technology",
            "science","society","energy","business"]

CAT_DEFAULT = {
 "AI/ML — Blogs & Newsletters":                  ("technology","ai","analysis"),
 "Code & Launches":                              ("technology","software","discussion"),
 "Discovered — AI-lab official blogs":           ("technology","ai","primary"),
 "Discovered — AI/ML & systems podcasts":        ("technology","ai","analysis"),
 "Discovered — GPU/systems practitioners":       ("technology","infrastructure","analysis"),
 "Discovered — builders in public":              ("technology","software","analysis"),
 "Discovered — econ analysis & commentary":      ("economy","commentary","analysis"),
 "Discovered — forums & communities":            ("technology","ai","discussion"),
 "Discovered — individual AI/ML researchers":    ("technology","ai","analysis"),
 "Discovered — local-LLM practitioners & guides":("technology","ai","analysis"),
 "Discovered — local-LLM releases & tooling":    ("technology","software","primary"),
 "Discovered — macro & econ data":               ("economy","indicators","primary"),
 "Discovered — markets/quant primary sources":   ("markets","research","analysis"),
 "Discovered — publications/journals":           ("technology","general","analysis"),
 "Markets & Econ":                               ("markets","news","wire"),
 "Papers":                                       ("science","papers","primary"),
 "Releases":                                     ("technology","software","primary"),
 "Stats & Causal":                               ("science","methods","analysis"),
 "Tech News":                                    ("technology","general","wire"),
 "Uncategorized":                                ("technology","software","primary"),
 "Video":                                        ("technology","ai","analysis"),
}

# name-substring -> override. Applied in order; first match wins.
OVERRIDE = [
 ("Show HN",                  ("business","startups","discussion")),
 ("Paul Graham",              ("business","startups","analysis")),
 ("Pieter Levels",            ("business","startups","analysis")),
 ("A Smart Bear",             ("business","startups","analysis")),
 ("Startups for the Rest",    ("business","startups","analysis")),
 ("Ben Kuhn",                 ("business","startups","analysis")),
 ("Fly.io",                   ("technology","software","primary")),
 ("Oxide Computer",           ("technology","software","primary")),
 ("Supabase",                 ("technology","software","primary")),
 ("Tailscale",                ("technology","software","primary")),
 ("Zed —",                    ("technology","software","primary")),
 ("Cloudflare",               ("technology","infrastructure","primary")),
 ("Meta — Engineering",       ("technology","infrastructure","primary")),
 ("PyTorch — Blog",           ("technology","ai","primary")),
 ("GPU MODE",                 ("technology","infrastructure","analysis")),
 ("Lobsters",                 ("technology","software","discussion")),
 ("The Changelog",            ("technology","software","analysis")),
 ("Oxide and Friends",        ("technology","software","analysis")),
 ("ACM Queue",                ("technology","software","analysis")),
 ("IEEE Spectrum",            ("technology","general","analysis")),
 ("MIT Technology Review",    ("technology","general","analysis")),
 ("JMLR",                     ("science","papers","primary")),
 ("Nature Machine",           ("science","papers","primary")),
 ("Quanta",                   ("science","discoveries","analysis")),
 ("3Blue1Brown",              ("science","methods","analysis")),
 ("arXiv q-fin",              ("science","papers","primary")),
 ("SEC — Press Releases",     ("politics","regulation","primary")),
 ("Federal Reserve — Press",  ("economy","central-bank","primary")),
 ("ECB —",                    ("economy","central-bank","primary")),
 ("Fed — FEDS Notes",         ("economy","central-bank","primary")),
 ("Liberty Street",           ("economy","central-bank","analysis")),
 ("Bank Underground",         ("economy","central-bank","analysis")),
 ("Atlanta Fed",              ("economy","central-bank","analysis")),
 ("FRED Blog",                ("economy","indicators","analysis")),
 ("Calculated Risk",          ("economy","indicators","analysis")),
 ("Econbrowser",              ("economy","indicators","analysis")),
 ("Apricitas",                ("economy","indicators","analysis")),
 ("Employ America",           ("economy","labor","analysis")),
 ("BEA —",                    ("economy","indicators","primary")),
 ("Census —",                 ("economy","indicators","primary")),
 ("CBO —",                    ("economy","fiscal","primary")),
 ("Marginal Revolution",      ("economy","commentary","analysis")),
 ("Investing.com",            ("markets","news","wire")),
 ("MarketWatch",              ("markets","news","wire")),
 ("Klement",                  ("markets","research","analysis")),
]

rows = json.loads(subprocess.run(["docker","exec","feedwall","php","-r","""
$db=new PDO("sqlite:/var/www/FreshRSS/data/users/mooteo/db.sqlite");
$o=[]; foreach($db->query("select c.name cat, f.name, f.url, f.cache_nbEntries n,
 f.error, f.lastUpdate from feed f join category c on c.id=f.category") as $r)
 $o[]=["cat"=>$r["cat"],"name"=>$r["name"],"url"=>$r["url"],
       "n"=>(int)$r["n"],"error"=>(int)$r["error"],"last"=>(int)$r["lastUpdate"]];
echo json_encode($o);"""], capture_output=True, text=True).stdout)

for r in rows:
    r["cat"]=html.unescape(r["cat"]); r["name"]=html.unescape(r["name"])

feeds=[]
for r in rows:
    sub = None
    for frag, trip in OVERRIDE:
        if frag in r["name"]: sub = trip; break
    if sub is None:
        sub = CAT_DEFAULT.get(r["cat"])
        if sub is None: raise SystemExit(f"unmapped category: {r['cat']}")
    feeds.append({"name":r["name"], "url":r["url"], "entries":r["n"],
                  "broken": r["error"]>0 or r["last"]==0,
                  "cat":r["cat"], "subject":sub[0], "group":sub[1], "tier":sub[2]})

assert len(feeds)==143, len(feeds)

tree={s:{} for s in SUBJECTS}
for f in feeds: tree[f["subject"]].setdefault(f["group"],[]).append(f)

out={"total":len(feeds),
     "subjects":[{"id":s,
        "count":sum(len(v) for v in tree[s].values()),
        "groups":[{"id":g,"count":len(v),
                   "feeds":sorted(v,key=lambda x:-x["entries"])}
                  for g,v in sorted(tree[s].items(), key=lambda kv:-len(kv[1]))]}
       for s in SUBJECTS]}
json.dump(out, open("sources.json","w"), indent=1)

print(f"{out['total']} feeds mapped\n")
for s in out["subjects"]:
    bar = "#"*round(s["count"]/2)
    print(f"  {s['id']:<12} {s['count']:>3}  {bar}")
    for g in s["groups"]: print(f"       {g['id']:<16} {g['count']:>3}")
tiers={}
for f in feeds: tiers[f["tier"]]=tiers.get(f["tier"],0)+1
print("\n  tier mix:", tiers)
