"""Batch 18 of hand-checked blog data (sources: work/sales/<slug>.txt and .root.txt, checked 2026-11-05).

Skipped (kept noindex, not enough product facts on the seller's pages): vitasana-collections, sonus-complete.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
C = "2026-11-05"
D = {
"keravita-pro": dict(checked=C, form="capsules",
  hook="NASA: This Is What We Do So Astronauts Don't Get Toenail Fungus (Do This Immediately!)",
  claim="Keravita Pro is a capsule sold for toenail fungus and healthy nails and hair, with a headline linking it to NASA. The sales letter describes 'over 95,000 customers'.",
  story="The Keravita Pro sales letter is word-for-word the same as the Keragenis letter, with the same '17 years of research' author and the same ingredient list (curcumin, cat's claw, garlic, quercetin, pomegranate and olive). NASA has no connection to the product.",
  ingredients=["turmeric", "cat's claw", "garlic", "quercetin", "pomegranate", "olive leaf"],
  ing_note="The letter names these ingredients 'such as'; the full label and amounts aren't shown.",
  packages=[[1, 69, "Free US shipping"]],
  price_note="3- and 6-bottle packages are discounted, with free US shipping; totals appear on the order page.",
  one_time=True, guarantee_days=60, refund_note="The seller promises a full refund within 60 days even if the bottle is used up.",
  checks=["The NASA headline is a curiosity hook; NASA hasn't endorsed or studied this product.",
          "None of the ingredients is an antifungal with evidence against nail fungus.",
          "The '95,000 customers' figure can't be verified.",
          "The same letter and formula are sold under another name (Keragenis)."],
  pros=["One-time price with free US shipping", "60-day guarantee"],
  cons=["No antifungal ingredient", "Misleading NASA headline", "Duplicate of another product", "Full label not shown"],
  verdict="Keravita Pro is the Keragenis formula with a NASA headline. Neither will treat nail fungus. A doctor or podiatrist can confirm the diagnosis and prescribe antifungal treatments with proven cure rates."),

"marineflex-ultra": dict(checked=C, form="capsules",
  hook="Military Doctor Shares \"Marine Tribal Secret\"",
  claim="MarineFlex Ultra is a joint supplement presented by a 'military doctor' as a 'marine tribal secret'. It's built around green-lipped mussel, a New Zealand shellfish rich in omega-3s, with boswellia, hyaluronic acid and glucosamine.",
  ingredients=["green lipped mussel", "boswellia", "hyaluronic acid", "glucosamine"],
  ing_note="Amounts aren't given in text. The page argues fish oil carries a risk of mercury poisoning; purified fish oil supplements are tested and generally low in mercury.",
  packages=[], price_note="The page says MarineFlex Ultra 'normally retails for $149 per bottle' and then offers lower package prices on the order page. The seller recommends at least 3 bottles.",
  checks=["Green-lipped mussel extract has small trials suggesting modest reductions in osteoarthritis pain; quality is mixed.",
          "Glucosamine sulfate showed small benefits in some European trials, but the large US GAIT trial found no clear benefit over placebo.",
          "Boswellia has small trials for knee osteoarthritis pain.",
          "'$149 per bottle' is a price anchor, not a real retail price."],
  pros=["Ingredients with some joint research", "Combines several popular joint ingredients"],
  cons=["Price anchoring and scarcity tactics", "Overstated fish oil scare", "Shellfish source, so not for people with shellfish allergy", "Amounts not disclosed"],
  verdict="MarineFlex Ultra combines joint ingredients with modest evidence, wrapped in dramatic marketing. People with shellfish allergies must avoid it. Exercise, weight loss and physical therapy are the most effective long-term treatments for joint pain."),

"memo-max-pro": dict(checked=C, form="capsules",
  hook="5 Easy-To-Follow Memory Supporting Tips That You Wish You Had Known Sooner",
  claim="Memo Max Pro is a memory capsule sold through a letter from 'James Beller', which shares five memory tips (dark chocolate, green tea, brain training and more) before introducing the formula.",
  ingredients=["beta-glucan", "pine bark", "grape seed", "mushroom complex", "ginseng", "quercetin"],
  ing_note="The letter lists these ingredients; amounts aren't disclosed. The 'mushroom complex' isn't broken down by species.",
  packages=[[1, 69, "Free shipping"]],
  price_note="3- and 6-bottle packages are discounted; totals appear on the order page.",
  one_time=True, guarantee_days=60, refund_note="The seller promises a full refund within 60 days even if the bottle is used up.",
  checks=["Some of the letter's tips are reasonable: regular mental challenge and physical activity are linked to better cognitive aging.",
          "Cocoa flavanols showed a small memory benefit in one large trial (COSMOS) only in people with poor diets.",
          "Beta-glucan, pine bark and grape seed are immune and circulation ingredients, not memory ingredients.",
          "Panax ginseng has small, inconsistent memory studies."],
  pros=["Some sensible memory advice in the letter", "One-time price with free shipping", "60-day guarantee"],
  cons=["Ingredients don't target memory", "Unspecified mushroom complex", "Template sales letter", "Amounts not disclosed"],
  verdict="Memo Max Pro's best feature is its free advice. The capsule itself is a general antioxidant blend with no real memory evidence. See a doctor about memory concerns; checking B12, thyroid, hearing, sleep and mood often finds treatable causes."),
}

if __name__ == "__main__":
    for k, v in D.items():
        json.dump(v, open(os.path.join(HERE, k + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(D), "written")
