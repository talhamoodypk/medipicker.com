"""Build page images from the vendor's REAL product photos (see memory: real-product-images).

usage: make_real_images.py <outdir> <workdir> "<Product>" <slug> <guarantee-days> <hero-photo> <bundle-photo>
                           <bg> <bar> <accent> <ink> <seal-c0> <seal-c1> <seal-c2> <font_url> <font_css>
Writes <slug>-bottle.png (800x900), buy-<slug>-6-bottles.png (1000x480),
<slug>-<days>-day-money-back-guarantee.png (600x600) and og-image.png (1200x630) by rendering HTML in headless Edge.
"""
import base64, io, os, re, subprocess, sys

(outdir, work, product, slug, days, hero, bundle, bg, bar, accent, ink,
 c0, c1, c2, font_url, font_css) = sys.argv[1:17]
edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
here = os.path.dirname(os.path.abspath(__file__))
os.makedirs(outdir, exist_ok=True)
os.makedirs(work, exist_ok=True)

seal_path = re.search(r'<path d="M100\.0 4\.0[^"]*"', io.open(os.path.join(here, "alphafuelpro-graphics.svg"), encoding="utf-8").read()).group(0)


def uri(p):
    # trim transparent margins so the product fills the frame
    from PIL import Image
    im = Image.open(p).convert("RGBA")
    box = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
    if box:
        im = im.crop(box)
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def t(y, size, w, txt, ln):
    return (f'<text x="100" y="{y}" text-anchor="middle" font-family="{font_css}, Arial, sans-serif" font-weight="{w}" '
            f'font-size="{size}" fill="{ink}" textLength="{ln}" lengthAdjust="spacingAndGlyphs">{txt}</text>')


SEAL = (f'<svg viewBox="0 0 200 200" style="{{s}}"><defs><radialGradient id="g" cx=".5" cy=".4" r=".6">'
        f'<stop offset="0" stop-color="{c0}"/><stop offset=".7" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></radialGradient></defs>'
        f'{seal_path} fill="url(#g)"/><circle cx="100" cy="100" r="70" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="3" stroke-dasharray="4 5"/>'
        + t(88, 30, 800, f"{days}-DAY", 100) + t(113, 19, 700, "MONEY-BACK", 112) + t(137, 19, 700, "GUARANTEE", 104) + "</svg>")

base = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family={font_url}&display=swap" rel="stylesheet">
<style>html,body{{margin:0;width:{w}px;height:{h}px;overflow:hidden;font-family:{font_css},Arial,sans-serif}}
img.p{{object-fit:contain;filter:drop-shadow(0 22px 22px rgba(0,0,0,.18))}}{css}</style></head><body>{body}</body></html>"""

H, B = uri(hero), uri(bundle)
jobs = {
    f"{slug}-bottle.png": (800, 900, f"body{{background:{bg};position:relative;display:flex;align-items:center;justify-content:center}}",
                           f'<img class="p" src="{H}" style="width:640px;height:720px">'
                           + SEAL.format(s="position:absolute;top:34px;right:34px;width:230px;transform:rotate(8deg)")),
    f"buy-{slug}-6-bottles.png": (1000, 480, f"body{{background:{bg};display:flex;align-items:center;justify-content:center}}",
                                  f'<img class="p" src="{B}" style="width:920px;height:430px">'),
    f"{slug}-{days}-day-money-back-guarantee.png": (600, 600, "body{background:#fff;display:flex;align-items:center;justify-content:center}",
                                                     SEAL.format(s="width:520px")),
    "og-image.png": (1200, 630,
                     f"body{{background:{bg};display:flex;align-items:center;gap:40px;padding:0 60px;box-sizing:border-box;position:relative}}"
                     f".bar{{position:absolute;left:0;right:0;top:0;height:22px;background:{bar}}}"
                     f"h1{{font-weight:800;font-size:68px;line-height:1.05;margin:0 0 18px;color:{ink}}}"
                     f"p{{font-size:34px;margin:0 0 26px;color:{accent};font-weight:600}}"
                     f".pill{{display:inline-block;background:{accent};color:#fff;font-size:28px;font-weight:700;padding:14px 30px;border-radius:999px}}"
                     f".brand{{font-size:26px;font-weight:800;color:{bar};margin-bottom:14px;letter-spacing:.04em}}",
                     f'<div class="bar"></div><img class="p" src="{H}" style="width:420px;height:520px;flex:none">'
                     f'<div><div class="brand">INDEPENDENT REVIEW</div><h1>{product} Reviews 2026</h1>'
                     f'<p>Ingredients, price &amp; where to buy</p><span class="pill">{days}-Day Money-Back Guarantee</span></div>'),
}

for name, (w, h, css, body) in jobs.items():
    html_path = os.path.join(work, name.replace(".png", ".html"))
    io.open(html_path, "w", encoding="utf-8").write(base.format(w=w, h=h, css=css, body=body, font_url=font_url, font_css=font_css))
    out = os.path.join(outdir, name)
    if os.path.exists(out):
        os.remove(out)
    for _ in range(3):
        subprocess.run([edge, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        f"--window-size={w},{h}", "--virtual-time-budget=5000", f"--screenshot={out}",
                        "file:///" + html_path.replace("\\", "/")], capture_output=True, timeout=90)
        if os.path.exists(out):
            break
    print(name, os.path.getsize(out) if os.path.exists(out) else "FAILED", "bytes")
