"""Buying guides on medipicker.com (comparison pages built from our own reviews and ratings).

best_prostate(by_slug) -> (path, html) for /best-prostate-supplements/
Ratings come from ratings.py so the guide always matches the individual reviews.
"""
import json
from ratings import BLOG, SUB, label

URL = "https://medipicker.com/best-prostate-supplements/"
UPDATED, UPDATED_TXT = "2026-11-13", "November 13, 2026"
GADS = ("AW-18556458627", "AW-18556458627/yI6MCKjotLYdEIOttJBF")

# Hand-checked from each review (blog_data / in-depth review pages). Prices = lowest-highest per bottle on the official order page.
PRODUCTS = [
    dict(slug="titanflow", name="TitanFlow", score=SUB["titanflow"], review="/reviews/titanflow/",
         key="Pumpkin seed oil 500 mg, pygeum 100 mg, beta-sitosterol 30 mg, lycopene, broccoli sprout",
         saw=False, label_txt="Full label with doses", price="$39–$69", guarantee="180 days (even empty bottles)",
         good=["Full supplement facts label with every dose", "Pumpkin seed oil and pygeum close to studied doses",
               "Skips saw palmetto, which failed large trials", "Longest refund window we've seen: 180 days"],
         bad=["No trials on the product itself", "Beta-sitosterol and lycopene below studied doses", "Exaggerated 'urethra strength' sales story"],
         verdict="The most credible formula in this group: transparent, built on the better-studied herbs, with a long refund window. Expect modest help for mild symptoms."),
    dict(slug="prostapeak", name="ProstaPeak", score=SUB["prostapeak"], review="/reviews/prostapeak/",
         key="20+ herbs incl. saw palmetto, pygeum, green tea, cat's claw, soursop",
         saw=True, label_txt="Proprietary blend, doses hidden", price="$49–$79", guarantee="180 days",
         good=["Includes pygeum", "180-day money-back guarantee"],
         bad=["Doses hidden in a proprietary blend", "Leans on saw palmetto", "Many extras with no prostate evidence"],
         verdict="Familiar herbs, but hidden doses and a weak headline ingredient make it hard to recommend over TitanFlow or a doctor's check."),
    dict(slug="prostastream", name="ProstaStream", score=BLOG["prostastream"], review="/blog/prostastream/",
         key="Saw palmetto, pygeum, plant sterols, mushrooms, zinc, selenium",
         saw=True, label_txt="Ingredients listed", price="$49–$69", guarantee="60 days",
         good=["Contains pygeum and plant sterols", "Free US shipping on 6 bottles"],
         bad=["Long list of extras with no evidence", "Saw palmetto-based", "Unrealistic headline promise"],
         verdict="A couple of useful ingredients buried in a kitchen-sink formula."),
    dict(slug="vital-flow", name="VitalFlow", score=BLOG["vital-flow"], review="/blog/vital-flow/",
         key="Saw palmetto, pygeum, stinging nettle, lycopene, graviola, cat's claw",
         saw=True, label_txt="Ingredients named", price="$69", guarantee="60 days",
         good=["Includes pygeum and nettle", "Free US shipping"],
         bad=["Saw palmetto-based", "Contains graviola (safety concerns)", "No doses shown"],
         verdict="A standard prostate blend with an ingredient we'd rather avoid."),
    dict(slug="prostadine", name="Prostadine", score=BLOG["prostadine"], review="/blog/prostadine/",
         key="Saw palmetto, seaweeds (kelp, bladderwrack, wakame, nori), iodine, shilajit",
         saw=True, label_txt="Ingredients named", price="See review", guarantee="60 days",
         good=["Liquid drops, if you dislike capsules"],
         bad=["Mostly a seaweed and iodine tonic", "Iodine is a concern with thyroid disease", "Weak prostate evidence"],
         verdict="Not a prostate formula in any meaningful sense."),
    dict(slug="protoflow", name="ProtoFlow", score=BLOG["protoflow"], review="/blog/protoflow/",
         key="Saw palmetto, ginseng, damiana, epimedium, muira puama, cayenne",
         saw=True, label_txt="Ingredients named", price="$49–$79", guarantee="60 days",
         good=["Free US shipping on 6 bottles"],
         bad=["Mostly libido herbs, not prostate herbs", "Near-twin of Fluxactive", "Little evidence for any ingredient"],
         verdict="A libido blend sold as a prostate supplement."),
    dict(slug="fluxactive", name="Fluxactive Complete", score=BLOG["fluxactive"], review="/blog/fluxactive/",
         key="Saw palmetto, ginseng, damiana, epimedium, ginkgo, oat straw",
         saw=True, label_txt="Proprietary formula", price="$49–$79", guarantee="60 days",
         good=["Widely available, one-time payment"],
         bad=["Saw palmetto plus libido herbs", "Proprietary formula", "Unlikely to help urinary symptoms"],
         verdict="Unlikely to help urinary symptoms meaningfully."),
    dict(slug="flowforce-max", name="FlowForce Max", score=BLOG["flowforce-max"], review="/blog/flowforce-max/",
         key="Saw palmetto, oregano, grape seed, peppermint, muira puama",
         saw=True, label_txt="Ingredients named", price="See review", guarantee="See review",
         good=["Short ingredient list"],
         bad=["Blames prostate problems on fungus, which doesn't match medical understanding", "Saw palmetto-based"],
         verdict="Built on a theory of prostate trouble that medicine doesn't support."),
]

INGREDIENTS = [
    ("Beta-sitosterol (plant sterols)", "60–195 mg a day", "Better", "Cochrane review: improved symptom scores and peak urine flow (about 4 mL/s) versus placebo."),
    ("Pygeum (African plum bark)", "75–200 mg extract", "Moderate", "Older trials: less night-time urination and better flow; studies small and short."),
    ("Pumpkin seed / seed oil", "320 mg oil to 10 g seeds", "Moderate", "Modest symptom improvement over a year in BPH trials; prostate size unchanged."),
    ("Rye grass pollen (Cernilton)", "Studied extracts", "Some", "Small trials suggest symptom relief; not in any product above."),
    ("Stinging nettle root", "Varies", "Limited", "Mixed results, often studied combined with saw palmetto."),
    ("Lycopene", "15 mg a day", "Limited", "One small trial slowed PSA rise; little urinary-flow data."),
    ("Saw palmetto", "320 mg a day", "No benefit", "Large trials (STEP 2006, CAMUS 2011) found it no better than placebo, even at triple doses."),
]

FAQ = [
    ("What is the best prostate supplement?",
     "Of the prostate supplements we've reviewed, TitanFlow scores highest (3.5 out of 5) because it publishes its full label and is built on pumpkin seed oil and pygeum rather than saw palmetto. No supplement matches prescription treatment, so get checked by a doctor first."),
    ("Does saw palmetto work for an enlarged prostate?",
     "Large, well-run trials (STEP and CAMUS) found saw palmetto no better than placebo for urinary symptoms of BPH, even at high doses. Most prostate supplements still use it as their main ingredient."),
    ("Which ingredients have the best evidence?",
     "Beta-sitosterol has the most consistent evidence, followed by pygeum and pumpkin seed. Effects are modest: smaller than prescription alpha-blockers such as tamsulosin."),
    ("Can a supplement shrink the prostate?",
     "No supplement has been shown to shrink the prostate meaningfully. Prescription 5-alpha-reductase inhibitors (finasteride, dutasteride) do, over 6 to 12 months."),
    ("How long do prostate supplements take to work?",
     "Trials of pumpkin seed, pygeum and beta-sitosterol ran for 1 to 12 months. Give any supplement 8 to 12 weeks and track your symptoms before deciding."),
    ("Is it safe to take a prostate supplement with tamsulosin or finasteride?",
     "Serious interactions are uncommon, but ask your doctor before combining them. Finasteride changes PSA results, so your doctor needs to know everything you take."),
    ("When should I see a doctor instead?",
     "See a doctor before trying any supplement, and urgently if you have blood in your urine, pain, fever, or can't pass urine. The same symptoms can come from infection, diabetes or prostate cancer."),
]


def best_prostate(by_slug, rating_box, e):
    """Return the page body + JSON-LD. rating_box and e come from build_site so styling matches."""
    prods = sorted(PRODUCTS, key=lambda p: -p["score"])
    top = prods[0]
    top_link = by_slug["titanflow"]["link"]

    rows = "\n".join(
        f'            <tr><td><a href="{p["review"]}">{e(p["name"])}</a></td><td><strong>{p["score"]:.1f}</strong> / 5</td>'
        f'<td>{e(p["key"])}</td><td>{"Yes" if p["saw"] else "No"}</td><td>{e(p["label_txt"])}</td><td>{e(p["price"])}</td><td>{e(p["guarantee"])}</td></tr>'
        for p in prods)
    ing_rows = "\n".join(f"            <tr><td>{e(a)}</td><td>{e(b)}</td><td><strong>{e(c)}</strong></td><td>{e(d)}</td></tr>" for a, b, c, d in INGREDIENTS)

    cards = []
    for i, p in enumerate(prods, 1):
        good = "".join(f"<li>{e(x)}</li>" for x in p["good"])
        bad = "".join(f"<li>{e(x)}</li>" for x in p["bad"])
        cta = (f'      <div class="buy-box"><div><strong>{e(p["name"])}</strong><span>{e(p["price"])} per bottle &middot; {e(p["guarantee"])} guarantee</span></div>'
               f'<a class="btn btn-buy" href="{e(top_link)}" rel="sponsored nofollow noopener" target="_blank">Check {e(p["name"])} Price</a></div>\n'
               if p is top else "")
        cards.append(f'''      <h3 id="{p["slug"]}">{i}. {e(p["name"])}: {p["score"]:.1f}/5 ({label(p["score"])})</h3>
{rating_box(p["score"], "../")}      <p><strong>Key ingredients:</strong> {e(p["key"])}. <strong>Label:</strong> {e(p["label_txt"])}. <strong>Price:</strong> {e(p["price"])} per bottle. <strong>Guarantee:</strong> {e(p["guarantee"])}.</p>
      <div class="pros-cons"><div><h4>Good</h4><ul class="check-list">{good}</ul></div><div><h4>Not so good</h4><ul class="check-list warn">{bad}</ul></div></div>
      <p>{e(p["verdict"])} <a href="{p["review"]}">Read our full {e(p["name"])} review</a>.</p>
{cta}''')

    faq_html = "\n".join(f"        <details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in FAQ)

    body = f'''<main id="main" class="post">
  <div class="container post-wrap">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="../">MediPicker</a> <span aria-hidden="true">&rsaquo;</span> <a href="../blog/">Reviews</a> <span aria-hidden="true">&rsaquo;</span> <span>Best Prostate Supplements</span></nav>
    <article>
      <span class="rc-tag">Men's Health</span>
      <h1>Best Prostate Supplements 2026: 8 Formulas Compared by Label &amp; Evidence</h1>
      <p class="byline">By <a href="../about"><strong>MediPicker Editorial Team</strong></a> &middot; <a href="../how-we-review">How we review</a> &middot; Updated <time datetime="{UPDATED}">{UPDATED_TXT}</time></p>
      <p class="disclosure">MediPicker may earn money when you buy through links on this page. Sellers can&rsquo;t pay for a review or a better rating. <a href="../how-we-review#money">How we make money</a></p>
      <p class="lede">We compared the eight prostate health supplements we've reviewed in depth: their full labels, how their doses compare with clinical research, safety, price and refund terms. Most are built on saw palmetto, which large trials found no better than placebo. Only one stands out.</p>

      <aside class="callout"><strong>Our top pick: {e(top["name"])} ({top["score"]:.1f}/5).</strong> It publishes every dose, relies on pumpkin seed oil and pygeum instead of saw palmetto, and offers a 180-day refund even on empty bottles. <a href="{top["review"]}">Read the review</a>.</aside>

      <h2>Prostate Supplements Compared</h2>
      <p>Ranked by our editorial rating, which weighs evidence, label transparency, safety and value (<a href="../how-we-review#ratings">how we rate</a>).</p>
      <div class="table-wrap"><table class="price-table">
          <thead><tr><th>Supplement</th><th>Rating</th><th>Key ingredients</th><th>Saw palmetto?</th><th>Label</th><th>Price / bottle</th><th>Guarantee</th></tr></thead>
          <tbody>
{rows}
          </tbody></table></div>

      <h2>The Best Prostate Health Supplements, Reviewed</h2>
{chr(10).join(cards)}
      <h2>What to Look For in a Prostate Supplement</h2>
      <p>The ingredient list matters more than the brand. Here is what clinical research says about the ingredients you'll see on prostate supplement labels:</p>
      <div class="table-wrap"><table class="price-table">
          <thead><tr><th>Ingredient</th><th>Studied dose</th><th>Evidence</th><th>What studies found</th></tr></thead>
          <tbody>
{ing_rows}
          </tbody></table></div>
      <ul class="check-list">
        <li>Choose a product that publishes its full supplement facts label with doses, not a proprietary blend.</li>
        <li>Prefer beta-sitosterol, pygeum or pumpkin seed over saw palmetto.</li>
        <li>Look for a refund window long enough to judge results: at least 60 days, ideally 90 or more.</li>
        <li>Avoid formulas that promise to shrink your prostate or end night-time urination; no supplement has shown that.</li>
      </ul>

      <h2>See a Doctor First</h2>
      <p>About half of men in their 50s and most men over 70 have some prostate enlargement (BPH), but the same symptoms can come from infection, diabetes, medicines or prostate cancer. A doctor can check your prostate, urine and PSA. Prescription alpha-blockers such as tamsulosin often improve flow within days, and finasteride shrinks the prostate over months. Both work better than any supplement.</p>
      <ul class="check-list warn">
        <li>Blood in your urine or semen</li>
        <li>Pain or burning when urinating, or fever</li>
        <li>Sudden inability to urinate: get urgent care</li>
        <li>Symptoms that worsen quickly or wake you several times a night</li>
      </ul>

      <h2>Prostate Supplement FAQ</h2>
      <div class="faq">
{faq_html}
      </div>
    </article>
  </div>
</main>
'''
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": "Best Prostate Supplements 2026: 8 Formulas Compared by Label & Evidence",
         "datePublished": UPDATED, "dateModified": UPDATED, "mainEntityOfPage": URL,
         "author": {"@type": "Organization", "name": "MediPicker Editorial Team", "url": "https://medipicker.com/about"},
         "publisher": {"@type": "Organization", "name": "MediPicker", "url": "https://medipicker.com/"}, "inLanguage": "en-US"},
        {"@type": "ItemList", "name": "Best prostate supplements", "itemListElement": [
            {"@type": "ListItem", "position": i, "name": p["name"], "url": "https://medipicker.com" + p["review"]} for i, p in enumerate(prods, 1)]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "MediPicker", "item": "https://medipicker.com/"},
            {"@type": "ListItem", "position": 2, "name": "Reviews", "item": "https://medipicker.com/blog/"},
            {"@type": "ListItem", "position": 3, "name": "Best Prostate Supplements", "item": URL}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    ]}
    aw, conv = GADS
    gads = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={aw}"></script>\n'
            "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());"
            f"gtag('config','{aw}');document.addEventListener('click',function(e){{var a=e.target.closest&&e.target.closest('a[rel~=\"sponsored\"]');"
            f"if(a)gtag('event','conversion',{{'send_to':'{conv}','transport_type':'beacon'}});}},true);</script>\n")
    return body, json.dumps(ld, ensure_ascii=False, indent=2), gads
