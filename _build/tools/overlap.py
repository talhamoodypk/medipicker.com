"""Shared 8-word phrases between blog pages: python overlap.py slug1 slug2 ... (main content only)."""
import html, itertools, os, re, sys
B = os.path.join(os.path.dirname(__file__), "..", "..", "medipicker.com", "blog")
def words(s):
    t = open(os.path.join(B, s, "index.html"), encoding="utf-8").read()
    return html.unescape(re.sub(r"<[^>]+>", " ", re.search(r"<main.*?</main>", t, re.S).group(0))).split()
def sh(w):
    return {" ".join(w[i:i + 8]) for i in range(len(w) - 8)}
P = {s: words(s) for s in sys.argv[1:]}
for a, b in itertools.combinations(P, 2):
    A, C = sh(P[a]), sh(P[b])
    print(f"{a} vs {b}: {100 * len(A & C) / min(len(A), len(C)):.0f}% shared | words {len(P[a])}/{len(P[b])}")
