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

## Done (13)
synogut, vivogut, claritox-pro, metaglucent, brain-memory-keeper, goldalign, fitspresso, prostastream, neurozoom,
cleansesana, triple-blood-balance, endopeak, visium-plus.
Valiora was disabled (broken tracking link).

## Next, in priority order (GSC impressions first)
dentasmile-pro, supranail, derma-prime-plus, ultrak9-pro, refirmance, terracalm, sonivon(?), audifort, revanail, keyslim,
honeyburn, tinnitrol, glucoflush, primebiome, triple-liver-health; then all remaining slugs
(`ls medipicker.com/blog`, minus the ones done).

## Findings worth reusing
- VivoGut is a thyroid-style formula sold as gut support.
- Visium Plus is a prostate formula sold as vision support.
- CleanseSana is the SynoGut formula with published mg amounts (glucomannan 8.5 mg).
- MetaGlucent and EndoPeak use the same $158 / $207 / $294 package structure.
- Claritox, SynoGut and Visium share the "$69 one-time, 60-day, FDA/GMP" letter template.
