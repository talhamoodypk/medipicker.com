# Blog expansion (started 27 Oct 2026)

Goal: replace category-template blog pages (median 576 words) with product-specific reviews of 1,500+ words.
Reason: Google impressions collapsed on 20 Oct (site-level quality re-score); the blog pages are near-identical templates.

## Pipeline
1. `python _build/tools/fetch_sales.py` (run from `_build/`): saves each sales page to `_build/work/sales/<slug>.html/.txt`. Done for 117/119 (seroburn and ocurenew timed out).
2. `python _build/tools/digest.py <slug> 45`: compact fact digest (headline, prices, guarantee, dosage, ingredient lines).
3. Write `_build/blog_data/<slug>.json` by hand from the digest. Only facts the page states; quote the headline; no invented numbers.
4. Ingredient evidence lives in `_build/ingredients.py` (ING dict): what it is, evidence, safety. Keys are lowercase.
5. `python _build/build_site.py` renders the extra sections when `blog_data/<slug>.json` exists.

## blog_data fields
hook, claim, story, form, use, ingredients[keys], ing_note, packages[[bottles,total,"shipping"]],
guarantee_days, refund_note, bonuses[], made, checks[], pros[], cons[], verdict, faqs[[q,a]]

## Order
Products with GSC impressions first: fitspresso, claritox-pro, goldalign, synogut, metaglucent, brain-memory-keeper,
vivogut, prostastream, neurozoom, cleansesana, triple-blood-balance, endopeak, visium-plus, valiora, dentasmile-pro,
supranail, derma-prime-plus, ultrak9-pro, refirmance, terracalm, sonivon; then everything else.

## Progress
Track with `ls _build/blog_data | wc -l`.
