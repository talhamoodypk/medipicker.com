"""Turn an in-depth review folder into a standalone product subdomain site.

- Brand with the product name instead of MediPicker (logo, byline, schema, og:site_name, copyright)
- Remove the breadcrumb and any affiliate / commission wording
- Rewrite privacy, disclaimer and terms pages without affiliate / commission wording

usage: py -X utf8 _build/debrand_subdomain.py <folder> "<Product Name>" <subdomain-host>
e.g.   py -X utf8 _build/debrand_subdomain.py gelatinesculpt.medipicker.com "Gelatine Sculpt" gelatinesculpt.medipicker.com
"""
import io, os, re, sys

folder, product, host = sys.argv[1], sys.argv[2], sys.argv[3]
site = f"{product} Reviews"
url = f"https://{host}/"
first, _, rest = product.partition(" ")
logo = f'{first} <span>{rest or "Reviews"}</span>' if rest else f'{first} <span>Reviews</span>'

p = os.path.join(folder, "index.html")
s = io.open(p, encoding="utf-8").read()

# Disclosure bar
s = re.sub(r'\s*<p class="disclosure-bar">.*?</p>', "", s, flags=re.S)
# Breadcrumb (visible)
s = re.sub(r'\s*<nav class="breadcrumb".*?</nav>', "", s, flags=re.S)
# Breadcrumb (schema) and the reference to it
s = re.sub(r',\s*\{\s*"@type": "BreadcrumbList".*?\]\s*\}', "", s, flags=re.S)
s = re.sub(r',\s*"breadcrumb": \{ "@id": "[^"]+" \}', "", s)
# Logo + home links
s = re.sub(r'<a href="https://medipicker\.com/" class="logo">Medi<span>Picker</span></a>', f'<a href="/" class="logo">{logo}</a>', s)
s = s.replace('<a href="https://medipicker.com/">MediPicker Home</a>', '<a href="/">Home</a>')
# Schema organisation / site / author
s = s.replace('"@id": "https://medipicker.com/#org"', f'"@id": "{url}#org"')
s = s.replace('"name": "MediPicker",\n        "url": "https://medipicker.com/"', f'"name": "{site}",\n        "url": "{url}"')
s = re.sub(r'"name": "[^"]* Reviews by MediPicker"', f'"name": "{site}"', s)
s = re.sub(r'"name": "[^"]*Review by MediPicker"', f'"name": "{site}"', s)
s = re.sub(r'"author": \{ "@type": "Organization", "name": "MediPicker Editorial Team", "url": "https://medipicker\.com/" \}',
           f'"author": {{ "@type": "Organization", "name": "{product} Review Team", "url": "{url}" }}', s)
# Visible text
s = s.replace('<meta property="og:site_name" content="MediPicker">', f'<meta property="og:site_name" content="{site}">')
s = s.replace("<strong>MediPicker Editorial Team</strong>", f"<strong>{product} Review Team</strong>")
s = re.sub(r'<p class="disclaimer"><strong>Affiliate disclosure:</strong>.*?</p>',
           f'<p class="disclaimer"><strong>About this site:</strong> This is an independent review website. It is not the manufacturer or seller of {product}. {product} is a trademark of its respective owner.</p>',
           s, flags=re.S)
s = re.sub(r"(©|&copy;) (<span id=\"year\">\d{4}</span>) MediPicker\.", rf"\1 \2 {site}.", s)
s = re.sub(r"\| MediPicker</title>", f"| {site}</title>", s)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

# Legal pages
HEAD = '''<!doctype html>
<html lang="en-US">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | {site}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}{file}">
  <meta name="robots" content="index, follow">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
<header class="site-header">
  <div class="container nav">
    <a href="/" class="logo">{logo}</a>
    <a href="/" class="btn btn-dark btn-sm">{product} Review</a>
  </div>
</header>
<main class="legal">
  <div class="container">
    <article class="card">
      <h1>{title}</h1>
      <p><em>Last updated: October 15, 2026</em></p>
{body}
      <p><a href="/">&larr; Back to the {product} review</a></p>
    </article>
  </div>
</main>
<footer class="site-footer">
  <div class="container">
    <nav class="footer-links" aria-label="Footer">
      <a href="/">{product} Review</a>
      <a href="privacy-policy.html">Privacy Policy</a>
      <a href="disclaimer.html">Disclaimer</a>
      <a href="terms.html">Terms &amp; Conditions</a>
    </nav>
    <p class="copyright">&copy; 2026 {site}. All rights reserved.</p>
  </div>
</footer>
</body>
</html>
'''
P = product
pages = {
"privacy-policy.html": ("Privacy Policy", f"How {site} handles information when you visit {host}.", f'''
      <p>This Privacy Policy explains how {site} ("we", "us") handles information when you visit {host}.</p>
      <h2>Information we collect</h2>
      <p>We don't ask you to create an account or submit personal information. Our hosting provider may automatically log basic technical data such as your IP address, browser type and the pages you visit, which is used only to keep the site secure and working.</p>
      <h2>Cookies</h2>
      <p>We don't set advertising cookies. Fonts are loaded from Google Fonts, which may receive your IP address when a page loads.</p>
      <h2>Links to other websites</h2>
      <p>Buy buttons take you to the official {P} order page. That website and its payment processor have their own privacy policies, which apply to any information you give them, including payment details. We never see or store your payment information.</p>
      <h2>Children</h2>
      <p>This website is intended for adults and is not directed at children under 18.</p>
      <h2>Changes</h2>
      <p>We may update this policy from time to time. The date at the top shows when it was last changed.</p>'''),
"disclaimer.html": ("Disclaimer", f"Medical and FDA disclaimer for the {P} review on {host}.", f'''
      <h2>Not medical advice</h2>
      <p>The content on {host} is for general information and education only. It is not medical advice and is not a substitute for advice from a doctor or other qualified health professional. Always talk to your doctor before starting any supplement, especially if you are pregnant, nursing, taking medication or have a medical condition.</p>
      <h2>FDA statement</h2>
      <p>Statements about {P} on this website have not been evaluated by the Food and Drug Administration. {P} is not intended to diagnose, treat, cure or prevent any disease. The FDA does not approve dietary supplements.</p>
      <h2>Results vary</h2>
      <p>Individual results with {P} vary. Descriptions of possible benefits are based on research into individual ingredients and information from the vendor, not on clinical trials of the finished {P} formula.</p>
      <h2>Independent website</h2>
      <p>This is an independent review website. It is not the manufacturer, vendor or retailer of {P}. {P} is a trademark of its respective owner, and its mention here does not imply endorsement.</p>
      <h2>Accuracy</h2>
      <p>We check prices and product details carefully, but they can change at any time. Always confirm the current price, ingredients and guarantee on the official {P} website before you buy.</p>'''),
"terms.html": ("Terms &amp; Conditions", f"Terms of use for {host}.", f'''
      <p>By using {host} you agree to these terms. If you don't agree, please don't use this website.</p>
      <h2>Use of content</h2>
      <p>All text and graphics on this website are owned by {site} unless stated otherwise. You may share links to our pages, but you may not copy or republish our content without permission.</p>
      <h2>No warranties</h2>
      <p>This website is provided "as is". We work to keep information about {P} accurate and up to date, but we make no guarantees about its completeness or accuracy, and information may change without notice.</p>
      <h2>Purchases</h2>
      <p>We do not sell {P}. Orders are placed on the official {P} website, whose terms, shipping and refund policies apply to your purchase. Questions about an order or refund should go to that seller.</p>
      <h2>Limitation of liability</h2>
      <p>To the fullest extent allowed by law, we are not liable for any loss or damage arising from your use of this website or of any product you buy through links on it.</p>
      <h2>Changes</h2>
      <p>We may update these terms at any time. Continued use of the website means you accept the updated terms.</p>'''),
}
for f, (t, d, b) in pages.items():
    io.open(os.path.join(folder, f), "w", encoding="utf-8", newline="\n").write(
        HEAD.format(title=t, desc=d, url=url, file=f, site=site, logo=logo, product=P, body=b.strip("\n")))

# Report anything left over
for f in os.listdir(folder):
    if f.endswith((".html", ".xml", ".txt", ".js", ".css")):
        t = io.open(os.path.join(folder, f), encoding="utf-8", errors="ignore").read()
        left = re.findall(r"(?i)affiliate|commission|medipicker(?!\.com)|Medi<span>Picker|breadcrumb", t)
        if left:
            print(f, "still has:", sorted(set(x.lower() for x in left)))
print("done")
