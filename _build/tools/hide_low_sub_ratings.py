"""Remove the visible rating box and the schema.org Review from in-depth reviews rated below 3.0 (idempotent).

User decision 2026-11-13: star ratings are shown (and marked up) only from 3.0/5; lower scores stay internal
(they still decide buy buttons vs. a plain official-website link).
"""
import io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from ratings import SUB

SHOW = 3.0
ROOT = os.path.join(HERE, "..", "..", "medipicker.com", "reviews")

for sub, score in SUB.items():
    if score >= SHOW:
        continue
    path = os.path.join(ROOT, sub, "index.html")
    s = io.open(path, encoding="utf-8").read()
    s, nbox = re.subn(r'<div class="rating-box">.*?</div>\n?', "", s, flags=re.S)

    def strip_review(m):
        d = json.loads(m.group(1))
        hit = 0
        for node in d.get("@graph", [d]):
            if node.get("@type") == "Product" and "review" in node:
                del node["review"]; hit += 1
        return ('<script type="application/ld+json">\n' + json.dumps(d, ensure_ascii=False, indent=2) + "\n</script>") if hit else m.group(0)
    s, nld = re.subn(r'<script type="application/ld\+json">\s*(\{.*?"@type": "Product".*?\})\s*</script>', strip_review, s, count=1, flags=re.S)
    io.open(path, "w", encoding="utf-8", newline="").write(s)
    print(f"{sub} {score}: removed {nbox} rating box(es); Review markup {'removed' if '\"reviewRating\"' not in s else 'STILL PRESENT'}")
