"""Batch 15 of hand-checked blog data (sources: work/sales/<slug>.txt and .root.txt, checked 2026-11-05).

Skipped (kept noindex, no ingredient facts on the seller's pages): fungus-elixir.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
C = "2026-11-05"
D = {
"glucoguard-pro": dict(checked=C, form="capsules",
  hook="I'll Unveil An Ancient Indian Secret For Stabilizing Blood Sugar That Will Show DRASTIC Results In Just 24 Hours!",
  claim="GlucoGuard Pro is a blood sugar capsule promoted with an 'ancient Indian secret' and a promise of drastic results within 24 hours. The sales page is styled as a news report (its web address includes 'msn-reports') and features a named customer story.",
  story="The page also contains a testimonial that refers to a different product name, 'SlimCentric', which suggests the sales copy was reused from another product.",
  ingredients=["mulberry leaf", "cinnamon"],
  ing_note="The page names white mulberry extract and cinnamon (Cinnamomum verum, Ceylon cinnamon) as key ingredients; the full label and amounts aren't shown in text.",
  packages=[[1, 59, "Free shipping"], [3, 147, "Free shipping"], [6, 234, "Free shipping"]],
  guarantee_days=180, refund_note="The seller offers a 6-month (180-day) money-back guarantee.",
  checks=["No supplement produces 'drastic' blood sugar results in 24 hours; diabetes medicines themselves take weeks to show their full effect on HbA1c.",
          "White mulberry can blunt blood sugar spikes after carbohydrate meals in small studies.",
          "Ceylon cinnamon contains less coumarin than cassia, but its effect on blood sugar is small and inconsistent.",
          "News-style pages ('MSN reports') are advertising, not journalism."],
  pros=["Low per-bottle prices compared with similar products", "Free shipping on every package", "Long 180-day guarantee", "Mulberry has some after-meal evidence"],
  cons=["Unrealistic 24-hour claim", "Fake news-style presentation", "Copied testimonial naming another product", "Full ingredient list not shown"],
  verdict="GlucoGuard Pro contains mulberry and cinnamon, which have small effects at best, and its marketing is misleading. If you have diabetes or prediabetes, rely on your doctor's plan, and check your blood sugar if you add any supplement, since mulberry can lower it after meals."),

"purpleburn-pro": dict(checked=C, form="powder or capsules",
  hook="These Kenyan Purple Leaves Support Healthy Weight Loss",
  claim="PurpleBurn Pro is sold as a weight-loss product based on 'Kenyan purple leaves', a reference to purple tea, a tea variety grown in Kenya that is rich in anthocyanins.",
  ingredients=["hibiscus", "oat", "inulin", "mangosteen", "white kidney bean", "cinnamon", "green tea", "bitter melon", "ginger", "turmeric"],
  ing_note="Purple tea itself isn't named in the ingredient list on the website; the purple color theme may come from hibiscus. Amounts aren't disclosed.",
  packages=[], price_note="PurpleBurn Pro is sold in multi-unit packages with free US shipping; totals appear on the order page. International shipping is $15.95.",
  guarantee_days=60,
  bonuses=["A guide to what 'Korean superagers' drink daily", "A Korean spices guide"],
  checks=["Purple tea contains a compound called GHG that is being studied for weight, but research is very early.",
          "White kidney bean extract may slightly reduce carbohydrate absorption; meta-analyses show about 1–2 kg of extra weight loss.",
          "Fiber (oat, inulin) can increase fullness, but only at gram-level doses.",
          "Bitter melon and cinnamon target blood sugar rather than weight."],
  pros=["Includes white kidney bean and fiber", "Free US shipping", "60-day guarantee"],
  cons=["Headline ingredient (purple tea) not clearly listed", "Small effects at best", "Proprietary amounts", "Prices hidden until checkout"],
  verdict="PurpleBurn Pro is a mixed fiber, carb-blocker and herb blend with a catchy 'Kenyan purple leaves' story. Expect small effects at best. Sustainable weight loss depends on diet and activity changes, and doctors can discuss medical options for people who need them."),

"sharpear": dict(checked=C, form="capsules",
  hook="Brain Experiment Uncovers the Root Cause of Hearing Loss, And How You Can Restore Your Hearing Naturally in Less Than 1 Month",
  claim="SharpEar is a once-a-day capsule sold to 'restore your hearing naturally in less than one month', told through the story of the author's wife, Daisy. The sales letter attacks the hearing-aid industry and 'Big Pharma'.",
  ingredients=["ginkgo biloba", "st. john's wort", "bacopa", "vinpocetine", "huperzine a"],
  ing_note="The seller stresses that its ginkgo comes from 'female trees'; there's no evidence that the sex of the tree matters for supplements. Amounts aren't disclosed.",
  use="One vegetable capsule a day with a large glass of water; the seller recommends at least 90 days.",
  packages=[], price_note="The letter anchors the price against '$997' and '$697' figures before revealing the real packages on the order page. Buying 3 bottles adds a free bottle of a mood supplement (BrightMood).",
  checks=["No supplement can restore hearing lost to age or noise, which is caused by loss of inner-ear hair cells.",
          "The ginkgo study cited was in sudden hearing loss, a medical emergency that needs prompt steroid treatment, not a supplement.",
          "Discouraging hearing aids is harmful: untreated hearing loss is linked to faster cognitive decline, and hearing aids help.",
          "St. John's Wort, vinpocetine and huperzine A all carry significant interaction or safety concerns."],
  pros=["Ingredient list published", "Simple once-daily dose"],
  cons=["Promises to restore hearing", "Discourages proven hearing aids", "Several ingredients with safety concerns", "Price anchoring tactics"],
  verdict="SharpEar's promise to restore hearing is false, and its advice against hearing aids could cause real harm. Sudden hearing loss needs same-day medical attention; gradual hearing loss is best managed with a hearing test and, if needed, hearing aids. Avoid this formula if you take antidepressants, blood thinners or birth control."),

"forti-prime": dict(checked=C, form="capsules",
  hook="Support an outbreak-free life",
  claim="Forti Prime is sold to support 'an outbreak-free life', aimed at people with recurring cold sores or herpes outbreaks. Its letter is written by a 35-year-old 'clinical researcher' and a colleague.",
  ingredients=["graviola", "green tea", "ginseng", "vitamin c", "vitamin e", "selenium", "olive leaf", "essiac"],
  ing_note="The letter names these ingredients 'and more'. It refers to the product both as a dropper and as capsules, so check which form you'll receive.",
  packages=[[1, 69, "Free US shipping"]],
  price_note="3- and 6-bottle packages are discounted, with free US shipping; totals appear on the order page.",
  one_time=True, guarantee_days=60, refund_note="The seller says refunds are given within 60 days even if the bottle is used up.",
  checks=["None of the ingredients has been shown to prevent herpes outbreaks in clinical trials.",
          "Essiac tea is a herbal cancer remedy that has failed in studies.",
          "Graviola (soursop) has been linked to nerve damage resembling atypical Parkinson's disease with regular use.",
          "Antiviral medicines (aciclovir, valaciclovir) are proven to reduce outbreaks and transmission."],
  pros=["One-time price with free US shipping", "60-day guarantee"],
  cons=["No evidence for preventing outbreaks", "Graviola safety concern", "Unverifiable author", "Unclear product form"],
  verdict="Forti Prime's ingredients have no proven effect on herpes outbreaks, and graviola carries a neurological safety concern. If you get frequent outbreaks, ask a doctor about suppressive antiviral therapy, which is safe, effective and inexpensive."),
}

if __name__ == "__main__":
    for k, v in D.items():
        json.dump(v, open(os.path.join(HERE, k + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(D), "written")
