# Blog rewrite (started 27 Oct 2026, resumed 5 Nov 2026)

## Why
- Google impressions collapsed after 20 Oct 2026; live inspection showed pages dropped ("Crawled – currently not indexed").
- Blog pages were category templates: same-category pages shared 53–59% of 8-word phrases.
- Fix: every template page is `noindex, follow` and left out of the sitemap (`robots()` in build_site.py). A page becomes indexable once `_build/blog_data/<slug>.json` exists.
- Rewritten pages share only 9–25% with each other (`python _build/tools/overlap.py a b c`).

## Workflow per batch
1. `PYTHONIOENCODING=utf-8 python _build/tools/brief.py <slug> ...`: headline, price, guarantee, dosage and ingredient lines from `work/sales/<slug>.txt` (+ `.root.txt` vendor homepage). Use grep on those files for details.
2. Write `_build/blog_data/_batchNN.py` (a dict of slug -> fields), then run it to produce the JSON files.
3. New ingredients go in `_build/ing_extra_NN.py` (`EXTRA = {key: {name, what, evidence, safety?}}`), which ingredients.py auto-loads. Check that no ingredient key is missing from ING.
4. `python _build/build_site.py`, then commit and `git push medipicker medipicker.com`.
5. After deploy: request indexing in GSC (about 10 a day) and send IndexNow pings for the new URLs.

## blog_data fields
- checked: date
- form
- currency: EUR or GBP; optional, defaults to USD
- hook: the sales headline, quoted exactly
- claim: what the product is sold as; its first sentence becomes the lede
- story: optional extra paragraph
- ingredients[]: keys into ING
- ing_note
- use: dosage
- packages[[bottles, total, "shipping"]]
- days_per_bottle: optional, defaults to 30
- price_note
- one_time
- guarantee_days
- refund_note
- bonuses[]
- checks[]: claims vs evidence
- pros[]
- cons[]
- verdict
- faqs[[q, a]]: optional

Rules: only facts the seller's page states, plus well-established research. No invented prices; if prices are hidden, use price_note. Be honest about mismatches.

## Status (5 Nov 2026): COMPLETE
- 85 product-specific reviews are live and indexable: median 1,054 words (min 767, max 1,480), up from a 576-word median.
- Same-category overlap: median 21% shared 8-word phrases (max 55% for products that really are the same formula), down from 53-59%.
- Sitemap: 93 URLs (85 reviews + home, blog, about, how-we-review, contact and legal pages). Submitted to GSC (read OK) and IndexNow.
- Kept noindex on purpose:
  - The 23 products that have in-depth subdomain reviews (avoids two pages competing).
  - Thin or no-data pages: fast-brain-booster, triple-collagen, triple-anti-aging-cream, fungus-elixir, vitasana-collections, sonus-complete, dentivive, ocurenew (fetch timed out).
  - Off-topic pages: derila-ergo-pillow, certified-concealed-first.
- Valiora disabled (broken tracking link).

## Daily follow-up
- GSC Request Indexing (about 10 a day). Already requested on 5 Nov: vivogut, visium-plus, synogut, claritox-pro, goldalign, brain-memory-keeper, prostastream, neurozoom, cleansesana.
- Next: dentasmile-pro, then the remaining sitemap URLs in order.
- Watch GSC Performance weekly; re-check sales pages roughly monthly for price changes (re-run `fetch_sales.py` and update the batch files).
