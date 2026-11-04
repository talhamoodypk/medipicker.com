"""Batch 2 of hand-checked blog data (sources: work/sales/<slug>.txt and .root.txt, checked 2026-11-05)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
C = "2026-11-05"
D = {
"fitspresso": dict(checked=C, form="capsules",
  hook="This Special Coffee Loophole Helped Me Drop 61 LBS In Weeks",
  claim="FitSpresso is sold as a 'coffee loophole' for weight loss: a capsule you take alongside your morning coffee. The official page is a video sales letter, and the product details only appear inside the video and on the checkout page.",
  story="The research list under the video is all about green coffee bean extract, green tea catechins (EGCG), caffeine, L-theanine and L-carnitine, which suggests these are the active ingredients, but the page itself doesn't confirm a supplement facts label in text.",
  ingredients=[],
  ing_note="The FitSpresso page doesn't list its ingredients in text; the studies it cites cover green coffee bean extract, green tea extract, caffeine, L-theanine and L-carnitine. If you take other caffeine products or are sensitive to stimulants, check the label before you order.",
  packages=[], price_note="FitSpresso prices are shown only on the checkout page after the video, so we couldn't record them. Check the total, shipping and whether the order is a one-time payment before paying.",
  checks=["'Drop 61 lbs in weeks' is an individual testimonial, not a typical result; no trial of FitSpresso exists.",
          "Green tea catechins with caffeine raised 24-hour energy use in small studies, but the extra calories burned are small (roughly 100 a day at best).",
          "A 2019 meta-analysis of L-carnitine found an average extra loss of about 1.3 kg compared with placebo, which is a modest effect.",
          "Green coffee bean extract trials are small and several were poorly run; one widely cited study was retracted."],
  pros=["Cites real research on its likely ingredients", "Simple routine (capsule with morning coffee)"],
  cons=["No ingredient list or prices on the sales page", "Dramatic weight-loss headline", "Likely contains caffeine on top of your coffee", "Evidence for the ingredients shows small effects only"],
  verdict="FitSpresso's likely ingredients (green tea, green coffee, caffeine, L-carnitine) have some research behind them, but the effects in studies are small and nowhere near '61 lbs in weeks'. Because the sales page hides both the label and the price until checkout, read both carefully before you buy, and count its caffeine together with your coffee."),

"prostastream": dict(checked=C, form="capsules",
  hook="15-Second Male Bedtime Ritual Shrinks Your Prostate in Just Weeks",
  claim="ProstaStream is a prostate supplement sold to men with frequent night-time urination and a weak stream. It combines saw palmetto, pygeum, plant sterols and a trio of Japanese mushrooms with zinc, selenium and vitamins.",
  ingredients=["saw palmetto", "pygeum", "plant sterols", "maitake", "reishi", "shiitake", "cat's claw", "lycopene", "green tea", "broccoli", "selenium", "vitamin e", "vitamin b6", "zinc", "copper"],
  ing_note="The video transcript names these ingredients but gives no amounts. Tomato fruit powder is the source of lycopene, and broccoli leaf extract is listed for its sulforaphane-type compounds.",
  packages=[[1, 69, "Shipping extra"], [6, 294, "Free US shipping"]],
  price_note="The seller compares this with a '$147' price that it was never sold at. A 3-bottle package is also offered; its total is shown on the order page.",
  guarantee_days=60, refund_note="Refunds are requested by email to the US customer service team within 60 days of purchase.",
  checks=["No supplement can 'shrink your prostate in weeks'. Prescription drugs for enlarged prostate (BPH) take months to reduce prostate size.",
          "Saw palmetto has been tested in large, well-run trials (STEP and CAMUS) and worked no better than placebo for urinary symptoms.",
          "Pygeum and beta-sitosterol (plant sterols) have modest supporting evidence from older, smaller trials.",
          "The mushroom, broccoli and green tea extracts have no clinical evidence for prostate symptoms."],
  pros=["Contains plant sterols and pygeum, the best-supported herbal options for BPH", "Free US shipping on the 6-bottle package", "60-day money-back guarantee"],
  cons=["'Shrinks your prostate' claim is unsupported", "Main ingredient (saw palmetto) failed in the largest trials", "No ingredient amounts", "Long list of minor ingredients likely at tiny doses"],
  verdict="ProstaStream includes a couple of ingredients with some evidence (pygeum and plant sterols) alongside a long list of extras with none, and its headline promise is not realistic. Urinary symptoms can also be a sign of infection, diabetes or prostate cancer, so men should get a PSA test and a doctor's check before relying on any supplement."),

"neurozoom": dict(checked=C, form="capsules",
  hook="People With Early Alzheimer's Do This Bathroom Mistake",
  claim="NeuroZoom is sold as a memory and cognitive-health supplement with a 'proprietary formula of 35 memory essential antioxidants, minerals, vitamins and herbs'. In practice it is a broad multivitamin with a few brain-related extras.",
  ingredients=["huperzine a", "bacopa", "phosphatidylserine", "green tea", "olive leaf", "bilberry", "licorice", "chromium", "vitamin e", "vitamin c", "selenium", "magnesium"],
  ing_note="The full list also includes riboflavin, niacin, vitamin B6, thiamine, biotin, choline, beta carotene, boron, zinc, vitamin B5, N-acetyl-L-tyrosine, DHA, vanadyl sulphate, calcium, cinnamon bark, grapefruit seed extract, molybdenum, inositol, iron, manganese and L-glutamine. With 35 ingredients in a few capsules, most can only be present in small amounts.",
  packages=[], price_note="NeuroZoom is sold in 2-month, 3-month and 6-month packages; the 2-month package has a small shipping fee and the 6-month package ships free in the US. Totals are shown on the order page.",
  guarantee_days=60, refund_note="The refund policy requires you to return the product within 60 days of receiving it.",
  bonuses=["Supercharge Your Body", "Biohacking Secrets"],
  checks=["The 'bathroom mistake' headline is a curiosity hook; there is no known bathroom habit that signals or causes Alzheimer's.",
          "Huperzine A acts like some prescription Alzheimer's drugs, but a large US trial found no benefit for Alzheimer's disease.",
          "Bacopa and phosphatidylserine have small studies showing modest memory benefits at doses a 35-ingredient blend is unlikely to reach.",
          "Vitamins only help memory if you are deficient (B12 in particular)."],
  pros=["Full ingredient list is published", "Includes a few studied memory ingredients", "60-day guarantee"],
  cons=["Fear-based marketing about Alzheimer's", "35 ingredients means low amounts of each", "Contains iron and vanadium, which most adults don't need to supplement", "Returns required for a refund"],
  verdict="NeuroZoom is essentially a multivitamin with small amounts of memory herbs. It won't prevent or treat Alzheimer's, and the fear-based marketing is a red flag. If you are worried about memory, see a doctor for a check-up, including B12 and thyroid tests; if you want a supplement, a single well-dosed ingredient is easier to judge than a 35-ingredient blend."),

"cleansesana": dict(checked=C, form="capsules", currency="EUR",
  hook="Die 300-Euro-Abnehmspritzen als 69-Euro-Kapsel (the €300 weight-loss injections as a €69 capsule)",
  claim="CleanseSana is a German-language gut-health and weight supplement that claims to activate the body's own GLP-1 production, positioning itself as a natural alternative to weight-loss injections. It is a one-capsule-a-day fiber and probiotic blend.",
  story="Its formula is almost the same as SynoGut's (psyllium, oat bran, flaxseed, glucomannan, apple pectin, black walnut, prune and L. acidophilus), but unlike SynoGut, CleanseSana publishes the amount of each ingredient.",
  ingredients=["psyllium", "oat", "flaxseed", "glucomannan", "apple pectin", "black walnut", "prune", "lactobacillus acidophilus"],
  ing_note="Amounts per capsule from the official page: psyllium husk 103 mg, oat bran 430 mg, flaxseed powder 130 mg, glucomannan 8.5 mg, apple pectin 8.5 mg, black walnut hull 5 mg, prune 5 mg and L. acidophilus 1.5 billion CFU. That adds up to well under 1 g of fiber a day, while the glucomannan studies the page cites used about 3,000 mg a day, roughly 350 times more.",
  use="One capsule a day, according to the official page. After 90 days the seller suggests 1–2 capsules a week for 'maintenance'.",
  packages=[[1, 69, "€9 shipping"], [3, 147, "See order page"], [6, 234, "See order page"]],
  guarantee_days=60,
  bonuses=["21-Tage Turbo-Reinigung Protokoll", "Darm-Gesundheit Ernährungsplan", "Destruktives Rückstau-Phänomen Elimination Guide", "Lebenslange Darm-Reinheit Maintenance"],
  checks=["There is no evidence that fiber capsules raise GLP-1 to anything like the levels produced by injections such as semaglutide.",
          "The cited meta-analysis found glucomannan helped people lose only about 0.8 kg on average, and at doses hundreds of times higher than in CleanseSana.",
          "1.5 billion CFU of L. acidophilus is a reasonable probiotic amount, but no strain is named.",
          "The black walnut (5 mg) and prune (5 mg) amounts are too small to have any effect."],
  pros=["Publishes exact amounts for every ingredient", "Vegetarian capsule, no gelatine", "One capsule a day", "60-day money-back guarantee"],
  cons=["Comparison with weight-loss injections is misleading", "Fiber doses are far below what studies use", "Expensive for under 1 g of fiber a day", "Bonus guides use alarmist language"],
  verdict="CleanseSana deserves credit for publishing its amounts, but those amounts show the problem: less than a gram of fiber a day can't replicate the studies it cites, let alone a GLP-1 injection. A spoonful of psyllium or oat bran costs a fraction of the price and gives a proven dose. Anyone considering weight-loss injections should talk to their doctor rather than look for a capsule substitute."),
}

if __name__ == "__main__":
    for k, v in D.items():
        json.dump(v, open(os.path.join(HERE, k + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(D), "written")
