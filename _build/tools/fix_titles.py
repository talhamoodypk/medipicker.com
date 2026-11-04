"""Shorten subdomain <title>s to <= 65 characters (Bing 'Title too long'), keeping each page's Bing keyword.

Replaces the old title wherever it appears in the page (title tag, WebPage name, Article headline) and in the spec file.
"""
import glob, html, io, os, re

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
NEW = {
  "alphafuelpro": "AlphaFuel Pro Review 2026: Ingredients, Price & Official Website",
  "arterisplus": "Arteris Plus Reviews 2026: Ingredients, Price & Blood Pressure",
  "biodentex": "BioDentex Reviews 2026: Ingredients, Price & Official Website",
  "cellucare": "CelluCare Reviews 2026: Official Website, Price & Discount",
  "dentavive": "DentaVive Review 2026: Probiotic Strains, Price & What to Know",
  "fastleanpro": "Fast Lean Pro Reviews 2026: Ingredients, Discount & Official Site",
  "flashburn": "FlashBurn Review 2026: Flash Burn Drops Ingredients & Price",
  "gelatinesculpt": "Gelatine Sculpt Reviews 2026: Official Website, Price & Where to Buy"[:0] or "Gelatine Sculpt Reviews 2026: Official Website & Price",
  "glucoarmor": "Gluco Armor Review 2026: 20 Ingredients, Price & Official Website",
  "glucoextend": "Gluco Extend Reviews 2026: Ingredients, Discount & Official Site",
  "glycomute": "GlycoMute Reviews 2026: 20 Ingredients, Price & What to Know",
  "nervealive": "Nerve Alive Review 2026: Ingredients, Price & Official Website",
  "neuroserge": "Neuro Serge Reviews 2026: Price, Sale & Neuro Surge Facts",
  "prostapeak": "ProstaPeak Reviews 2026: Prosta Peak Ingredients & Official Site",
  "seroburn": "SeroBurn Review 2026: Serotonin Supplement Ingredients & Safety",
  "slimboosttea": "Slim Boost Tea 2026: Slimming Tea Ingredients, Safety & Price",
  "sonovive": "SonoVive Reviews 2026: Price, Discount & Official Website",
  "sugarmute": "SugarMute Reviews 2026: Sugar Mute Ingredients & Official Website",
  "titantransform": "Titan Transform Review 2026: Spray Ingredients, Price & Safety",
  "trimology": "Trimology Reviews 2026: Supplement Review & Where to Buy",
  "visiflora": "VisiFlora Reviews 2026: Ingredients, Discount & Official Website",
  "whispeara": "Whispeara Reviews 2026: Price, Discount & Official Website",
}

for sub, new in NEW.items():
    assert len(new) <= 65, (sub, len(new))
    path = os.path.join(ROOT, f"{sub}.medipicker.com", "index.html")
    s = io.open(path, encoding="utf-8").read()
    raw = re.search(r"<title>(.*?)</title>", s, re.S).group(1).strip()
    old_txt = html.unescape(raw)
    variants = {raw, old_txt, html.escape(old_txt, quote=False), old_txt.replace("&", "\\u0026")}
    n = 0
    for v in variants:
        if v and v in s:
            rep = html.escape(new, quote=False) if "&amp;" in v else new
            n += s.count(v)
            s = s.replace(v, rep)
    io.open(path, "w", encoding="utf-8", newline="").write(s)
    for spec in glob.glob(os.path.join(ROOT, "_build", "tools", "specs", f"{sub}*.py")):
        t = io.open(spec, encoding="utf-8").read()
        if old_txt in t:
            io.open(spec, "w", encoding="utf-8", newline="").write(t.replace(old_txt, new))
    print(f"{sub}: {len(old_txt)} -> {len(new)} chars, {n} replacements")
