"""Batch 3 of hand-checked blog data (sources: work/sales/<slug>.txt and .root.txt, checked 2026-11-05)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
C = "2026-11-05"
D = {
"triple-blood-balance": dict(checked=C, form="capsules",
  hook="Over 1,000,000 Bottles Sold!",
  claim="Triple Blood Balance Formula, made by Triple Naturals, is sold to support healthy blood pressure, blood sugar and cholesterol in one product, with possible help for weight management. The company says it is formulated in Salt Lake City, Utah.",
  ingredients=["berberine", "cinnamon", "mulberry leaf", "chromium", "juniper", "biotin"],
  ing_note="The website names these ingredients but does not show the amounts in text.",
  packages=[], price_note="The order page advertises a '55% off' discount and shows package prices only after you choose a package. Two bonus e-books ('20 Health Foods You Should Never Eat' and '8 Healthy Foods That Cause Flab') are included as digital downloads.",
  made="Formulated in Salt Lake City, Utah in a GMP-verified facility (seller's claim).",
  checks=["Berberine has the strongest evidence here: meta-analyses show it lowers fasting blood sugar, HbA1c and LDL cholesterol, at 900–1,500 mg a day.",
          "Cinnamon and mulberry leaf have small, inconsistent effects on blood sugar.",
          "None of the listed ingredients has good evidence for lowering blood pressure, despite that being a headline claim.",
          "The page suggests it works 'without the nasty side effects you see with statins', which is not a fair comparison: statins prevent heart attacks in trials, and no supplement has shown that."],
  pros=["Includes berberine, a genuinely studied blood sugar ingredient", "Made in a US facility", "Free bonus e-books"],
  cons=["No amounts, so the berberine dose is unknown", "Blood pressure claim not supported by its ingredients", "Statin comparison is misleading", "Prices hidden behind '55% off' banners"],
  verdict="Triple Blood Balance contains one ingredient with real evidence (berberine) plus several weaker ones, but without amounts you can't tell whether the berberine dose is meaningful. Berberine also interacts with diabetes medicine and other drugs, so check with your doctor first, and never use it in place of blood pressure, cholesterol or diabetes medication."),

"endopeak": dict(checked=C, form="capsules",
  hook="Erection Muscle Trick Gets You Hard in 9 Seconds",
  claim="EndoPeak is a male-enhancement capsule sold for stronger, faster erections. It combines traditional 'libido' herbs (horny goat weed, tribulus and tongkat ali) with hawthorn, saw palmetto and magnesium.",
  ingredients=["epimedium", "tribulus", "tongkat ali", "hawthorn", "saw palmetto", "magnesium"],
  ing_note="The sales page lists these ingredients but no amounts. Its reference list also cites studies on DHEA, niacin and folate, though those don't appear in the ingredient list shown.",
  use="One capsule a day, according to testimonials on the sales page (one user takes it with morning coffee). The seller recommends at least three months of use.",
  packages=[[2, 158, "Shipping extra"], [3, 207, "Free US shipping"], [6, 294, "Free shipping"]],
  guarantee_days=60, refund_note="The seller calls it a 'No Questions Asked' guarantee.",
  checks=["No supplement produces an erection 'in 9 seconds'; even prescription PDE5 drugs take 30–60 minutes.",
          "Tongkat ali raised testosterone and improved sexual-function scores in some small trials; evidence is limited but positive.",
          "Tribulus has repeatedly failed to raise testosterone in men, and its effect on erections is unclear.",
          "Horny goat weed's icariin works like a very weak PDE5 inhibitor in the lab; human evidence is minimal."],
  pros=["Contains tongkat ali, the best-studied herb in the blend", "60-day guarantee", "Free shipping on larger packages"],
  cons=["Unrealistic '9 seconds' headline", "No ingredient amounts", "Recommends three months before judging results", "'You save $780' figures are based on a list price it isn't sold at"],
  verdict="EndoPeak uses common libido herbs with mixed evidence and makes a promise no supplement can keep. Erection problems can be an early warning sign of heart disease or diabetes, so it's worth seeing a doctor; prescription treatments are proven and widely available. If you try EndoPeak, use the 60-day guarantee if it doesn't help."),

"visium-plus": dict(checked=C, form="capsules",
  hook="One Simple Way To Maintain A Healthy Vision",
  claim="Visium Plus is sold as a natural formula to support the health of your eyes 'no matter if you are 40 or 80 years old'. The sales page is written as a letter from a creator who says he has researched plants for years.",
  story="When we read the ingredient list, it turned out to be a prostate and urinary formula: saw palmetto, pygeum, plant sterols, stinging nettle, uva ursi, buchu, gravel root, pumpkin seed and juniper. It contains none of the nutrients studied for eye health, such as lutein, zeaxanthin or the AREDS2 vitamin blend.",
  ingredients=["saw palmetto", "pygeum", "plant sterols", "stinging nettle", "uva ursi", "quercetin", "green tea", "lycopene", "goldenseal", "vitamin e", "zinc"],
  ing_note="The full list on the website also includes vitamin B6, copper, selenium, red raspberry, Annona muricata (graviola), cat's claw, broccoli leaf, maitake, reishi, shiitake, juniper, buchu, calcium D-glucarate, pumpkin, burdock, cayenne pepper, gravel root and marshmallow root, 29 ingredients in all, with no amounts.",
  packages=[[1, 69, "Free US shipping"], [3, 177, "Free US shipping"], [6, 294, "Free US shipping"]],
  one_time=True, guarantee_days=60, refund_note="The seller says you can get a refund within 60 days even if you have used the whole bottle.",
  checks=["The ingredient list matches a prostate supplement, not an eye supplement; we found no ingredient with evidence for vision.",
          "The nutrients proven to slow age-related macular degeneration (the AREDS2 formula of vitamins C and E, zinc, copper, lutein and zeaxanthin) are not provided at studied doses.",
          "Uva ursi is meant for short-term use only because of its hydroquinone content.",
          "No study of Visium Plus is cited."],
  pros=["Ingredient list is published", "One-time payment with free US shipping", "60-day guarantee even on empty bottles"],
  cons=["Formula doesn't match its eye-health purpose", "29 ingredients with no amounts", "Contains uva ursi and goldenseal, which aren't suited to long-term daily use", "Only sold on its own website"],
  verdict="Visium Plus is one of the clearest mismatches we've reviewed: an eye-health product whose ingredients are a prostate formula. If you want to protect your eyes, get a dilated eye exam and ask your optometrist whether an AREDS2 supplement suits you. We don't recommend Visium Plus for vision."),
}

if __name__ == "__main__":
    for k, v in D.items():
        json.dump(v, open(os.path.join(HERE, k + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(D), "written")
