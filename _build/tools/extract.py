import sys, re, html
src = open(sys.argv[1], encoding="utf-8", errors="ignore").read()
src = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", src)
title = re.search(r"(?is)<title>(.*?)</title>", src)
print("TITLE:", html.unescape(title.group(1)).strip() if title else "")
for m in re.finditer(r'(?is)<meta[^>]+(name|property)="(description|og:[a-z]+)"[^>]+content="([^"]*)"', src):
    print("META", m.group(2), ":", html.unescape(m.group(3)))
for m in re.finditer(r'(?is)<img[^>]+src="([^"]+)"', src):
    print("IMG", m.group(1))
txt = re.sub(r"(?is)<br\s*/?>|</(p|div|h[1-6]|li|tr|section)>", "\n", src)
txt = html.unescape(re.sub(r"(?s)<[^>]+>", " ", txt))
lines = [re.sub(r"[ \t\u00a0]+", " ", l).strip() for l in txt.splitlines()]
print("\n".join(l for l in lines if l))
