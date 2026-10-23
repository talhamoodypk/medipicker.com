"""Build the whole medipicker.com site into ../medipicker.com/

  - index.html            home page / product directory
  - blog/index.html       list of all product reviews
  - blog/<slug>/index.html  one SEO page per product
  - sitemap.xml, robots.txt

Run:  py -X utf8 _build/build_site.py
Inputs: products.tsv (name<TAB>link), facts.json (from sales pages), content.py (category copy).
"""
import html, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_home import CATEGORY, CAT_ORDER, CAT_ICON, DEFAULT_CAT, load, slug  # noqa: E402
from content import CATEGORY_COPY, OVERRIDES, FULL_REVIEWS, DISABLED  # noqa: E402

SITE = os.path.join(os.path.dirname(HERE), "medipicker.com")
DOMAIN = "https://medipicker.com"
TODAY = "2026-10-15"
TODAY_TXT = "October 15, 2026"
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
        items.append(p)
    return items


def seo(p):
    n, c = p["name"], CATEGORY_COPY[p["cat"]]
    f = p["facts"]
    title = f"{n} Review 2026: Ingredients, Price & Where to Buy"
    if len(title) + len(" | MediPicker") <= 72:
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
  <meta name="keywords" content="{kws}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
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
        <a href="{root}privacy-policy">Privacy Policy</a>
        <a href="{root}terms">Terms</a>
        <a href="{root}disclaimer">Disclaimer</a>
      </nav>
    </div>
    <p class="disclaimer">We may earn a commission when you buy through links on this site, at no extra cost to you.</p>
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
</body>
</html>
"""


def buy(p, label="Buy Now", cls="btn btn-buy"):
    return f'<a class="{cls}" href="{e(p["link"])}" rel="sponsored nofollow noopener" target="_blank">{label}</a>'


def faq_items(p):
    n, c, f = p["name"], CATEGORY_COPY[p["cat"]], p["facts"]
    qa = [(f"What is {n}?", f"{n} is a {c['noun']} designed to {c['purpose']}. It is sold through its official website.")]
    if f.get("prices"):
        lo, hi = min(f["prices"]), max(f["prices"])
        price = (f"On the official website {n} costs ${lo} per bottle." if lo == hi else
                 f"On the official website {n} costs between ${lo} and ${hi} per bottle, depending on how many bottles you buy. Larger packages have the lowest price per bottle.")
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


def product_page(p, by_cat):
    n, c, f = p["name"], CATEGORY_COPY[p["cat"]], p["facts"]
    root = "../../"
    url = f"{DOMAIN}/blog/{p['slug']}/"
    title, desc, kws = seo(p)
    faqs = faq_items(p)
    lo = min(f["prices"]) if f.get("prices") else None
    hi = max(f["prices"]) if f.get("prices") else None
    g = f.get("guarantee_days")

    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": f"{n} Review 2026: Ingredients, Price & Where to Buy", "description": desc,
         "datePublished": TODAY, "dateModified": TODAY, "mainEntityOfPage": url,
         "author": {"@type": "Organization", "name": "MediPicker Editorial Team", "url": DOMAIN + "/"},
         "publisher": {"@type": "Organization", "name": "MediPicker", "url": DOMAIN + "/"}, "inLanguage": "en-US"},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "MediPicker", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": "Reviews", "item": DOMAIN + "/blog/"},
            {"@type": "ListItem", "position": 3, "name": f"{n} Review", "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
    ]}
    # Google rejects Product markup that has no offers/review/rating, so only emit it when we know real prices.
    if p["cat"] != "Home & Lifestyle" and lo:
        ld["@graph"].append({
            "@type": "Product", "name": n, "category": "Dietary Supplement" if p["cat"] != "Pets" else "Pet Supplement",
            "description": f"{n} is a {c['noun']} designed to {c['purpose']}.",
            "offers": {"@type": "AggregateOffer", "priceCurrency": "USD", "lowPrice": str(lo), "highPrice": str(hi),
                       "offerCount": str(len(f["prices"])), "availability": "https://schema.org/InStock", "url": url}})

    facts_rows = [("Category", e(p["cat"]))]
    if f.get("form"):
        facts_rows.append(("Form", e(f["form"].capitalize())))
    facts_rows.append(("Price", f"From ${lo} per bottle" if lo else "See official website"))
    facts_rows.append(("Guarantee", f"{g}-day money-back guarantee" if g else "See official website"))
    if f.get("one_time"):
        facts_rows.append(("Billing", "One-time payment"))
    if f.get("free_shipping"):
        facts_rows.append(("Shipping", "Free shipping on some packages"))
    facts_rows.append(("Where to buy", f'<a href="{e(p["link"])}" rel="sponsored nofollow noopener" target="_blank">Official {e(n)} website</a>'))
    facts_html = "\n".join(f"          <div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in facts_rows)

    if f.get("ingredients"):
        ing_html = ("        <p>These ingredients are named on the official website:</p>\n        <ul class=\"ing-list\">\n"
                    + "\n".join(f"          <li>{e(nice(i))}</li>" for i in f["ingredients"])
                    + "\n        </ul>\n        <p>Exact amounts aren't always shown on the sales page, so check the supplement facts label on your bottle for the complete formula.</p>")
    else:
        ing_html = (f"        <p>The official website doesn't list its full ingredients in text form. Check the product label or the official website for the complete formula and amounts before you buy, especially if you have allergies or take medication.</p>")

    if lo:
        price_p = (f"On the official website, {e(n)} costs <strong>${lo} per bottle</strong>." if lo == hi else
                   f"On the official website, {e(n)} costs between <strong>${lo} and ${hi} per bottle</strong>, depending on the package. Buying more bottles at once lowers the price per bottle, which is why multi-bottle packages are the most popular.")
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

    related = [q for q in by_cat[p["cat"]] if q is not p][:4]
    related_html = ""
    if related:
        related_html = ('      <section class="related" aria-labelledby="rel-h">\n        <h2 id="rel-h">More ' + e(p["cat"]) + ' Reviews</h2>\n        <ul>\n'
                        + "\n".join(f'          <li><a href="../{q["slug"]}/">{e(q["name"])} Review</a></li>' for q in related)
                        + "\n        </ul>\n      </section>\n")

    safety_html = "\n".join(f"          <li>{e(s)}</li>" for s in c["safety"])
    fit_html = "\n".join(f"          <li>{e(s)}</li>" for s in c["fit"])
    faq_html = "\n".join(f"          <details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faqs)

    ing_section = "" if p["cat"] == "Home & Lifestyle" else f'''
      <h2>{e(n)} Ingredients</h2>
{ing_html}
'''
    safety_title = "Things to Know Before You Buy" if p["cat"] == "Home & Lifestyle" else f"Is {e(n)} Safe? Side Effects to Know"

    body = f'''<main id="main" class="post">
  <div class="container post-wrap">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{root}">MediPicker</a> <span aria-hidden="true">&rsaquo;</span> <a href="{root}blog/">Reviews</a> <span aria-hidden="true">&rsaquo;</span> <span>{e(n)}</span></nav>
    <article>
      <span class="rc-tag">{e(p["cat"])}</span>
      <h1>{e(n)} Review 2026: Ingredients, Price &amp; Where to Buy</h1>
      <p class="byline">By <strong>MediPicker Editorial Team</strong> &middot; Updated <time datetime="{TODAY}">{TODAY_TXT}</time></p>
      <p class="lede"><strong>{e(n)}</strong> is a {e(c["noun"])} designed to {e(c["purpose"])}.* In this review we cover what it is, the ingredients named on its official website, the current price, the money-back guarantee and how to buy it safely.</p>
      <p>{buy(p, "Buy " + e(n) + " Now", "btn btn-buy btn-lg")}</p>

      <div class="facts-box">
        <h2 class="facts-title">{e(n)} Quick Facts</h2>
        <dl>
{facts_html}
        </dl>
      </div>

{review_callout}      <h2>What Is {e(n)}?</h2>
      <p>{e(n)} is a {e(c["noun"])} sold through its official website. {e(c["intro"])}</p>

      <h2>How Does {e(n)} Work?</h2>
      <p>{e(c["how"])} As with any {e(c["noun"])}, results vary from person to person.</p>
{ing_section}
      <h2>{e(n)} Price &amp; Money-Back Guarantee</h2>
      <p>{price_p}</p>
      <p>{guar_p}</p>
      <p>{buy(p, "Check the Current Price")}</p>

      <h2>{safety_title}</h2>
      <ul class="check-list warn">
{safety_html}
      </ul>

      <h2>Who Is {e(n)} For?</h2>
      <ul class="check-list">
{fit_html}
      </ul>

      <h2>Where to Buy {e(n)}</h2>
      <p>The best place to buy {e(n)} is the official website. Ordering there means you get the genuine product, the current package prices and the maker's money-back guarantee. Be careful with look-alike websites and third-party marketplace listings, which may not offer the same protection.</p>
      <div class="buy-box">
        <div>
          <strong>{e(n)}</strong>
          <span>{("From $" + str(lo) + " per bottle") if lo else "See current prices"}{(" &middot; " + str(g) + "-day guarantee") if g else ""}</span>
        </div>
        {buy(p, "Buy " + e(n) + " from the Official Website", "btn btn-buy")}
      </div>

      <h2>{e(n)} FAQ</h2>
      <div class="faq">
{faq_html}
      </div>

{related_html}    </article>
  </div>
</main>
'''
    ld_txt = json.dumps(ld, ensure_ascii=False, indent=2)
    return (HEAD.format(title=e(title), desc=e(desc), kws=e(kws), url=url, ogtype="article", root=root, ld=ld_txt)
            + body + FOOT.format(root=root, year=YEAR))


def blog_index(items, cats):
    root = "../"
    url = f"{DOMAIN}/blog/"
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Health Product Reviews", "url": url,
          "hasPart": [{"@type": "Article", "headline": f"{p['name']} Review", "url": f"{DOMAIN}/blog/{p['slug']}/"} for p in items]}
    groups = []
    for c in cats:
        lis = "\n".join(f'        <li><a href="{p["slug"]}/">{e(p["name"])} Review</a></li>' for p in items if p["cat"] == c)
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
    return (HEAD.format(title="Health Product Reviews: Ingredients, Prices &amp; Where to Buy | MediPicker",
                        desc=e(f"Read {len(items)} health supplement reviews: ingredients, prices, money-back guarantees and where to buy each product from its official website."),
                        kws="supplement reviews, health product reviews, weight loss supplement reviews, blood sugar supplement reviews",
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
            <h3><a href="blog/{p["slug"]}/">{e(p["name"])}</a></h3>
            <span class="p-cat">{e(p["cat"])}</span>
          </div>
        </div>
        <div class="p-actions">
          <a class="btn btn-buy" href="{e(p["link"])}" rel="sponsored nofollow noopener" target="_blank">Buy Now<span class="sr-only"> {e(p["name"])}</span></a>
          <a class="link-review" href="blog/{p["slug"]}/">Read review</a>
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
                 "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": p["name"], "url": f"{DOMAIN}/blog/{p['slug']}/"} for i, p in enumerate(items)]}
    site_ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Organization", "@id": DOMAIN + "/#org", "name": "MediPicker", "url": DOMAIN + "/", "logo": DOMAIN + "/favicon.svg"},
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
    for p in items:
        write(os.path.join(SITE, "blog", p["slug"], "index.html"), product_page(p, by_cat))

    urls = ["/", "/blog/"] + [f"/blog/{p['slug']}/" for p in items] + ["/privacy-policy", "/terms", "/disclaimer"]
    write(os.path.join(SITE, "sitemap.xml"),
          '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url>\n    <loc>{DOMAIN}{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>\n" for u in urls) + "</urlset>\n")
    write(os.path.join(SITE, "robots.txt"), f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")

    titles = [seo(p) for p in items]
    print(f"{len(items)} products, {len(cats)} categories, {len(urls)} URLs in sitemap")
    print("longest title:", max(len(t) for t, _, _ in titles), "| longest description:", max(len(d) for _, d, _ in titles))
    print("disabled:", ", ".join(DISABLED))


if __name__ == "__main__":
    main()
