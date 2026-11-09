"""Build the whole medipicker.com site into ../medipicker.com/

  - index.html            home page / product directory
  - blog/index.html       list of all product reviews
  - blog/<slug>/index.html  one SEO page per product
  - sitemap.xml, robots.txt

Run:  py -X utf8 _build/build_site.py
Inputs: products.tsv (name<TAB>link), facts.json (from sales pages), content.py (category copy).
"""
import datetime, html, io, json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_home import CATEGORY, CAT_ORDER, CAT_ICON, DEFAULT_CAT, load, slug  # noqa: E402
from content import CATEGORY_COPY, OVERRIDES, FULL_REVIEWS, DISABLED  # noqa: E402
from ingredients import ING  # noqa: E402
from ratings import BLOG as BLOG_RATINGS, label as rating_label  # noqa: E402


def rating_box(score, root):
    """Visible editorial rating; must match the Review markup."""
    stars = (f'<span class="rating-stars" aria-hidden="true"><span class="rs-bg">&#9733;&#9733;&#9733;&#9733;&#9733;</span>'
             f'<span class="rs-fg" style="width:{score / 5 * 100:.0f}%">&#9733;&#9733;&#9733;&#9733;&#9733;</span></span>')
    return (f'      <div class="rating-box">{stars}'
            f'<span><strong>MediPicker rating: {score:.1f} / 5</strong> &middot; {rating_label(score)}</span>'
            f'<a href="{root}how-we-review#ratings">How we rate</a></div>\n')


def review_ld(p):
    d = p["bd"]
    return {"@type": "Review", "author": {"@type": "Organization", "name": "MediPicker Editorial Team", "url": DOMAIN + "/about"},
            "publisher": {"@type": "Organization", "name": "MediPicker", "url": DOMAIN + "/"},
            "datePublished": p["updated"], "name": f"{p['name']} review",
            "reviewBody": d["verdict"],
            "reviewRating": {"@type": "Rating", "ratingValue": f"{BLOG_RATINGS[p['slug']]:.1f}", "bestRating": "5", "worstRating": "1"}}
BLOG_DATA = os.path.join(HERE, "blog_data")

SITE = os.path.join(os.path.dirname(HERE), "medipicker.com")
DOMAIN = "https://medipicker.com"
TODAY = "2026-10-15"
TODAY_TXT = "October 15, 2026"
MOVED = "2026-11-10"  # in-depth reviews moved from sub-domains to /reviews/<sub>/
YEAR = "2026"
e = html.escape

SPECIAL = {"egcg": "EGCG", "coq10": "CoQ10", "5-htp": "5-HTP", "gaba": "GABA", "alpha-gpc": "Alpha-GPC", "nac": "NAC",
           "msm": "MSM", "rs2": "RS2"}


def nice(ing):
    if ing in SPECIAL:
        return SPECIAL[ing]
    if any(c.isupper() for c in ing):
        return ing
    out = []
    for w in ing.split(" "):
        out.append("-".join(SPECIAL.get(p, p[:1].upper() + p[1:]) for p in w.split("-")))
    return " ".join(out).replace("Vitamin B12", "Vitamin B12")


def products():
    facts = json.load(io.open(os.path.join(HERE, "facts.json"), encoding="utf-8"))
    items = []
    for p in load():
        if p["key"] in DISABLED:
            continue
        f = dict(facts.get(slug(p["key"]), {}))
        f.pop("form", None)  # auto-detected product type is unreliable; only hand-checked overrides set it
        f.update(OVERRIDES.get(p["key"], {}))
        if p["cat"] == "Home & Lifestyle":
            f["ingredients"] = []
        p["facts"] = f
        p["slug"] = slug(p["name"].replace("(", "").replace(")", ""))
        p["full_review"] = FULL_REVIEWS.get(p["key"])
        bd_path = os.path.join(BLOG_DATA, p["slug"] + ".json")
        p["bd"] = json.load(io.open(bd_path, encoding="utf-8")) if os.path.exists(bd_path) else None
        p["updated"] = (p["bd"] or {}).get("checked", TODAY)
        if p["bd"]:
            # hand-checked sales-page facts replace the automatic extraction
            if p["bd"].get("packages"):
                f["prices"] = sorted({round(t / b) for b, t, _ in p["bd"]["packages"]})
            for k in ("guarantee_days", "form"):
                if p["bd"].get(k):
                    f[k] = p["bd"][k]
            f["one_time"] = p["bd"].get("one_time", False)
            f["currency"] = p["bd"].get("currency", "USD")
            f["free_shipping"] = (any("free" in sh.lower() for _, _, sh in p["bd"].get("packages", []))
                                  or "free" in p["bd"].get("price_note", "").lower())
        items.append(p)
    return items


def seo(p):
    n, c = p["name"], CATEGORY_COPY[p["cat"]]
    f = p["facts"]
    # Bing flags titles over ~65 characters, so fall back to shorter patterns for long product names.
    title = next(t for t in (f"{n} Review 2026: Ingredients, Price & Where to Buy", f"{n} Review 2026: Ingredients, Price & Safety",
                             f"{n} Review 2026: Ingredients & Price", f"{n} Review 2026") if len(t) <= 60 or t.endswith("2026"))
    if len(title) + len(" | MediPicker") <= 65:
        title += " | MediPicker"
    parts = [f"{n} review: what this {c['noun']} contains"]
    if f.get("prices"):
        parts.append(f"price from ${min(f['prices'])}/bottle")
    if f.get("guarantee_days"):
        parts.append(f"{f['guarantee_days']}-day guarantee")
    desc = ", ".join(parts) + f" and where to buy {n} from the official website."
    if len(desc) > 160:
        desc = f"{n} review: ingredients, price, guarantee and where to buy {n} from the official website."
    if len(desc) > 160:
        desc = f"{n} review: ingredients, price and where to buy {n}."
    low = n.lower()
    kws = [low, f"{low} reviews", f"{low} review", f"{low} ingredients", f"{low} price", f"buy {low}",
           f"{low} official website", f"{low} side effects"]
    if c["keyword"]:
        kws.append(f"{low} {c['keyword']}")
    return title, desc, ", ".join(kws)


HEAD = """<!doctype html>
<html lang="en-US">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="{robots}">
  <meta property="og:type" content="{ogtype}">
  <meta property="og:site_name" content="MediPicker">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary">
  <link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{root}styles.css">
  <script type="application/ld+json">
{ld}
  </script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header" id="top">
  <div class="container nav">
    <a href="{root}" class="logo">Medi<span>Picker</span></a>
    <nav class="nav-links" aria-label="Main">
      <a href="{root}blog/">Reviews</a>
      <a href="{root}#products">All Products</a>
      <a href="{root}#how">How We Choose</a>
    </nav>
  </div>
</header>
"""

FOOT = """<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <a href="{root}" class="logo">Medi<span>Picker</span></a>
      <nav class="footer-links" aria-label="Footer">
        <a href="{root}blog/">Reviews</a>
        <a href="{root}#products">All Products</a>
        <a href="{root}about">About</a>
        <a href="{root}how-we-review">How We Review</a>
        <a href="{root}contact">Contact</a>
        <a href="{root}privacy-policy">Privacy Policy</a>
        <a href="{root}terms">Terms</a>
        <a href="{root}disclaimer">Disclaimer</a>
      </nav>
    </div>
    <p class="disclaimer">MediPicker is an independent review site. We are not the maker, seller or distributor of any product listed — always buy from the official website, check the label and talk to your doctor before starting a supplement.</p>
    <p class="disclaimer">*Statements on this website have not been evaluated by the Food and Drug Administration. Products are not intended to diagnose, treat, cure or prevent any disease. Information here is for general education and is not a substitute for advice from a qualified medical professional. Individual results may vary.</p>
    <p class="copyright">&copy; {year} MediPicker. All rights reserved.</p>
  </div>
</footer>
<a href="#top" class="to-top" aria-label="Back to top">&uarr;</a>
<script>
  (function () {{
    var t = document.querySelector('.to-top');
    window.addEventListener('scroll', function () {{ t.classList.toggle('show', window.scrollY > 600); }}, {{ passive: true }});
  }})();
</script>
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "9b34e71be0224e769409a669b329971e"}}'></script>
</body>
</html>
"""


def buy(p, label="Buy Now", cls="btn btn-buy"):
    return f'<a class="{cls}" href="{e(p["link"])}" rel="sponsored nofollow noopener" target="_blank">{label}</a>'


def page_url(q, root=""):
    """Where a product's review lives: its in-depth /reviews/<sub>/ page when there is one, otherwise its blog page."""
    return q["full_review"] if q.get("full_review") else f"{root}blog/{q['slug']}/"


def low_rated(p):
    """Rated 2/5 or lower: no buy buttons, one plain link to the official website (decided 10 Nov 2026)."""
    return bool(p.get("bd")) and BLOG_RATINGS.get(p["slug"], 5) <= 2.0


def disclosure(root):
    return (f'      <p class="disclosure">MediPicker may earn money when you buy through links on this page. Sellers can&rsquo;t pay for a review '
            f'or a better rating. <a href="{root}how-we-review#money">How we make money</a></p>\n')


def faq_items(p):
    n, c, f = p["name"], CATEGORY_COPY[p["cat"]], p["facts"]
    what = (p["bd"]["claim"] if p.get("bd") else
            f"{n} is a {c['noun']} designed to {c['purpose']}. It is sold through its official website.")
    qa = [(f"What is {n}?", what)]
    if f.get("prices"):
        lo, hi = min(f["prices"]), max(f["prices"])
        price = (f"On the official website {n} costs {sym(p)}{lo} per bottle." if lo == hi else
                 f"On the official website {n} costs between {sym(p)}{lo} and {sym(p)}{hi} per bottle, depending on how many bottles you buy. Larger packages have the lowest price per bottle.")
    else:
        price = f"Prices for {n} are listed on its official website and usually drop when you buy more than one unit."
    qa.append((f"How much does {n} cost?", price))
    if f.get("guarantee_days"):
        qa.append((f"Does {n} have a money-back guarantee?",
                   f"Yes. According to the official website, {n} comes with a {f['guarantee_days']}-day money-back guarantee on orders placed there."))
    qa.append((f"Where can I buy {n}?",
               f"The safest place to buy {n} is the official website, where you get genuine product and the maker's guarantee. Third-party listings may not include the guarantee."))
    if p["cat"] != "Home & Lifestyle":
        qa.append((f"Is {n} safe?", c["safety"][0] + " " + c["safety"][1]))
    return qa


def nice_date(iso):
    dt = datetime.date.fromisoformat(iso)
    return f"{dt:%B} {dt.day}, {dt.year}"


INDEX = "index, follow, max-image-preview:large, max-snippet:-1"


def robots(p):
    """Only product-specific (hand-checked) reviews are indexed; template pages stay out of Google until rewritten."""
    return INDEX if p.get("bd") else "noindex, follow"


SYM = {"USD": "$", "EUR": "\u20ac", "GBP": "\u00a3"}


def sym(p):
    return SYM[p["facts"].get("currency", "USD")]


def money(x, s="$"):
    return f"{s}{x:,.2f}".replace(".00", "")


def per_bottle(q):
    """Lowest verified price per bottle for comparison tables, or None."""
    if q.get("bd") and q["bd"].get("packages"):
        return min(t / b for b, t, _ in q["bd"]["packages"])
    return min(q["facts"]["prices"]) if q["facts"].get("prices") else None


def rich(p, by_cat):
    """Product-specific sections built from hand-checked sales-page facts (blog_data/<slug>.json)."""
    n, d, c = e(p["name"]), p["bd"], CATEGORY_COPY[p["cat"]]
    days = d.get("days_per_bottle", 30)
    out = {}
    claim = f'      <h2>What Is {n}?</h2>\n      <p>{e(d["claim"])}</p>\n'
    if d.get("story"):
        claim += f'      <p>{e(d["story"])}</p>\n'
    out["what"] = claim

    checks = "\n".join(f"          <li>{e(x)}</li>" for x in d.get("checks", []))
    out["claims"] = (f'      <h2>{n} Claims vs. Evidence</h2>\n'
                     + (f'      <p>The official website leads with this headline:</p>\n      <blockquote class="hook">&ldquo;{e(d["hook"])}&rdquo;</blockquote>\n' if d.get("hook") else "")
                     + f'      <p>Here is how the main claims hold up against published research and the information the seller actually provides:</p>\n'
                     + f'      <ul class="check-list">\n{checks}\n      </ul>\n') if checks else ""

    ings = [i for i in d.get("ingredients", [])]
    if ings:
        parts = [f'      <h2>{n} Ingredients</h2>',
                 f'      <p>The official website names {len(ings)} key ingredient{"s" if len(ings) != 1 else ""} in {n}. Here is what each one is and what research says about it.</p>']
        for k in ings:
            info = ING.get(k.lower())
            name = info["name"] if info else k[:1].upper() + k[1:]
            parts.append(f'      <h3>{e(name)}</h3>')
            if info:
                parts.append(f'      <p>{e(info["what"])} {e(info["evidence"])}</p>')
        if d.get("ing_note"):
            parts.append(f'      <p>{e(d["ing_note"])}</p>')
        out["ingredients"] = "\n".join(parts) + "\n"
    else:
        out["ingredients"] = (f'      <h2>{n} Ingredients</h2>\n      <p>{e(d.get("ing_note") or "The official website does not list the ingredients in text form. Ask the seller for the supplement facts label before you buy, especially if you have allergies or take medication.")}</p>\n')

    if d.get("use"):
        out["use"] = f'      <h2>How to Take {n}</h2>\n      <p>{e(d["use"])}</p>\n'

    rows = []
    for b, t, ship in sorted(d.get("packages", []), key=lambda r: r[0]):
        rows.append(f"            <tr><td>{b} bottle{'s' if b > 1 else ''}</td><td>{b * days} days</td><td>{money(t, sym(p))}</td>"
                    f"<td>{money(t / b, sym(p))}</td><td>{money(t / (b * days), sym(p))}</td><td>{e(ship)}</td></tr>")
    price = [f'      <h2>{n} Price &amp; Money-Back Guarantee</h2>']
    if rows:
        price.append(f'      <p>These are the packages shown on the official {n} order page when we checked it. The cost per day assumes one bottle lasts {days} days, as the seller states.</p>')
        price.append('      <div class="table-wrap"><table class="price-table">\n          <thead><tr><th>Package</th><th>Supply</th><th>Total</th><th>Per bottle</th><th>Per day</th><th>Shipping</th></tr></thead>\n          <tbody>\n'
                     + "\n".join(rows) + '\n          </tbody>\n        </table></div>')
    if d.get("price_note"):
        price.append(f'      <p>{e(d["price_note"])}</p>')
    elif not rows:
        price.append(f'      <p>The official website doesn\'t show {n} prices until you reach the order page, so check the current packages there before you buy.</p>')
    g = d.get("guarantee_days")
    if g:
        price.append(f'      <p>Orders from the official website come with a <strong>{g}-day money-back guarantee</strong>. {e(d.get("refund_note", ""))}</p>')
    if d.get("one_time"):
        price.append('      <p>Billing is a one-time payment &mdash; the seller states there is no subscription or automatic rebilling.</p>')
    if d.get("bonuses"):
        price.append(f'      <p>Larger packages come with these free bonus guides:</p>\n      <ul>\n' + "\n".join(f"        <li>{e(x)}</li>" for x in d["bonuses"]) + "\n      </ul>")
    out["price"] = "\n".join(price) + "\n"

    if d.get("pros") or d.get("cons"):
        out["proscons"] = (f'      <h2>{n} Pros and Cons</h2>\n      <div class="pros-cons">\n        <div><h3>Pros</h3>\n        <ul class="check-list">\n'
                           + "\n".join(f"          <li>{e(x)}</li>" for x in d.get("pros", []))
                           + '\n        </ul></div>\n        <div><h3>Cons</h3>\n        <ul class="check-list warn">\n'
                           + "\n".join(f"          <li>{e(x)}</li>" for x in d.get("cons", []))
                           + "\n        </ul></div>\n      </div>\n")

    extra_safety = []
    for k in ings:
        info = ING.get(k.lower())
        if info and info.get("safety") and info["safety"] not in extra_safety:
            extra_safety.append(info["safety"])
    out["safety_extra"] = extra_safety

    peers = [q for q in by_cat[p["cat"]] if q is not p and per_bottle(q)]
    peers = sorted(peers, key=lambda q: (q.get("bd") is None, q["name"]))[:4]
    if peers and per_bottle(p):
        def row(q, me=False):
            g2 = (q.get("bd") or {}).get("guarantee_days") or q["facts"].get("guarantee_days")
            name = e(q["name"]) if me else f'<a href="../{q["slug"]}/">{e(q["name"])}</a>'
            return f"            <tr{' class=\"me\"' if me else ''}><td>{name}</td><td>From {money(per_bottle(q), sym(q))}</td><td>{str(g2) + ' days' if g2 else '&ndash;'}</td></tr>"
        out["compare"] = (f'      <h2>{n} vs. Similar {e(p["cat"])} Products</h2>\n'
                          f'      <p>How {n} compares on price and refund window with other {e(c["noun"])}s we have reviewed:</p>\n'
                          '      <div class="table-wrap"><table class="price-table">\n          <thead><tr><th>Product</th><th>Price per bottle</th><th>Guarantee</th></tr></thead>\n          <tbody>\n'
                          + row(p, True) + "\n" + "\n".join(row(q) for q in peers) + '\n          </tbody>\n        </table></div>\n')
    out["verdict"] = (f'      <h2>Our Verdict on {n}</h2>\n{rating_box(BLOG_RATINGS[p["slug"]], "../../")}      <p>{e(d["verdict"])}</p>\n'
                      if d.get("verdict") else "")
    return out


def product_page(p, by_cat):
    n, c, f = p["name"], CATEGORY_COPY[p["cat"]], p["facts"]
    root = "../../"
    url = f"{DOMAIN}/blog/{p['slug']}/"
    title, desc, kws = seo(p)
    faqs = faq_items(p)
    R = rich(p, by_cat) if p["bd"] else {}
    if p["bd"]:
        d = p["bd"]
        if d.get("use"):
            faqs.insert(1, (f"How do you take {n}?", d["use"]))
        if d.get("packages"):
            days = d.get("days_per_bottle", 30)
            six = any(b == 6 for b, _, _ in d["packages"])
            faqs.insert(2, (f"How long does one bottle of {n} last?",
                            f"According to the official website, one bottle is a {days}-day supply"
                            + (f", so the 6-bottle package lasts about {6 * days // 30} months." if six else ".")))
        faqs += [tuple(x) for x in d.get("faqs", [])]
    lo = min(f["prices"]) if f.get("prices") else None
    hi = max(f["prices"]) if f.get("prices") else None
    g = f.get("guarantee_days")

    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": f"{n} Review 2026: Ingredients, Price & Where to Buy", "description": desc,
         "datePublished": TODAY, "dateModified": p["updated"], "mainEntityOfPage": url,
         "author": {"@type": "Organization", "name": "MediPicker Editorial Team", "url": DOMAIN + "/about"},
         "publisher": {"@type": "Organization", "name": "MediPicker", "url": DOMAIN + "/"}, "inLanguage": "en-US"},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "MediPicker", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": "Reviews", "item": DOMAIN + "/blog/"},
            {"@type": "ListItem", "position": 3, "name": f"{n} Review", "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
    ]}
    # Product markup only on rated, indexable reviews with verified prices; it carries our editorial Review so
    # Google's product snippet has the review it asks for. No aggregateRating: we don't have genuine reader ratings.
    if p["cat"] != "Home & Lifestyle" and lo and p["bd"]:
        ld["@graph"].append({
            "@type": "Product", "name": n, "category": "Dietary Supplement" if p["cat"] != "Pets" else "Pet Supplement",
            "description": p["bd"]["claim"].split(". ")[0].rstrip(".") + ".",
            "offers": {"@type": "AggregateOffer", "priceCurrency": f.get("currency", "USD"), "lowPrice": str(lo), "highPrice": str(hi),
                       "offerCount": str(len(f["prices"])), "availability": "https://schema.org/InStock", "url": url},
            "review": review_ld(p)})

    facts_rows = [("Category", e(p["cat"]))]
    if f.get("form"):
        facts_rows.append(("Form", e(f["form"].capitalize())))
    facts_rows.append(("Price", f"From {sym(p)}{lo} per bottle" if lo else "See official website"))
    facts_rows.append(("Guarantee", f"{g}-day money-back guarantee" if g else "See official website"))
    if f.get("one_time"):
        facts_rows.append(("Billing", "One-time payment"))
    if f.get("free_shipping"):
        facts_rows.append(("Shipping", "Free shipping on some packages"))
    low = low_rated(p)
    facts_rows.append(("Where to buy", f'<a href="#where-to-buy">Official website only</a>' if low else
                       f'<a href="{e(p["link"])}" rel="sponsored nofollow noopener" target="_blank">Official {e(n)} website</a>'))
    facts_html = "\n".join(f"          <div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in facts_rows)

    if f.get("ingredients"):
        ing_html = ("        <p>These ingredients are named on the official website:</p>\n        <ul class=\"ing-list\">\n"
                    + "\n".join(f"          <li>{e(nice(i))}</li>" for i in f["ingredients"])
                    + "\n        </ul>\n        <p>Exact amounts aren't always shown on the sales page, so check the supplement facts label on your bottle for the complete formula.</p>")
    else:
        ing_html = (f"        <p>The official website doesn't list its full ingredients in text form. Check the product label or the official website for the complete formula and amounts before you buy, especially if you have allergies or take medication.</p>")

    if lo:
        price_p = (f"On the official website, {e(n)} costs <strong>{sym(p)}{lo} per bottle</strong>." if lo == hi else
                   f"On the official website, {e(n)} costs between <strong>{sym(p)}{lo} and {sym(p)}{hi} per bottle</strong>, depending on the package. Buying more bottles at once lowers the price per bottle, which is why multi-bottle packages are the most popular.")
    else:
        price_p = f"Current prices and package options are shown on the official website. Like most products in this category, the price per unit usually drops when you buy a larger package."
    guar_p = (f"Every order from the official website is covered by a <strong>{g}-day money-back guarantee</strong>, so you have time to try it and request a refund if it isn't right for you." if g else
              f"Check the official website for {e(n)}'s refund policy before ordering.")

    review_callout = ""
    if p["full_review"]:
        review_callout = f'''      <aside class="callout">
        <strong>Want the full details?</strong> Read our in-depth <a href="{p['full_review']}">{e(n)} review</a> with ingredients, science, side effects and a full FAQ.
      </aside>
'''

    # In-depth reviews in the same category first, then the next blog reviews in the list (rotating, so every
    # page gets links from its neighbours rather than every page linking to the same first four).
    group = by_cat[p["cat"]]
    deep = [q for q in group if q.get("full_review") and q is not p]
    i = group.index(p)
    others = [q for q in group[i + 1:] + group[:i] if not q.get("full_review")]
    deep_html = ""
    if deep:
        deep_html = ('      <section class="related" aria-labelledby="deep-h">\n        <h2 id="deep-h">In-Depth ' + e(p["cat"]) + ' Reviews</h2>\n'
                     '        <p>Full label analysis, research on each ingredient, side effects and verified prices:</p>\n        <ul>\n'
                     + "\n".join(f'          <li><a href="{e(q["full_review"])}">{e(q["name"])} Review</a></li>' for q in deep[:6])
                     + "\n        </ul>\n      </section>\n")
    related_html = deep_html
    if others[:4]:
        related_html += ('      <section class="related" aria-labelledby="rel-h">\n        <h2 id="rel-h">More ' + e(p["cat"]) + ' Reviews</h2>\n        <ul>\n'
                         + "\n".join(f'          <li><a href="../{q["slug"]}/">{e(q["name"])} Review</a></li>' for q in others[:4])
                         + "\n        </ul>\n      </section>\n")

    safety_html = "\n".join(f"          <li>{e(s)}</li>" for s in list(c["safety"]) + R.get("safety_extra", []))
    fit_html = "\n".join(f"          <li>{e(s)}</li>" for s in c["fit"])
    faq_html = "\n".join(f"          <details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faqs)

    ing_section = "" if p["cat"] == "Home & Lifestyle" else f'''
      <h2>{e(n)} Ingredients</h2>
{ing_html}
'''
    if R:
        ing_section = R["ingredients"] + R.get("use", "")
    what_default = f'''      <h2>What Is {e(n)}?</h2>
      <p>{e(n)} is a {e(c["noun"])} sold through its official website. {e(c["intro"])}</p>
'''
    price_default = f'''      <h2>{e(n)} Price &amp; Money-Back Guarantee</h2>
      <p>{price_p}</p>
      <p>{guar_p}</p>
'''
    how_default = f'''      <h2>How Does {e(n)} Work?</h2>
      <p>{e(c["how"])} As with any {e(c["noun"])}, results vary from person to person.</p>
'''
    fit_default = f'''      <h2>Who Is {e(n)} For?</h2>
      <ul class="check-list">
{fit_html}
      </ul>

'''
    if R:
        lede = (f'{e(p["bd"]["claim"].split(". ")[0].rstrip("."))}. We checked the official {e(n)} website for the ingredients, dosage, '
                f'prices and refund terms, compared the claims with published research and list the safety points to know before you buy.')
    else:
        lede = (f'<strong>{e(n)}</strong> is a {e(c["noun"])} designed to {e(c["purpose"])}.* In this review we cover what it is, the ingredients named '
                f'on its official website, the current price, the money-back guarantee and how to buy it safely.')
    safety_title = "Things to Know Before You Buy" if p["cat"] == "Home & Lifestyle" else f"Is {e(n)} Safe? Side Effects to Know"
    if low:
        where_html = (f'      <p>Given our rating, we don&rsquo;t recommend {e(n)} for most people{"; the options in our comparison above have better evidence or clearer labels" if R.get("compare") else ""}. '
                      f'If you still want to try it, buy only from the official website: it is the only seller that honours the '
                      f'{str(g) + "-day " if g else ""}money-back guarantee, and look-alike sites and marketplace listings may not. Keep your order confirmation for any refund.</p>\n'
                      f'      <p><a class="official-link" href="{e(p["link"])}" rel="sponsored nofollow noopener" target="_blank">Official {e(n)} website</a></p>\n')
    else:
        where_html = f'''      <p>The best place to buy {e(n)} is the official website. Ordering there means you get the genuine product, the current package prices and the maker's money-back guarantee. Be careful with look-alike websites and third-party marketplace listings, which may not offer the same protection.</p>
      <div class="buy-box">
        <div>
          <strong>{e(n)}</strong>
          <span>{("From " + sym(p) + str(lo) + " per bottle") if lo else "See current prices"}{(" &middot; " + str(g) + "-day guarantee") if g else ""}</span>
        </div>
        {buy(p, "Buy " + e(n) + " from the Official Website", "btn btn-buy")}
      </div>
'''

    body = f'''<main id="main" class="post">
  <div class="container post-wrap">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{root}">MediPicker</a> <span aria-hidden="true">&rsaquo;</span> <a href="{root}blog/">Reviews</a> <span aria-hidden="true">&rsaquo;</span> <span>{e(n)}</span></nav>
    <article>
      <span class="rc-tag">{e(p["cat"])}</span>
      <h1>{e(n)} Review 2026: Ingredients, Price &amp; Where to Buy</h1>
      <p class="byline">By <a href="{root}about"><strong>MediPicker Editorial Team</strong></a> &middot; <a href="{root}how-we-review">How we review</a> &middot; Updated <time datetime="{p['updated']}">{nice_date(p['updated'])}</time></p>
{disclosure(root)}      <p class="lede">{lede}</p>
{"" if low else "      <p>" + buy(p, "Buy " + e(n) + " Now", "btn btn-buy btn-lg") + "</p>" + chr(10)}
      <div class="facts-box">
        <h2 class="facts-title">{e(n)} Quick Facts</h2>
        <dl>
{facts_html}
        </dl>
      </div>

{review_callout}{R.get("what") or what_default}{R.get("claims") or how_default}
{ing_section}
{R.get("price") or price_default}{"" if low else "      <p>" + buy(p, "Check the Current Price") + "</p>" + chr(10)}{R.get("proscons", "")}
      <h2>{safety_title}</h2>
      <ul class="check-list warn">
{safety_html}
      </ul>

{"" if R else fit_default}{R.get("compare", "")}{R.get("verdict", "")}      <h2 id="where-to-buy">Where to Buy {e(n)}</h2>
{where_html}
      <h2>{e(n)} FAQ</h2>
      <div class="faq">
{faq_html}
      </div>

{related_html}    </article>
  </div>
</main>
'''
    ld_txt = json.dumps(ld, ensure_ascii=False, indent=2)
    return (HEAD.format(title=e(title), desc=e(desc), url=url, ogtype="article", root=root, ld=ld_txt, robots=robots(p))
            + body + FOOT.format(root=root, year=YEAR))


def review_btn(p):
    """Outlined review button for product cards; full reviews go straight to the in-depth sub-site."""
    arrow = '<svg class="rb-ico" viewBox="0 0 20 20" aria-hidden="true"><path d="M4 10h11M11 5l5 5-5 5"/></svg>'
    if p.get("full_review"):
        star = '<svg class="rb-star" viewBox="0 0 20 20" aria-hidden="true"><path d="M10 1.5l2.6 5.4 5.9.8-4.3 4.1 1 5.8L10 14.8l-5.2 2.8 1-5.8L1.5 7.7l5.9-.8z"/></svg>'
        return (f'<a class="btn btn-review btn-review-full" href="{e(p["full_review"])}">{star}Full Review{arrow}'
                f'<span class="sr-only"> of {e(p["name"])}</span></a>')
    return f'<a class="btn btn-review" href="blog/{p["slug"]}/">Read Review{arrow}<span class="sr-only"> of {e(p["name"])}</span></a>'


def blog_index(items, cats):
    root = "../"
    url = f"{DOMAIN}/blog/"
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Health Product Reviews", "url": url,
          "hasPart": [{"@type": "Article", "headline": f"{p['name']} Review", "url": DOMAIN + page_url(p, "/")} for p in items]}
    groups = []
    for c in cats:
        lis = "\n".join(f'        <li><a href="{e(p["full_review"]) if p.get("full_review") else p["slug"] + "/"}">{e(p["name"])} Review</a>'
                        f'{" <span class=\"deep-tag\">In-depth</span>" if p.get("full_review") else ""}</li>' for p in items if p["cat"] == c)
        groups.append(f'    <section class="blog-group" id="{slug(c)}">\n      <h2>{e(c)}</h2>\n      <ul>\n{lis}\n      </ul>\n    </section>')
    body = f'''<main id="main" class="post">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{root}">MediPicker</a> <span aria-hidden="true">&rsaquo;</span> <span>Reviews</span></nav>
    <h1 class="blog-h1">Health Product Reviews</h1>
    <p class="blog-sub">{len(items)} reviews covering ingredients, prices, guarantees and where to buy — grouped by category.</p>
    <div class="blog-groups">
{chr(10).join(groups)}
    </div>
  </div>
</main>
'''
    return (HEAD.format(title="Supplement Reviews: Ingredients, Prices &amp; Safety | MediPicker",
                        desc=e(f"Read {len(items)} health supplement reviews: ingredients, prices, money-back guarantees and where to buy each product from its official website."),
                        robots=INDEX,
                        url=url, ogtype="website", root=root, ld=json.dumps(ld, ensure_ascii=False, indent=2))
            + body + FOOT.format(root=root, year=YEAR))


def home(items, cats):
    counts = {c: sum(1 for p in items if p["cat"] == c) for c in cats}
    chips = "\n".join(f'        <button type="button" class="chip" data-filter="{slug(c)}" aria-pressed="false">{e(c)} <span>{counts[c]}</span></button>' for c in cats)

    def card(p):
        initials = "".join(w[0] for w in re.findall(r"[A-Za-z0-9]+", p["name"])[:2]).upper()
        return f'''      <li class="product" data-cat="{slug(p["cat"])}" data-name="{e(p["name"].lower())}">
        <div class="p-top">
          <span class="p-badge" aria-hidden="true">{e(initials)}</span>
          <div>
            <h3><a href="{e(page_url(p))}">{e(p["name"])}</a></h3>
            <span class="p-cat">{e(p["cat"])}</span>
          </div>
        </div>
        <div class="p-actions">
          <a class="btn btn-buy" href="{e(p["link"])}" rel="sponsored nofollow noopener" target="_blank">Buy Now<span class="sr-only"> {e(p["name"])}</span></a>
          {review_btn(p)}
        </div>
      </li>'''

    sections = []
    for c in cats:
        group = [p for p in items if p["cat"] == c]
        sections.append(f'''  <section class="cat-block" id="{slug(c)}" data-cat-block="{slug(c)}" aria-labelledby="h-{slug(c)}">
    <div class="cat-head">
      <span class="cat-icon" aria-hidden="true"><svg viewBox="0 0 24 24">{CAT_ICON.get(c, CAT_ICON[DEFAULT_CAT])}</svg></span>
      <h2 id="h-{slug(c)}">{e(c)}</h2>
      <span class="cat-count">{len(group)} products</span>
    </div>
    <ul class="product-grid">
{chr(10).join(card(p) for p in group)}
    </ul>
  </section>''')

    item_list = {"@context": "https://schema.org", "@type": "ItemList", "name": "MediPicker Health Product Directory",
                 "numberOfItems": len(items),
                 "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": p["name"], "url": DOMAIN + page_url(p, "/")} for i, p in enumerate(items)]}
    site_ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Organization", "@id": DOMAIN + "/#org", "name": "MediPicker", "url": DOMAIN + "/", "logo": DOMAIN + "/favicon.svg", "email": "info@medipicker.com",
         "contactPoint": {"@type": "ContactPoint", "contactType": "editorial", "email": "info@medipicker.com", "url": DOMAIN + "/contact"}},
        {"@type": "WebSite", "@id": DOMAIN + "/#website", "url": DOMAIN + "/", "name": "MediPicker",
         "publisher": {"@id": DOMAIN + "/#org"}, "inLanguage": "en-US"}]}
    tpl = io.open(os.path.join(HERE, "home_template.html"), encoding="utf-8").read()
    return (tpl.replace("{{COUNT}}", str(len(items))).replace("{{CAT_COUNT}}", str(len(cats)))
               .replace("{{CHIPS}}", chips).replace("{{SECTIONS}}", "\n\n".join(sections))
               .replace("{{ITEMLIST_LD}}", json.dumps(item_list, ensure_ascii=False, indent=2))
               .replace("{{SITE_LD}}", json.dumps(site_ld, ensure_ascii=False, indent=2)))


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    io.open(path, "w", encoding="utf-8", newline="\n").write(text)


def main():
    items = sorted(products(), key=lambda p: (CAT_ORDER.index(p["cat"]), p["name"].lower()))
    cats = [c for c in CAT_ORDER if any(p["cat"] == c for p in items)]
    by_cat = {c: [p for p in items if p["cat"] == c] for c in cats}

    write(os.path.join(SITE, "index.html"), home(items, cats))
    write(os.path.join(SITE, "blog", "index.html"), blog_index(items, cats))
    redirects = ["# Short blog pages of products with an in-depth review now redirect to it (10 Nov 2026)."]
    for p in items:
        if p.get("full_review"):
            old = os.path.join(SITE, "blog", p["slug"])
            if os.path.isdir(old):
                shutil.rmtree(old)
            redirects += [f"/blog/{p['slug']}/ {p['full_review']} 301", f"/blog/{p['slug']} {p['full_review']} 301"]
            continue
        write(os.path.join(SITE, "blog", p["slug"], "index.html"), product_page(p, by_cat))
    write(os.path.join(SITE, "_redirects"), "\n".join(redirects) + "\n")

    lastmod = {f"/blog/{p['slug']}/": p["updated"] for p in items if not p.get("full_review")}
    lastmod["/"] = lastmod["/blog/"] = max(lastmod.values())
    reviews = sorted(p["full_review"] for p in items if p.get("full_review"))
    lastmod.update({u: MOVED for u in reviews})
    for u in ("/", "/blog/", "/about", "/how-we-review", "/disclaimer"):
        lastmod[u] = MOVED
    urls = (["/", "/blog/"] + reviews + [f"/blog/{p['slug']}/" for p in items if robots(p) == INDEX and not p.get("full_review")]
            + ["/about", "/how-we-review", "/contact", "/privacy-policy", "/terms", "/disclaimer"])
    write(os.path.join(SITE, "sitemap.xml"),
          '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url>\n    <loc>{DOMAIN}{u}</loc>\n    <lastmod>{lastmod.get(u, TODAY)}</lastmod>\n  </url>\n" for u in urls) + "</urlset>\n")
    write(os.path.join(SITE, "robots.txt"), f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")

    titles = [seo(p) for p in items]
    print(f"{len(items)} products, {len(cats)} categories, {len(urls)} URLs in sitemap")
    print("longest title:", max(len(t) for t, _, _ in titles), "| longest description:", max(len(d) for _, d, _ in titles))
    print("disabled:", ", ".join(DISABLED))


if __name__ == "__main__":
    main()
