"""Finish a product subdomain folder after index.html is written.

usage: finish_site.py <sub> "<Product Name>" <brand-regex> <buy-link> <date> <google-font-family-param>
e.g.  finish_site.py visiflora "VisiFlora" "visiflora" "https://mwebtrackwise.com/12271/5654/7/?" 2026-10-18 "Jost:wght@400;500;600;700;800"
"""
import glob, html, io, json, os, re, secrets, subprocess, sys

sub, product, brand_re, link, date, font = sys.argv[1:7]
ROOT = r"D:\Medicne Bing"
host = f"{sub}.medipicker.com"
folder = os.path.join(ROOT, host)

subprocess.run([sys.executable, "-I", "-X", "utf8", os.path.join(ROOT, "_build", "debrand_subdomain.py"), host, product, host],
               cwd=ROOT, check=True)

logo = f'class="logo">{product} <span>Reviews</span>'
for f in ("disclaimer.html", "privacy-policy.html", "terms.html"):
    p = os.path.join(folder, f)
    s = io.open(p, encoding="utf-8").read()
    s = re.sub(r'class="logo">.*?</span>', logo, s, count=1)
    s = re.sub(r'family=Jost:wght@[0-9;]+', "family=" + font, s)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)

for old in glob.glob(os.path.join(folder, "*.txt")):
    if re.fullmatch(r"[0-9a-f]{32}\.txt", os.path.basename(old)):
        key = os.path.basename(old)[:-4]
        break
else:
    key = secrets.token_hex(16)
    io.open(os.path.join(folder, key + ".txt"), "w", newline="").write(key)

# Run the pages.dev redirect function only for "/" (Workers free plan = 100k invocations/day per account);
# every other pages.dev URL gets noindex instead.
io.open(os.path.join(folder, "_routes.json"), "w", newline="\n").write('{\n  "version": 1,\n  "include": ["/"],\n  "exclude": []\n}\n')
io.open(os.path.join(folder, "_headers"), "w", newline="\n").write(
    "# Keep *.pages.dev preview addresses out of search results (the homepage there also 301s to the real domain).\n"
    "https://:project.pages.dev/*\n  X-Robots-Tag: noindex\n")
io.open(os.path.join(folder, "robots.txt"), "w", newline="\n").write(
    f"User-agent: *\nAllow: /\n\nSitemap: https://{host}/sitemap.xml\n")
urls = [("", "weekly", "1.0"), ("privacy-policy", None, "0.3"), ("disclaimer", None, "0.3"), ("terms", None, "0.3")]
io.open(os.path.join(folder, "sitemap.xml"), "w", newline="\n").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>https://{host}/{u}</loc><lastmod>{date}</lastmod>"
              + (f"<changefreq>{c}</changefreq>" if c else "") + f"<priority>{p}</priority></url>\n" for u, c, p in urls)
    + "</urlset>\n")

# checks
s = io.open(os.path.join(folder, "index.html"), encoding="utf-8").read()
d = json.loads(re.findall(r'(?is)<script[^>]+ld\+json[^>]*>(.*?)</script>', s)[0])
faq = [x for x in d["@graph"] if x["@type"] == "FAQPage"][0]["mainEntity"]
vis = [(html.unescape(q), html.unescape(a)) for q, a in re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>', s)]
ok = len(faq) == len(vis) and all(f["name"] == v[0] and f["acceptedAnswer"]["text"] == v[1] for f, v in zip(faq, vis))
b = re.sub(r"(?is)<(script|style|svg|head)[^>]*>.*?</\1>", " ", s)
t = html.unescape(re.sub(r"<[^>]+>", " ", b))
n = len(re.findall(r"[A-Za-z0-9'$]+", t))
k = len(re.findall(brand_re, t, re.I))
print(f"key={key}")
print(f"faq {len(faq)}/{len(vis)} match={ok} | words {n} | brand {k} ({k / n * 100:.2f}%) | buy links {s.count(link)} | h2 {s.count('<h2')}")
bad = [f for f in os.listdir(folder) if f.endswith(".html")
       and re.search(r"affiliate|commission", io.open(os.path.join(folder, f), encoding="utf-8").read(), re.I)]
print("affiliate/commission in:", bad or "none")
print("msvalidate:", s.count("msvalidate.01"), "| .html legal links:", len(re.findall(r'(privacy-policy|terms|disclaimer)\.html', s)))
