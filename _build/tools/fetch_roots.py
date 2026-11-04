"""Fetch each vendor's homepage (host of the landed sales page) into work/sales/<slug>.root.txt."""
import concurrent.futures as cf, io, os, re, sys, urllib.request, urllib.parse
sys.path.insert(0, os.path.dirname(__file__))
from fetch_sales import OUT, UA, text
def get(slug):
    first = io.open(os.path.join(OUT, slug + ".txt"), encoding="utf-8").readline().strip()
    u = urllib.parse.urlsplit(first)
    if "mwebtrackwise" in u.netloc:
        return slug, "tracker", ""
    root = f"{u.scheme}://{u.netloc}/"
    try:
        r = urllib.request.urlopen(urllib.request.Request(root, headers={"User-Agent": UA}), timeout=25)
        t = text(r.read().decode("utf-8", "ignore"))
        io.open(os.path.join(OUT, slug + ".root.txt"), "w", encoding="utf-8").write(r.geturl() + "\n" + t)
        return slug, len(t.split()), r.geturl()[:70]
    except Exception as ex:
        return slug, "ERR", str(ex)[:60]
slugs = sorted(f[:-4] for f in os.listdir(OUT) if f.endswith(".txt") and not f.endswith(".root.txt"))
with cf.ThreadPoolExecutor(6) as ex:
    for r in ex.map(get, slugs):
        print(*r)
