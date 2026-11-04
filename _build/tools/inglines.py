"""Print lines naming ingredients (from sales page + vendor homepage): python inglines.py <slug> [max]."""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from ingvocab import TERMS
rx = re.compile("|".join(r"\b" + t.replace(" ", r"\s") for t in TERMS), re.I)
D = os.path.join(os.path.dirname(__file__), "..", "work", "sales")
seen, n = set(), 0
for f in (sys.argv[1] + ".txt", sys.argv[1] + ".root.txt"):
    p = os.path.join(D, f)
    if not os.path.exists(p):
        continue
    for l in io.open(p, encoding="utf-8").read().splitlines()[1:]:
        if rx.search(l) and 6 < len(l) < 400 and l[:50] not in seen and not re.search(r"evaluated by the Food|diagnose", l):
            seen.add(l[:50]); print(l[:300]); n += 1
            if n >= int(sys.argv[2] if len(sys.argv) > 2 else 40):
                sys.exit()
