"""Fetch every product's official sales page (via its buy link) into _build/work/sales/<slug>.html/.txt."""
import concurrent.futures as cf, html, io, json, os, re, sys, urllib.request
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from build_site import products
OUT = os.path.join(os.path.dirname(__file__), "..", "work", "sales")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"

def text(src):
    src = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", src)
    t = re.sub(r"(?is)<br\s*/?>|</(p|div|h[1-6]|li|tr|td|section|span|button|a)>", "\n", src)
    t = html.unescape(re.sub(r"(?s)<[^>]+>", " ", t))
    out, prev = [], None
    for l in t.splitlines():
        l = re.sub(r"[ \t\u00a0]+", " ", l).strip()
        if l and l != prev:
            out.append(l)
        prev = l
    return "\n".join(out)

def get(p):
    path = os.path.join(OUT, p["slug"])
    if os.path.exists(path + ".txt") and os.path.getsize(path + ".txt") > 500:
        return p["slug"], "cached", ""
    try:
        r = urllib.request.urlopen(urllib.request.Request(p["link"], headers={"User-Agent": UA, "Accept-Language": "en-US"}), timeout=30)
        src = r.read().decode("utf-8", "ignore")
        io.open(path + ".html", "w", encoding="utf-8").write(src)
        t = text(src)
        io.open(path + ".txt", "w", encoding="utf-8").write(r.geturl() + "\n" + t)
        return p["slug"], len(t.split()), r.geturl()[:80]
    except Exception as ex:
        return p["slug"], "ERR", str(ex)[:80]

if __name__ == "__main__":
    ps = products()
    with cf.ThreadPoolExecutor(6) as ex:
        for s, n, u in ex.map(get, ps):
            print(s, n, u)
