"""Competitor summary: title, description, H1-H3, word count, brand count, schema types, colours, fonts.
usage: comp.py <html> <brand-regex>"""
import html, re, sys, json, collections

src = open(sys.argv[1], encoding="utf-8", errors="ignore").read()
brand = sys.argv[2]
t = re.search(r"(?is)<title>(.*?)</title>", src)
print("TITLE:", html.unescape(t.group(1)).strip() if t else "")
d = re.search(r'(?is)<meta[^>]+name="description"[^>]+content="([^"]*)"', src)
print("DESC:", html.unescape(d.group(1)) if d else "")
types = re.findall(r'"@type"\s*:\s*"([^"]+)"', src)
print("SCHEMA:", dict(collections.Counter(types)))
for lvl, txt in re.findall(r"(?is)<(h[1-3])[^>]*>(.*?)</\1>", src):
    s = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", txt))).strip()
    if s:
        print(f"  {lvl.upper()}: {s[:110]}")
body = re.sub(r"(?is)<(script|style|noscript|svg|head)[^>]*>.*?</\1>", " ", src)
text = html.unescape(re.sub(r"<[^>]+>", " ", body))
words = re.findall(r"[A-Za-z0-9'$]+", text)
k = len(re.findall(brand, text, re.I))
print(f"WORDS {len(words)} | brand {k} ({k / max(len(words), 1) * 100:.2f}%) | imgs {len(re.findall(r'<img', src, re.I))}")
cols = collections.Counter(c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}\b", src))
print("COLOURS:", cols.most_common(10))
print("FONTS:", set(re.findall(r"family=([A-Za-z+]+)", src)) | set(re.findall(r"font-family:\s*['\"]?([A-Za-z ]+)", src)))
alts = re.findall(r'(?is)<img[^>]+alt="([^"]*)"', src)
print("ALTS:", alts[:12])
