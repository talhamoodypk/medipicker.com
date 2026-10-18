"""Render PNG images for a product page from a graphics file's <defs> (bottle + seal symbols) using headless Edge.

usage: make_images.py <graphics-or-page> <outdir> <workdir> <Product Name> <slug> <guarantee-days> <bg> <bar> <accent> <ink>
"""
import io, os, re, subprocess, sys

page, outdir, work, product = sys.argv[1:5]
slug = sys.argv[5] if len(sys.argv) > 5 else product.lower().replace(" ", "-")
days = sys.argv[6] if len(sys.argv) > 6 else "180"
bg = sys.argv[7] if len(sys.argv) > 7 else "#fbf7e4"
bar = sys.argv[8] if len(sys.argv) > 8 else "#299618"
accent = sys.argv[9] if len(sys.argv) > 9 else "#1d6e10"
ink = sys.argv[10] if len(sys.argv) > 10 else "#232323"
font_url = sys.argv[11] if len(sys.argv) > 11 else "Jost:wght@400;500;600;700;800"
font_css = sys.argv[12] if len(sys.argv) > 12 else "Jost"
edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

src = io.open(page, encoding="utf-8").read()
defs = re.search(r"(?s)<defs>.*?</defs>", src).group(0)
os.makedirs(outdir, exist_ok=True)
os.makedirs(work, exist_ok=True)

base = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family={font_url}&display=swap" rel="stylesheet">
<style>html,body{{margin:0;width:{w}px;height:{h}px;overflow:hidden;font-family:{font_css},Arial,sans-serif}}{css}</style></head>
<body><svg width="0" height="0" style="position:absolute">{defs}</svg>{body}</body></html>"""

B = '<svg viewBox="0 0 220 300" style="{s}"><use href="#bottle"/></svg>'
S = '<svg viewBox="0 0 200 200" style="{s}"><use href="#seal"/></svg>'

jobs = {
  f"{slug}-bottle.png": (800, 900,
    f"body{{background:{bg};display:flex;align-items:center;justify-content:center;position:relative}}",
    B.format(s="width:560px;filter:drop-shadow(0 30px 30px rgba(0,0,0,.22))")
    + S.format(s="position:absolute;top:40px;right:40px;width:250px;transform:rotate(8deg)")),
  f"buy-{slug}-6-bottles.png": (1000, 480,
    f"body{{background:{bg};display:flex;align-items:flex-end;justify-content:center;padding-bottom:30px;box-sizing:border-box}}",
    "".join(B.format(s=f"width:{w}px;flex:none;margin:0 -14px;filter:drop-shadow(0 18px 18px rgba(0,0,0,.18));position:relative;z-index:{z}")
            for w, z in [(150, 1), (175, 2), (205, 3), (205, 3), (175, 2), (150, 1)])),
  f"{slug}-{days}-day-money-back-guarantee.png": (600, 600,
    "body{background:#ffffff;display:flex;align-items:center;justify-content:center}",
    S.format(s="width:520px")),
  "og-image.png": (1200, 630,
    f"body{{background:{bg};display:flex;align-items:center;gap:40px;padding:0 70px;box-sizing:border-box;position:relative}}"
    f".bar{{position:absolute;left:0;right:0;top:0;height:22px;background:{bar}}}"
    f"h1{{font-family:{font_css},Arial,sans-serif;font-weight:800;font-size:70px;line-height:1.05;margin:0 0 18px;color:{ink}}}"
    f"p{{font-size:34px;margin:0 0 26px;color:{accent};font-weight:600}}"
    f".pill{{display:inline-block;background:{accent};color:#fff;font-size:28px;font-weight:700;padding:14px 30px;border-radius:999px}}"
    f".brand{{font-size:26px;font-weight:800;color:{bar};margin-bottom:14px;letter-spacing:.04em}}",
    '<div class="bar"></div>'
    + B.format(s="width:340px;flex:none;filter:drop-shadow(0 24px 24px rgba(0,0,0,.22))")
    + f'<div><div class="brand">INDEPENDENT REVIEW</div><h1>{product} Reviews 2026</h1>'
      f'<p>Ingredients, price &amp; where to buy</p><span class="pill">{days}-Day Money-Back Guarantee</span></div>'),
}

for name, (w, h, css, body) in jobs.items():
    html_path = os.path.join(work, name.replace(".png", ".html"))
    io.open(html_path, "w", encoding="utf-8").write(base.format(w=w, h=h, css=css, defs=defs, body=body, font_url=font_url, font_css=font_css))
    out = os.path.join(outdir, name)
    for attempt in range(3):
        subprocess.run([edge, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        f"--window-size={w},{h}", "--virtual-time-budget=4000", f"--screenshot={out}",
                        "file:///" + html_path.replace("\\", "/")], capture_output=True, timeout=90)
        if os.path.exists(out):
            break
    print(name, os.path.getsize(out) if os.path.exists(out) else "FAILED", "bytes")
