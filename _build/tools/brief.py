"""Compact research brief for writing blog_data: python brief.py <slug> [<slug> ...]."""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from ingvocab import TERMS
ING = re.compile("|".join(r"\b" + t.replace(" ", r"\s") for t in TERMS), re.I)
D = os.path.join(os.path.dirname(__file__), "..", "work", "sales")
SKIP = re.compile(r"evaluated by the Food|diagnose, treat|Wilmington|ClickBank|Testimonials|results may vary|Privacy|Terms of|Copyright|cookies", re.I)
PRICE = re.compile(r"\$\s?\d|total|per bottle|bottles?\b|supply|shipping", re.I)
GUAR = re.compile(r"\d+[- ]day|guarantee|refund|return", re.I)
DOSE = re.compile(r"\b(take|capsules?|tablets?|drops?|scoop|serving|gumm|per day|daily|dropper|morning|before (bed|meals))\b", re.I)
for slug in sys.argv[1:]:
    lines, src = [], []
    for f in (slug + ".txt", slug + ".root.txt"):
        p = os.path.join(D, f)
        if os.path.exists(p):
            t = io.open(p, encoding="utf-8").read().splitlines()
            src.append(t[0].split("?")[0]); lines += t[1:]
    lines = [l for l in lines if 4 < len(l) < 400 and not SKIP.search(l)]
    print(f"######## {slug}  {' | '.join(src)}")
    seen = set()
    def show(tag, rx, cap):
        out = []
        for l in lines:
            if rx.search(l) and l[:60] not in seen:
                seen.add(l[:60]); out.append(l[:260])
            if len(out) >= cap: break
        if out: print(f"[{tag}] " + " || ".join(out))
    print("[HEAD] " + " || ".join(l[:160] for l in lines[:4]))
    show("PRICE", PRICE, 14); show("GUAR", GUAR, 4); show("DOSE", DOSE, 5); show("ING", ING, 14)
