"""Add the editorial rating to every <sub>.medipicker.com review (idempotent).

- visible rating box at the start of the verdict (or a new verdict section for the oldest sites)
- schema.org Review (author MediPicker Editorial Team) inside the page's Product node
- rating CSS appended to the site's styles.css
Ratings and the three missing verdicts live in _build/ratings.py (SUB, SUB_VERDICT).
New sub-sites: add a SUB rating, then run this script.
"""
import html, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from ratings import SUB, SUB_VERDICT, label

ROOT = os.path.join(HERE, "..", "..")
DATE = "2026-11-05"
CSS = """
/* MediPicker editorial rating */
.rating-box { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 14px; margin: 10px 0 16px; padding: 12px 16px; border: 1px solid #e3e6df; border-radius: 12px; background: #f6f7f4; }
.rating-box a { font-size: 15px; margin-left: auto; }
.rating-stars { position: relative; display: inline-block; font-size: 22px; line-height: 1; letter-spacing: 2px; }
.rating-stars .rs-bg { color: #cfd5ca; }
.rating-stars .rs-fg { position: absolute; left: 0; top: 0; overflow: hidden; white-space: nowrap; color: #d99a00; }
"""


def box(score):
    return ('<div class="rating-box"><span class="rating-stars" aria-hidden="true"><span class="rs-bg">&#9733;&#9733;&#9733;&#9733;&#9733;</span>'
            f'<span class="rs-fg" style="width:{score / 5 * 100:.0f}%">&#9733;&#9733;&#9733;&#9733;&#9733;</span></span>'
            f'<span><strong>MediPicker rating: {score:.1f} / 5</strong> &middot; {label(score)}</span>'
            '<a href="https://medipicker.com/how-we-review#ratings">How we rate</a></div>\n')


for sub, score in SUB.items():
    folder = os.path.join(ROOT, "medipicker.com", "reviews", sub)  # moved from <sub>.medipicker.com on 10 Nov 2026
    path = os.path.join(folder, "index.html")
    s = io.open(path, encoding="utf-8").read()
    if 'class="rating-box"' in s:
        print(sub, "already done"); continue
    name = json.loads(re.search(r'"@type": "Product".*?"name": (".*?")', s, re.S).group(1))

    if sub in SUB_VERDICT:
        verdict = SUB_VERDICT[sub]
        m = re.search(r'<h2[^>]*>[^<]*Pros &amp; Cons</h2>.*?(?=<h2)', s, re.S)
        block = (f'<h2 id="verdict">Our Verdict on {html.escape(name)}</h2>\n{box(score)}<p>{html.escape(verdict)}</p>\n\n')
        s = s[:m.end()] + block + s[m.end():]
    else:
        m = re.search(r'(<h[34][^>]*>\s*(?:Our )?Verdict on [^<]*</h[34]>\s*)(<p>(.*?)</p>)', s, re.S)
        verdict = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", m.group(3)))).strip()
        s = s[:m.start(2)] + box(score) + s[m.start(2):]

    def add_review(mt):
        d = json.loads(mt.group(1))
        for node in d.get("@graph", [d]):
            if node.get("@type") == "Product":
                node["review"] = {"@type": "Review",
                                  "author": {"@type": "Organization", "name": "MediPicker Editorial Team", "url": "https://medipicker.com/about"},
                                  "publisher": {"@type": "Organization", "name": "MediPicker", "url": "https://medipicker.com/"},
                                  "datePublished": DATE, "name": f"{name} review", "reviewBody": verdict,
                                  "reviewRating": {"@type": "Rating", "ratingValue": f"{score:.1f}", "bestRating": "5", "worstRating": "1"}}
        return '<script type="application/ld+json">\n' + json.dumps(d, ensure_ascii=False, indent=2) + "\n</script>"
    s, n = re.subn(r'<script type="application/ld\+json">\s*(\{.*?"@type": "Product".*?\})\s*</script>', add_review, s, count=1, flags=re.S)
    assert n == 1, sub
    io.open(path, "w", encoding="utf-8", newline="").write(s)

    css = os.path.join(folder, "styles.css")
    c = io.open(css, encoding="utf-8").read()
    if "rating-box" not in c:
        io.open(css, "a", encoding="utf-8", newline="").write(CSS)
    print(sub, score, "ok", "| verdict:", verdict[:60])
