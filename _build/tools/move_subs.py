"""Move every <sub>.medipicker.com review into medipicker.com/reviews/<sub>/ (one-off, 10 Nov 2026).

- git mv the folder, drop the sub-site-only files (functions, legal pages, robots, sitemap, IndexNow key)
- rewrite URLs to https://medipicker.com/reviews/<sub>/ and point legal links at the main site
- add the money disclosure under the header
- reviews rated 2.0/5 or lower: keep one neutral "Official website" link, remove the other buy buttons
- leave <sub>.medipicker.com/ with only a _redirects file (301 everything to the new folder)
"""
import io, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from ratings import SUB

ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DEST = os.path.join(ROOT, "medipicker.com", "reviews")
DROP = ["functions", "_routes.json", "_headers", "robots.txt", "sitemap.xml",
        "privacy-policy.html", "terms.html", "disclaimer.html"]
DISCLOSURE = ('<p class="mp-disclosure">MediPicker may earn money when you buy through links on this page. '
              'Sellers can&rsquo;t pay for a review or a better rating. <a href="/how-we-review#money">How we make money</a></p>\n')
CSS = """
/* MediPicker shared bits */
.mp-disclosure { margin: 0; padding: 8px 16px; background: #f6f7f4; border-bottom: 1px solid #e3e6df; color: #555; font-size: 14px; text-align: center; }
.mp-disclosure a { color: inherit; text-decoration: underline; }
.official-link { font-weight: 600; text-decoration: underline; }
"""
BTN = re.compile(r'<a\b[^>]*class="btn[^"]*"[^>]*rel="[^"]*sponsored[^"]*"[^>]*>.*?</a>', re.S)
INLINE = re.compile(r'<a\b(?![^>]*class=)[^>]*rel="[^"]*sponsored[^"]*"[^>]*>(.*?)</a>', re.S)


def git(*a):
    subprocess.run(["git", *a], cwd=ROOT, check=True)


def low_rated(s, sub):
    """One neutral link (the former 'Visit the official website' button); other buy buttons removed, inline links unlinked."""
    m = re.search(r'<a\b([^>]*)class="btn btn-light[^"]*"([^>]*)>(.*?)</a>', s, re.S)
    href = re.search(r'href="([^"]+)"', m.group(0)).group(1)
    name = re.sub(r"^Visit the |\s*(Official Website|Order Page)$", "", re.sub(r"<[^>]+>", "", m.group(3)).strip())
    keep = (f'<a class="official-link" href="{href}" rel="sponsored nofollow noopener" target="_blank">'
            f'Official {name} website</a>')
    s = s[:m.start()] + "\x00KEEP\x00" + s[m.end():]
    s, nb = BTN.subn("", s)
    s, ni = INLINE.subn(r"\1", s)
    s = s.replace("\x00KEEP\x00", keep)
    # tidy wrappers left empty
    s = re.sub(r'<(p|div)(?:\s+class="[^"]*(?:cta|btn|action|buy|order)[^"]*")?\s*>\s*</\1>\s*', "", s)
    print(f"   low rating: removed {nb} buttons, unlinked {ni} inline links")
    return s


for sub, score in SUB.items():
    src = os.path.join(ROOT, f"{sub}.medipicker.com")
    dst = os.path.join(DEST, sub)
    if os.path.exists(dst):
        print(sub, "already moved"); continue
    os.makedirs(DEST, exist_ok=True)
    git("mv", f"{sub}.medipicker.com", f"medipicker.com/reviews/{sub}")
    for f in DROP + [x for x in os.listdir(dst) if re.fullmatch(r"[0-9a-f]{32}\.txt", x)]:
        if os.path.exists(os.path.join(dst, f)):
            git("rm", "-r", "-q", "-f", f"medipicker.com/reviews/{sub}/{f}")

    path = os.path.join(dst, "index.html")
    s = io.open(path, encoding="utf-8").read()
    new = f"https://medipicker.com/reviews/{sub}/"
    s = s.replace(f"https://{sub}.medipicker.com/", new).replace(f"https://{sub}.medipicker.com", new.rstrip("/"))
    s = s.replace('<a href="/">Home</a>', '<a href="/">MediPicker Home</a>\n      <a href="/blog/">All Reviews</a>')
    s = s.replace('href="/"', 'href="./"').replace('<a href="./">MediPicker Home</a>', '<a href="/">MediPicker Home</a>')
    for leg in ("privacy-policy", "disclaimer", "terms"):
        s = s.replace(f'href="{leg}"', f'href="/{leg}"')
    s = s.replace('<a href="/terms">Terms &amp; Conditions</a>',
                  '<a href="/terms">Terms &amp; Conditions</a>\n      <a href="/about">About MediPicker</a>\n      <a href="/how-we-review">How We Review</a>\n      <a href="/contact">Contact</a>')
    s = re.sub(r'<meta name="msvalidate\.01"[^>]*>\s*', "", s)
    if "mp-disclosure" not in s:
        s = re.sub(r"(</header>\s*)", lambda m: m.group(1) + DISCLOSURE, s, count=1)
    if score <= 2.0:
        s = low_rated(s, sub)
    assert f"{sub}.medipicker.com" not in s, sub
    io.open(path, "w", encoding="utf-8", newline="").write(s)

    css = os.path.join(dst, "styles.css")
    c = io.open(css, encoding="utf-8").read()
    if "mp-disclosure" not in c:
        io.open(css, "a", encoding="utf-8", newline="").write(CSS)

    # old sub-site: redirects only
    os.makedirs(src, exist_ok=True)
    io.open(os.path.join(src, "_redirects"), "w", encoding="utf-8", newline="\n").write(
        "# This review moved to medipicker.com/reviews/ on 10 Nov 2026.\n"
        + "".join(f"/{leg} https://medipicker.com/{leg} 301\n/{leg}.html https://medipicker.com/{leg} 301\n"
                  for leg in ("privacy-policy", "terms", "disclaimer"))
        + f"/images/* {new}images/:splat 301\n/* {new} 301\n")
    git("add", f"{sub}.medipicker.com/_redirects", f"medipicker.com/reviews/{sub}")
    print(sub, score, "moved")
