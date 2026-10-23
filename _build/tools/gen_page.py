"""Build a product subdomain folder (index.html, styles.css, script.js, favicon.svg, functions/) from a content spec.

usage: gen_page.py <spec.py>
The spec module defines P (dict) and S (list of sections built with the helpers below via `from gen_page import *`).
"""
import html, io, json, os, re, runpy, shutil, sys

ROOT = r"D:\Medicne Bing"
TEMPLATE = os.path.join(ROOT, "sugarmute.medipicker.com")
DATE = "2026-10-18"
DATE_TXT = "October 18, 2026"

E = html.escape


def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))


# ---------- section helpers (return dicts) ----------
def sec(id, h2, body, toc=None, bg=None):
    return {"id": id, "h2": h2, "body": body, "toc": toc, "bg": bg}


def prose(*paras, narrow=True):
    inner = "\n".join(p if p.lstrip().startswith("<") else f"<p>{p}</p>" for p in paras)
    return f'<div class="container{" narrow" if narrow else ""} prose reveal">\n{inner}\n</div>'


def h3(t):
    return f"<h3>{t}</h3>"


def ul(*items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def ol(*items):
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


def note(t):
    return f'<p class="note">{t}</p>'


def split(img, alt, *paras, reverse=False, w=800, h=900):
    inner = "\n".join(p if p.lstrip().startswith("<") else f"<p>{p}</p>" for p in paras)
    return (f'<div class="container split{" reverse" if reverse else ""}">\n'
            f'<div class="illus reveal"><img src="images/{img}" width="{w}" height="{h}" loading="lazy" alt="{E(alt)}"></div>\n'
            f'<div class="prose reveal">\n{inner}\n</div>\n</div>')


def steps(items, after=None):
    s = "".join(f'<article class="step reveal"><span class="step-num">{i}</span><h3>{t}</h3><p>{d}</p></article>'
                for i, (t, d) in enumerate(items, 1))
    a = f'<div class="prose narrow" style="margin: 40px auto 0">{"".join(f"<p>{p}</p>" for p in after)}</div>' if after else ""
    return f'<div class="container"><div class="grid-3">{s}</div>{a}</div>'


def table(head, rows, lead=None, after=None, foot=None):
    th = "".join(f'<th scope="col">{c}</th>' for c in head)
    tr = ""
    for r in rows:
        tr += f'<tr><th scope="row">{r[0]}</th>' + "".join(
            f'<td data-label="{E(strip(head[i + 1]))}">{c}</td>' for i, c in enumerate(r[1:])) + "</tr>\n"
    out = '<div class="container">'
    if lead:
        out += f'<p class="lead">{lead}</p>'
    out += f'<div class="table-wrap reveal"><table class="compare"><thead><tr>{th}</tr></thead><tbody>\n{tr}</tbody></table></div>'
    if foot:
        out += f'<p class="center" style="margin-top:20px;color:var(--muted);font-size:16px">{foot}</p>'
    if after:
        out += '<div class="prose narrow" style="margin: 32px auto 0">' + "".join(
            p if p.startswith("<") else f"<p>{p}</p>" for p in after) + "</div>"
    return out + "</div>"


ICONS = {
    "wave": '<path d="M3 12h4l2-6 4 12 2-6h6"/>',
    "circle": '<circle cx="12" cy="12" r="8"/><path d="M8 12h8"/>',
    "heart": '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>',
    "shield": '<path d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5z"/>',
    "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    "leaf": '<path d="M5 19c0-9 6-14 14-14 0 8-5 14-14 14zM5 19l7-7"/>',
    "moon": '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
    "brain": '<path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 2 5 3 3 0 0 0 6 1V5a3 3 0 0 0-3-1zM15 4a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-2 5 3 3 0 0 1-6 1"/>',
    "ear": '<path d="M7 9a5 5 0 0 1 10 0c0 4-4 5-4 8a3 3 0 0 1-6 0"/><path d="M10 9a2 2 0 0 1 4 0"/>',
    "tooth": '<path d="M7 3c-3 0-4 3-3 6l2 11c.3 1.5 2.3 1.5 2.6 0L10 15h4l1.4 5c.3 1.5 2.3 1.5 2.6 0l2-11c1-3 0-6-3-6-2 0-3 1-5 1S9 3 7 3z"/>',
    "cup": '<path d="M5 8h12v6a6 6 0 0 1-12 0zM17 10h2a2 2 0 0 1 0 4h-2M8 3v3M12 3v3"/>',
    "drop": '<path d="M12 3c4 5 6 8 6 11a6 6 0 0 1-12 0c0-3 2-6 6-11z"/>',
}


def benefits(lead, items, cta=None):
    b = "".join(
        f'<article class="benefit reveal"><div class="icon-circle" aria-hidden="true"><svg viewBox="0 0 24 24">{ICONS[ic]}</svg></div>'
        f'<div><h3>{t}</h3><p>{d}</p></div></article>' for ic, t, d in items)
    c = f'<div class="center" style="margin-top:36px">{BTN(cta, "btn-dark btn-lg")}</div>' if cta else ""
    return f'<div class="container"><p class="lead">{lead}</p><div class="grid-2">{b}</div>{c}</div>'


def who(yes_t, yes, no_t, no):
    return (f'<div class="container grid-2"><div class="who who-yes reveal"><h3>{yes_t}</h3>{ul(*yes)}</div>'
            f'<div class="who who-no reveal"><h3>{no_t}</h3>{ul(*no)}</div></div>')


def info(items, before=None, after=None):
    li = "".join(f"<li><strong>{a}</strong> {b}</li>" for a, b in items)
    pre = "".join(f"<p>{p}</p>" for p in (before or []))
    post = "".join(p if p.startswith("<") else f"<p>{p}</p>" for p in (after or []))
    return f'<div class="container narrow">{pre}<ul class="info-list">{li}</ul>{post}</div>'


def review(pros, cons, verdict_h, verdict, cta):
    return (f'<div class="container"><div class="grid-2"><div class="who who-yes reveal"><h3>Pros</h3>{ul(*pros)}</div>'
            f'<div class="who who-no reveal"><h3>Cons</h3>{ul(*cons)}</div></div>'
            f'<div class="verdict reveal"><h3>{verdict_h}</h3>{"".join(f"<p>{p}</p>" for p in verdict)}'
            f'{BTN(cta, "btn-light")}</div></div>')


def pricing(lead, cards, fine):
    out = ""
    for c in cards:
        feat = c.get("featured")
        out += (f'<article class="price-card{" featured" if feat else ""} reveal">'
                + (f'<span class="ribbon">{c["ribbon"]}</span>' if c.get("ribbon") else "")
                + f'<h3>{c["title"]}</h3><p class="supply">{c["supply"]}</p>'
                f'<div class="bottles" aria-hidden="true">{"<i></i>" * c["n"]}</div>'
                f'<p class="price"><span>{c["price"]}</span>/{c.get("unit", "bottle")}</p><p class="was">{c["was"]}</p>'
                f'{ul(*c["list"])}{BTN(c["btn"], ("btn-green" if feat else "btn-dark") + " btn-block")}</article>')
    return f'<div class="container"><p class="lead">{lead}</p><div class="pricing">{out}</div><p class="fineprint">{fine}</p></div>'


def faq_block(items):
    return '<div class="container narrow faq">' + "".join(
        f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items) + "</div>"


def BTN(text, cls):
    return f'<a href="{P["link"]}" class="btn {cls}" rel="sponsored nofollow noopener" target="_blank">{text}</a>'


def LINK(text):
    return f'<a href="{P["link"]}" rel="sponsored nofollow noopener" target="_blank">{text}</a>'


P = {}


def build(spec_path):
    P.clear()  # specs fill the shared P with P.update(...) before building sections
    g = runpy.run_path(spec_path, init_globals={k: v for k, v in globals().items() if not k.startswith("__")})
    S = g["S"]
    host = f'{P["sub"]}.medipicker.com'
    url = f"https://{host}/"
    out = os.path.join(ROOT, host)
    os.makedirs(os.path.join(out, "images"), exist_ok=True)
    os.makedirs(os.path.join(out, "functions"), exist_ok=True)
    name, slug = P["name"], P["slug"]
    c = P["colors"]
    font_css = P["font_css"]

    # styles.css from template with new palette and font
    css = io.open(os.path.join(TEMPLATE, "styles.css"), encoding="utf-8").read()
    root = (":root {\n" + "".join(f"  --{k}: {v};\n" for k, v in [
        ("green", c["main"]), ("green-dark", c["dark"]), ("green-deep", c["deep"]), ("green-soft", c["soft"]),
        ("cream", c["cream"]), ("off", c["off"]), ("gold", c["gold"]), ("gold-dark", c["gold_dark"]),
        ("ink", "#232323"), ("muted", c["muted"]), ("white", "#fff"), ("line", c["line"]), ("radius", "16px"),
        ("shadow", f'0 10px 28px {c["shadow"]}'), ("header-h", "66px")]) + "}")
    css = re.sub(r"(?s):root \{.*?\}", root, css, count=1)
    css = css.replace('font-family: "Jost", system-ui', f"font-family: {font_css}, system-ui")
    css = (css.replace("rgba(255, 225, 69, .40)", c["btn_shadow"]).replace("#453a00", c["btn_ink"])
           .replace("#ffe145", c["gold"]))
    io.open(os.path.join(out, "styles.css"), "w", encoding="utf-8", newline="\n").write(css)
    shutil.copy(os.path.join(TEMPLATE, "script.js"), os.path.join(out, "script.js"))
    io.open(os.path.join(out, "favicon.svg"), "w", encoding="utf-8", newline="\n").write(P["favicon"])
    mw = io.open(os.path.join(TEMPLATE, "functions", "_middleware.js"), encoding="utf-8").read().replace("sugarmute.medipicker.com", host)
    io.open(os.path.join(out, "functions", "_middleware.js"), "w", encoding="utf-8", newline="\n").write(mw)

    # FAQ (single source for schema + page)
    faq = P["faq"]
    sections = S + [sec("faq", f"{name} FAQ", faq_block(faq), toc="FAQ")]
    bgs = ["bg-white", "bg-cream"]
    body_secs = ""
    for i, s in enumerate(sections):
        bg = s["bg"] or bgs[i % 2]
        body_secs += (f'\n<section id="{s["id"]}" aria-labelledby="{s["id"]}-h">\n'
                      f'  <div class="block-bar"><div class="container"><h2 id="{s["id"]}-h">{s["h2"]}</h2></div></div>\n'
                      f'  <div class="block-body {bg}">\n{s["body"]}\n  </div>\n</section>\n')
    toc = "".join(f'<li><a href="#{s["id"]}">{s["toc"]}</a></li>' for s in sections if s["toc"])
    dl = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in P["facts"])
    trust = "".join(
        f'<div class="trust reveal"><svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="19" fill="{c["main"]}"/>'
        f'<g fill="none" stroke="{c["gold"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" transform="translate(8 8)">{ICONS[ic]}</g></svg><span>{t}</span></div>'
        for ic, t in P["trust"])
    hero_p = "".join(f"<p>{p}</p>" for p in P["intro"])
    checks = "".join(f"<li>{x}</li>" for x in P["checks"])
    nav = "".join(f'<a href="#{a}">{b}</a>' for a, b in P["nav"])
    cta = P["cta"]

    page_body = f"""<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header" id="top">
  <div class="container nav">
    <a href="/" class="logo">{name} <span>Reviews</span></a>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="nav-menu"><span></span><span></span><span></span></button>
    <nav id="nav-menu" class="nav-menu" aria-label="Main">
      {nav}
      {BTN("Buy " + name, "btn-dark btn-sm")}
    </nav>
  </div>
</header>

<main id="main">
<section class="hero">
  <div class="container">
    <h1>{P["h1"]}</h1>
    <p class="tagline">{P["tagline"]}</p>
    <p class="byline">By <strong>{name} Review Team</strong> · Updated <time datetime="{DATE}">{DATE_TXT}</time> · READTIME min read</p>
    <div class="hero-grid">
      <div class="hero-media reveal"><img class="hero-img" src="images/{slug}-bottle.png" width="800" height="900" fetchpriority="high" alt="{E(P["hero_alt"])}"></div>
      <div class="hero-copy reveal">
        {hero_p}
        <ul class="checks">{checks}</ul>
        <div class="hero-actions">
          {BTN("Buy " + name, "btn-dark btn-lg")}
          <a href="#price" class="btn btn-ghost">See Prices</a>
        </div>
      </div>
    </div>
    <div class="trust-row">{trust}</div>
  </div>
</section>

<section aria-labelledby="glance-h">
  <div class="block-bar"><div class="container"><h2 id="glance-h">{name} at a Glance</h2></div></div>
  <div class="block-body bg-off">
    <div class="container glance-grid">
      <div class="card glance reveal">
        <h3>Product Facts</h3>
        <dl>{dl}</dl>
      </div>
      <nav class="card toc reveal" aria-label="Table of contents">
        <h3>In This Review</h3>
        <ol>{toc}</ol>
      </nav>
    </div>
  </div>
</section>
{body_secs}
<section class="cta-final" aria-labelledby="cta-h">
  <div class="container reveal">
    <h2 id="cta-h">{cta["h2"]}</h2>
    <img class="cta-img" src="images/buy-{slug}-6-bottles.png" width="1000" height="480" loading="lazy" alt="{E(cta["alt"])}">
    <p>{cta["text"]}</p>
    {BTN(cta["btn"], "btn-dark btn-lg")}
  </div>
</section>
</main>

<footer class="site-footer">
  <div class="container">
    <nav class="footer-links" aria-label="Footer">
      <a href="/">Home</a>{"".join(f'<a href="#{a}">{b}</a>' for a, b in P["footer_links"])}
      <a href="privacy-policy">Privacy Policy</a><a href="disclaimer">Disclaimer</a><a href="terms">Terms &amp; Conditions</a>
    </nav>
    <p class="disclaimer"><strong>About this site:</strong> This is an independent review website. It is not the manufacturer or seller of {name}. {name} is a trademark of its respective owner.</p>
    <p class="disclaimer">*These statements have not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure or prevent any disease. The information on this page is for general education and is not a substitute for advice from a qualified medical professional. Talk to your doctor before using any supplement, especially if you take medication or have a medical condition. Individual results may vary.</p>
    <p class="copyright">Contact: <a href="mailto:info@medipicker.com" style="color:inherit">info@medipicker.com</a></p>
    <p class="copyright">© <span id="year">2026</span> {name} Reviews. All rights reserved.</p>
  </div>
</footer>
<a href="#top" class="to-top" aria-label="Back to top">↑</a>
<script src="script.js"></script>
</body>
</html>
"""
    text = strip(re.sub(r"(?is)<(script|style|svg)[^>]*>.*?</\1>", " ", page_body))
    words = len(re.findall(r"[A-Za-z0-9'$]+", text))
    page_body = page_body.replace("READTIME", str(max(1, round(words / 200))))

    title = strip(P["title"])
    graph = [
        {"@type": "Organization", "@id": url + "#org", "name": f"{name} Reviews", "url": url},
        {"@type": "WebSite", "@id": url + "#website", "url": url, "name": f"{name} Reviews", "publisher": {"@id": url + "#org"}, "inLanguage": "en-US"},
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "isPartOf": {"@id": url + "#website"},
         "primaryImageOfPage": f"{url}images/{slug}-bottle.png", "datePublished": DATE, "dateModified": DATE, "inLanguage": "en-US"},
        {"@type": "Article", "@id": url + "#article", "headline": title, "description": P["article_desc"], "image": url + "images/og-image.png",
         "datePublished": DATE, "dateModified": DATE, "author": {"@type": "Organization", "name": f"{name} Review Team", "url": url},
         "publisher": {"@id": url + "#org"}, "mainEntityOfPage": {"@id": url + "#webpage"}, "about": {"@id": url + "#product"}, "inLanguage": "en-US"},
        {"@type": "Product", "@id": url + "#product", "name": name, "alternateName": P["alt_names"], "image": f"{url}images/{slug}-bottle.png",
         "description": P["product_desc"], "category": "Dietary Supplement",
         "offers": {"@type": "AggregateOffer", "priceCurrency": P.get("currency", "USD"), "lowPrice": P["low"], "highPrice": P["high"], "offerCount": "3",
                    "availability": "https://schema.org/InStock", "url": url + "#price"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faq]},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    head = f"""<!doctype html>
<html lang="en-US">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="msvalidate.01" content="64C7E7CA4E419E5A46C42493F8ECE607" />
  <title>{P["title"]}</title>
  <meta name="description" content="{E(P["desc"])}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="{name} Reviews">
  <meta property="og:title" content="{E(P["og_title"])}">
  <meta property="og:description" content="{E(P["og_desc"])}">
  <meta property="og:url" content="{url}">
  <meta property="og:locale" content="en_US">
  <meta property="og:image" content="{url}images/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{E(name)} reviews 2026">
  <meta property="article:published_time" content="{DATE}">
  <meta property="article:modified_time" content="{DATE}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{E(P["og_title"])}">
  <meta name="twitter:image" content="{url}images/og-image.png">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family={P["font_url"]}&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
  <script type="application/ld+json">
{ld}
  </script>
</head>
"""
    io.open(os.path.join(out, "index.html"), "w", encoding="utf-8", newline="\n").write(head + page_body)
    kw = P.get("kw_re", re.escape(name))
    k = len(re.findall(kw, text, re.I))
    print(f"{host}: {words} words, brand {k} ({k / words * 100:.2f}%), h2 {len(sections) + 3}, faq {len(faq)}")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        build(p)
