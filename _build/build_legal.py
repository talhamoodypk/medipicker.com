"""Build privacy-policy.html, terms.html and disclaimer.html for the MediPure home site."""
import io, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HEAD = '''<!doctype html>
<html lang="en-US">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | MediPure</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="https://medipure.com/{file}">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
<header class="site-header">
  <div class="container nav">
    <a href="index.html" class="logo">Medi<span>Pure</span></a>
    <nav class="nav-links" aria-label="Main"><a href="index.html#products">All Products</a></nav>
  </div>
</header>
<main class="legal">
  <div class="container">
    <article>
      <h1>{title}</h1>
      <p><em>Last updated: October 15, 2026</em></p>
{body}
      <p><a href="index.html">&larr; Back to MediPure</a></p>
    </article>
  </div>
</main>
<footer class="site-footer">
  <div class="container">
    <nav class="footer-links" aria-label="Footer">
      <a href="index.html">Home</a>
      <a href="privacy-policy.html">Privacy Policy</a>
      <a href="terms.html">Terms</a>
      <a href="disclaimer.html">Disclaimer</a>
    </nav>
    <p class="copyright" style="margin-top:16px">&copy; 2026 MediPure. All rights reserved.</p>
  </div>
</footer>
</body>
</html>
'''

PAGES = {
"privacy-policy.html": ("Privacy Policy", "How MediPure handles information when you visit medipure.com.", '''
      <p>This Privacy Policy explains how MediPure ("we", "us") handles information when you visit medipure.com and its review pages.</p>
      <h2>Information we collect</h2>
      <p>We don't ask you to create an account or submit personal information. Our hosting provider may automatically log basic technical data such as your IP address, browser type and the pages you visit, which is used only to keep the site secure and working.</p>
      <h2>Cookies</h2>
      <p>We don't set advertising cookies. Fonts are loaded from Google Fonts, which may receive your IP address when a page loads.</p>
      <h2>Links to other websites</h2>
      <p>Buy Now buttons take you to the official websites of the products listed. Those websites and their payment processors have their own privacy policies, which apply to any information you give them — including payment details. We never see or store your payment information.</p>
      <h2>Children</h2>
      <p>This website is intended for adults and is not directed at children under 18.</p>
      <h2>Changes</h2>
      <p>We may update this policy from time to time. The date at the top shows when it was last changed.</p>'''),
"terms.html": ("Terms &amp; Conditions", "Terms of use for medipure.com.", '''
      <p>By using medipure.com you agree to these terms. If you don't agree, please don't use this website.</p>
      <h2>Use of content</h2>
      <p>All text and graphics on this website are owned by MediPure unless stated otherwise. You may share links to our pages, but you may not copy or republish our content without permission.</p>
      <h2>No warranties</h2>
      <p>This website is provided "as is". We work to keep product information accurate, but prices, ingredients and offers can change at any time. Always confirm details on the product's official website before you buy.</p>
      <h2>Purchases</h2>
      <p>We don't sell any of the products listed. Orders are placed on each product's official website, whose terms, shipping and refund policies apply to your purchase. Questions about an order or refund should go to that seller.</p>
      <h2>Limitation of liability</h2>
      <p>To the fullest extent allowed by law, MediPure is not liable for any loss or damage arising from your use of this website or of any product you buy from another website.</p>
      <h2>Changes</h2>
      <p>We may update these terms at any time. Continued use of the website means you accept the updated terms.</p>'''),
"disclaimer.html": ("Disclaimer", "Medical and FDA disclaimer for medipure.com.", '''
      <h2>Not medical advice</h2>
      <p>The content on medipure.com is for general information and education only. It is not medical advice and is not a substitute for advice from a doctor or other qualified health professional. Always talk to your doctor before starting any supplement, especially if you are pregnant, nursing, taking medication or have a medical condition.</p>
      <h2>FDA statement</h2>
      <p>Statements on this website have not been evaluated by the Food and Drug Administration. The products listed are not intended to diagnose, treat, cure or prevent any disease. The FDA does not approve dietary supplements.</p>
      <h2>Results vary</h2>
      <p>Individual results with any product vary. Descriptions of possible benefits are based on information from the product makers and research into individual ingredients.</p>
      <h2>Commissions</h2>
      <p>MediPure is independent and is not the maker or seller of the products listed. We may earn a commission when you buy through links on this site, at no extra cost to you.</p>
      <h2>Trademarks</h2>
      <p>Product names are trademarks of their respective owners. Their mention on this website does not imply endorsement.</p>'''),
}

for f, (t, d, b) in PAGES.items():
    io.open(os.path.join(ROOT, f), "w", encoding="utf-8", newline="\n").write(HEAD.format(title=t, desc=d, file=f, body=b.strip("\n")))

io.open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8", newline="\n").write(
    "User-agent: *\nAllow: /\nDisallow: /_build/\n\nSitemap: https://medipure.com/sitemap.xml\n")
urls = ["", "privacy-policy.html", "terms.html", "disclaimer.html"]
io.open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url>\n    <loc>https://medipure.com/{u}</loc>\n    <lastmod>2026-10-15</lastmod>\n  </url>\n" for u in urls)
    + "</urlset>\n")
io.open(os.path.join(ROOT, "favicon.svg"), "w", encoding="utf-8", newline="\n").write(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#299618"/>'
    '<path d="M32 12c-14 9-17 25-7 38 12-3 19-18 7-38z" fill="#d4f7a8"/><path d="M32 12c14 9 17 25 7 38-12-3-19-18-7-38z" fill="#f5b700"/></svg>\n')
print("ok")
