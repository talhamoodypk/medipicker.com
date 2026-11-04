"""Print a compact fact digest of a fetched sales page: python digest.py <slug> [maxlines]."""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from ingvocab import TERMS
ING = re.compile("|".join(r"" + t.replace(" ", r"\s") for t in TERMS), re.I)
D = os.path.join(os.path.dirname(__file__), "..", "work", "sales")
PAT = re.compile(r"\$\s?\d|\bmg\b|mcg|\biu\b|guarantee|refund|capsule|tablet|gumm|drops?\b|scoop|powder|serving|take \d|per day|daily|"
                 r"ingredient|extract|root|leaf|seed|vitamin|bonus|free shipping|shipping|made in|gmp|fda|non-gmo|gluten|vegan|"
                 r"stimulant|supply|bottle|clinical|study|studies|research|scientist|doctor|dr\.|secret|ritual|hack|trick|discover", re.I)
def digest(slug, maxl=70):
    t = io.open(os.path.join(D, slug + ".txt"), encoding="utf-8").read().splitlines()
    root = os.path.join(D, slug + ".root.txt")
    if os.path.exists(root):
        t += ["== vendor homepage =="] + io.open(root, encoding="utf-8").read().splitlines()[1:]
    url, lines = t[0], t[1:]
    out, seen = [url.split("?")[0]], set()
    out += [l for l in lines[:6] if len(l) > 15][:3]
    for l in lines:
        k = l.lower()[:60]
        if (PAT.search(l) or ING.search(l)) and 8 < len(l) < 260 and not re.search(r"evaluated by the Food|diagnose, treat|Wilmington|ClickBank is|retailer of products|^\s*(Privacy|Terms|Contact)", l) and k not in seen:
            seen.add(k); out.append(l)
    return out[:maxl]
if __name__ == "__main__":
    for l in digest(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 70):
        print(l)
