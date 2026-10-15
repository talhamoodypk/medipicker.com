"""Build the MediPicker home page (index.html at the repo root) from products.tsv.

Run:  py -I -X utf8 _build/build_home.py
Edit products.tsv (name<TAB>link) to add products; the first link for each product wins.
Edit CATEGORY below to change which category a product is listed under.
"""
import html, io, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TSV = os.path.join(ROOT, "_build", "products.tsv")

# Network/version suffixes that aren't part of the product name
SUFFIXES = [" MW DTC", " German MW", " Short Version", " - Studies lead", " - EMOTIONAL",
            " MW", " CB", " DTC", " TSL", " Adv", " V2", " UK"]
DISPLAY_OVERRIDE = {"GlucoTrust": "GlucoTrust (German)", "All Day Slimming Tea": "All Day Slimming Tea (UK)"}

CATEGORY = {
  "Weight Loss": ["Trimology", "Gelatine Sculpt", "FlashBurn", "SeroBurn", "Slim Boost Tea", "KeySlim", "FitSpresso",
                  "Fast Lean Pro", "PurpleBurn Pro", "HoneyBurn", "All Day Slimming Tea", "Hidragenix", "MetaboSana",
                  "Flush Factor Plus"],
  "Blood Sugar": ["CelluCare", "Gluco Armor", "SugarMute", "GlycoMute", "GlucoTrust", "GlycoFortin", "Free Sugar Pro",
                  "MetaGlucent", "GlucoGuard Pro", "Gluco Extend", "GlucoSana", "GlucoFlush", "VivoTonic", "Triple Blood Balance"],
  "Men's Health": ["AlphaFuel Pro", "ProstaPeak", "EndoPeak", "Prostadine", "FlowForce Max", "ProtoFlow", "Fluxactive",
                   "Emperor's Vigor Tonic", "TitanFlow", "Forti Prime", "VigorSana", "ProstaStream", "Vital Flow"],
  "Hearing": ["Whispeara", "Tinnitrol", "Audifort", "Synaptigen", "SharpEar", "Sonovive", "Quietum Plus", "AquaPeace",
              "Sonus Complete", "Serenity Prime", "VidaCalm"],
  "Brain & Memory": ["Neurozoom", "Fast Brain Booster", "Brain Memory Keeper", "MemoDefend", "Memo Max Pro", "ProMind Complex"],
  "Nerves & Joints": ["NerveAlive", "Nerve Soothe", "Sciaticyl", "NerveSana", "Jointgen", "MarineFlex Ultra"],
  "Dental Health": ["Dentavive", "BioDentex", "Synadentix", "DentaSmile Pro", "Fortbite", "PowerBite", "Dentitox Pro", "DentiVive"],
  "Vision": ["VisiFlora", "EyeFortin", "OptiPlax", "Vitrafoxin", "OcuRenew", "Visium Plus"],
  "Skin, Hair & Nails": ["Kerassentials", "TerraCalm", "Supranail", "Keragenis", "RevaNail", "ReFirmance", "Triple Collagen",
                         "Triple Anti-Aging Cream", "Fungus Elixir", "Bio Fungus Nuker", "Keravita Pro", "Triple Fungus Blast",
                         "Mycosyn Pro", "Derma Prime Plus", "Restolin", "FoliPrime", "Neotonics", "PrimeBiome"],
  "Gut & Detox": ["DigestiStart", "VivoGut", "SynoGut", "Cleanest Body", "Triple Liver Health", "CleanseSana"],
  "Heart, Lungs & Immunity": ["Arteris Plus", "Lungora", "TonicGreens", "NewEra Protect"],
  "Balance": ["VertiAid", "Claritox Pro"],
  "Pets": ["UltraK9 Pro", "PawBiotix"],
  "Home & Lifestyle": ["Derila Ergo Pillow", "Certified Concealed First"],
}
DEFAULT_CAT = "General Wellness"
CAT_OF = {n.lower(): c for c, names in CATEGORY.items() for n in names}
CAT_ORDER = list(CATEGORY) + [DEFAULT_CAT]
CAT_ICON = {  # simple stroke icons (24x24)
  "Weight Loss": '<path d="M5 20h14M7 20l2-12h6l2 12"/><path d="M9.5 8a2.5 2.5 0 0 1 5 0"/>',
  "Blood Sugar": '<path d="M12 3c3 4.5 6 7.5 6 11a6 6 0 0 1-12 0c0-3.5 3-6.5 6-11z"/>',
  "Men's Health": '<circle cx="10" cy="14" r="6"/><path d="M14.5 9.5 20 4M15 4h5v5"/>',
  "Hearing": '<path d="M7 9a5 5 0 0 1 10 0c0 3-3 4-3 7a3 3 0 0 1-6 0"/><path d="M10 9a2 2 0 0 1 4 0"/>',
  "Brain & Memory": '<path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 3 5 3 3 0 0 0 5 1V5a3 3 0 0 0-3-1z"/><path d="M15 4a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-3 5 3 3 0 0 1-5 1"/>',
  "Nerves & Joints": '<path d="M4 12h4l2-6 4 12 2-6h4"/>',
  "Dental Health": '<path d="M7 3c-2 0-3 2-3 4 0 4 2 6 2 10 0 2 1 4 2 4s2-3 2-5h4c0 2 1 5 2 5s2-2 2-4c0-4 2-6 2-10 0-2-1-4-3-4-2 0-3 1-5 1S9 3 7 3z"/>',
  "Vision": '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
  "Skin, Hair & Nails": '<path d="M12 3l2.5 5.5L20 9l-4 4 1 6-5-3-5 3 1-6-4-4 5.5-.5z"/>',
  "Gut & Detox": '<path d="M5 21c0-9 5-15 15-17-1 10-6 15-15 17z"/><path d="M5 21 14 12"/>',
  "Heart, Lungs & Immunity": '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>',
  "Balance": '<path d="M12 3v18M5 7h14M5 7l-3 6a3 3 0 0 0 6 0zM19 7l-3 6a3 3 0 0 0 6 0z"/>',
  "Pets": '<circle cx="6" cy="10" r="2"/><circle cx="10" cy="6" r="2"/><circle cx="14" cy="6" r="2"/><circle cx="18" cy="10" r="2"/><path d="M8 17c0-3 2-5 4-5s4 2 4 5-2 3-4 3-4 0-4-3z"/>',
  "Home & Lifestyle": '<path d="M3 11l9-7 9 7v9H3z"/><path d="M9 20v-6h6v6"/>',
  "General Wellness": '<path d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
}
REVIEWS = {  # products that have a full review site
  "trimology": "https://trimology.medipicker.com/",
  "gelatine sculpt": "https://gelatinesculpt.medipicker.com/",
}


def clean(name):
    n = " ".join(name.split())
    changed = True
    while changed:
        changed = False
        for s in SUFFIXES:
            if n.endswith(s):
                n, changed = n[: -len(s)].strip(), True
    return n


def load():
    seen, items = set(), []
    for line in io.open(TSV, encoding="utf-8"):
        if "\t" not in line:
            continue
        raw, link = [p.strip() for p in line.split("\t", 1)]
        base = clean(raw)
        key = base.lower()
        if not link or key in seen:
            continue
        seen.add(key)
        display = DISPLAY_OVERRIDE.get(base, base)
        items.append({"name": display, "key": key, "link": link, "cat": CAT_OF.get(key, DEFAULT_CAT),
                      "review": REVIEWS.get(key)})
    return items


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def card(p):
    e = html.escape
    initials = "".join(w[0] for w in re.findall(r"[A-Za-z0-9]+", p["name"])[:2]).upper()
    review = (f'<a class="link-review" href="{p["review"]}">Read review</a>' if p["review"] else "")
    return f'''      <li class="product" data-cat="{slug(p["cat"])}" data-name="{e(p["name"].lower())}">
        <div class="p-top">
          <span class="p-badge" aria-hidden="true">{e(initials)}</span>
          <div>
            <h3>{e(p["name"])}</h3>
            <span class="p-cat">{e(p["cat"])}</span>
          </div>
        </div>
        <div class="p-actions">
          <a class="btn btn-buy" href="{e(p["link"])}" rel="sponsored nofollow noopener" target="_blank">Buy Now<span class="sr-only"> {e(p["name"])}</span></a>
          {review}
        </div>
      </li>'''


def build():
    items = load()
    cats = [c for c in CAT_ORDER if any(p["cat"] == c for p in items)]
    counts = {c: sum(1 for p in items if p["cat"] == c) for c in cats}
    items_sorted = sorted(items, key=lambda p: (CAT_ORDER.index(p["cat"]), p["name"].lower()))

    chips = '\n'.join(
        f'        <button type="button" class="chip" data-filter="{slug(c)}" aria-pressed="false">{html.escape(c)} <span>{counts[c]}</span></button>'
        for c in cats)

    sections = []
    for c in cats:
        group = [p for p in items_sorted if p["cat"] == c]
        sections.append(f'''  <section class="cat-block" id="{slug(c)}" data-cat-block="{slug(c)}" aria-labelledby="h-{slug(c)}">
    <div class="cat-head">
      <span class="cat-icon" aria-hidden="true"><svg viewBox="0 0 24 24">{CAT_ICON.get(c, CAT_ICON[DEFAULT_CAT])}</svg></span>
      <h2 id="h-{slug(c)}">{html.escape(c)}</h2>
      <span class="cat-count">{len(group)} products</span>
    </div>
    <ul class="product-grid">
{chr(10).join(card(p) for p in group)}
    </ul>
  </section>''')

    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "MediPicker Health Product Directory",
        "numberOfItems": len(items_sorted),
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": p["name"]} for i, p in enumerate(items_sorted)],
    }
    site_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Organization", "@id": "https://medipicker.com/#org", "name": "MediPicker", "url": "https://medipicker.com/",
             "logo": "https://medipicker.com/favicon.svg"},
            {"@type": "WebSite", "@id": "https://medipicker.com/#website", "url": "https://medipicker.com/", "name": "MediPicker",
             "publisher": {"@id": "https://medipicker.com/#org"}, "inLanguage": "en-US"},
        ],
    }

    tpl = io.open(os.path.join(ROOT, "_build", "home_template.html"), encoding="utf-8").read()
    out = (tpl.replace("{{COUNT}}", str(len(items)))
              .replace("{{CAT_COUNT}}", str(len(cats)))
              .replace("{{CHIPS}}", chips)
              .replace("{{SECTIONS}}", "\n\n".join(sections))
              .replace("{{ITEMLIST_LD}}", json.dumps(item_list, ensure_ascii=False, indent=2))
              .replace("{{SITE_LD}}", json.dumps(site_ld, ensure_ascii=False, indent=2)))
    io.open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8", newline="\n").write(out)
    print(f"{len(items)} unique products in {len(cats)} categories")
    for c in cats:
        print(f"  {c}: {counts[c]}")
    print("General Wellness:", [p["name"] for p in items if p["cat"] == DEFAULT_CAT])


if __name__ == "__main__":
    # The full site (home + blog) is now built by build_site.py
    import build_site
    build_site.main()
