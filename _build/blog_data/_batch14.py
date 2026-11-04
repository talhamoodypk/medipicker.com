"""Batch 14 of hand-checked blog data (sources: work/sales/<slug>.txt and .root.txt, checked 2026-11-05).

Skipped (kept noindex, no ingredient facts on the seller's pages): triple-anti-aging-cream.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
C = "2026-11-05"
D = {
"jointgen": dict(checked=C, form="capsules",
  hook="Joint Genesis, from BioDynamix",
  claim="Joint Genesis (sold by BioDynamix) is a joint supplement built around Mobilee, a branded hyaluronic acid matrix from rooster comb, combined with French maritime pine bark and ginger. It's presented by a 'Dr. Weis, M.D.'.",
  ingredients=["mobilee", "pine bark", "ginger"],
  ing_note="The page states an 80 mg dose of Mobilee, the amount used in its trials. Other amounts aren't given in text.",
  packages=[[2, 158, "$9.95 US shipping"], [6, 294, "Free US shipping"]],
  price_note="A single bottle is offered at a 'special one-time price' of $59, and a 3-bottle package is also available.",
  guarantee_days=180, refund_note="The seller offers a 180-day 'empty bottle' guarantee: a full refund even if you've used the whole supply.",
  checks=["Mobilee is one of the few branded joint ingredients with its own placebo-controlled trials, which showed modest improvements in knee pain and function.",
          "The '14 randomized trials' claim includes small and manufacturer-funded studies; independent evidence is more limited.",
          "Pine bark extract (Pycnogenol) has small trials showing reduced knee arthritis pain.",
          "Ginger has modest evidence for arthritis pain."],
  pros=["Uses a branded ingredient at its studied dose", "Supporting ingredients have some trial evidence", "Generous 180-day empty-bottle guarantee", "Clear package prices"],
  cons=["Effects are modest, not 'sprint down the stairs'", "Much of the evidence is manufacturer-funded", "Not suitable for people with chicken or egg allergies (rooster comb source)"],
  verdict="Joint Genesis is one of the better-evidenced joint supplements we've reviewed, thanks to Mobilee at its trial dose. Expect gradual, modest relief. Exercise, weight loss and physical therapy remain the most effective treatments for knee and hip arthritis, and the long guarantee makes it a low-risk trial."),

"all-day-slimming-tea-uk": dict(checked=C, form="loose tea (UK)", currency="GBP",
  hook="Hidden Costa Rican Slimming Tea Recipe Exposed...",
  claim="All Day Slimming Tea is a two-part tea system (a morning tea and an evening tea) sold in the UK in pounds sterling for weight loss, based on a 'hidden Costa Rican recipe'.",
  ingredients=["green tea", "oolong", "ginseng", "garcinia", "ginger", "dandelion"],
  ing_note="The page names these ingredients for the teas; the full blend and amounts aren't given in text. Its references also cite berberine, chromium, hesperidin and rutin studies, though those aren't in the tea ingredient list shown.",
  packages=[], price_note="All Day Slimming Tea is sold as 1-, 3- and 6-month supplies, with free shipping on 3 and 6 months. The page says the 6-month supply works out at £1.63 a day; totals appear on the order page.",
  guarantee_days=60,
  checks=["Green and oolong tea provide caffeine and catechins with small effects on metabolism.",
          "Garcinia cambogia (HCA) didn't produce meaningful weight loss in a well-run trial published in JAMA.",
          "'Losing 4 stone' testimonials and rapid loss 'in the first 2 days' (mostly water) aren't typical.",
          "Some references are blogs (Healthline, Dr Axe) rather than research."],
  pros=["Tea is a pleasant, low-calorie drink", "60-day guarantee", "Free shipping on larger packages"],
  cons=["Weight-loss claims far exceed the evidence", "Garcinia has failed in good trials", "Caffeine from three cups a day adds up", "Full blend not disclosed"],
  verdict="All Day Slimming Tea is ordinary green and oolong tea with a dramatic story. Swapping sugary drinks for tea can help a little, but it won't melt fat. In the UK, the NHS offers free weight management support, and your GP can discuss options."),

"newera-protect": dict(checked=C, form="capsules",
  hook="Scientists Reveal the Shocking Cause of Bladder Leakage...",
  claim="NewEra Protect is a two-capsule daily supplement for women over 40 with bladder leakage and urgency. Its sales page is styled as a 'wellness article' about a scientific breakthrough.",
  ingredients=["boswellia", "horsetail", "sumac", "resveratrol", "zinc", "vitamin d"],
  ing_note="The website says resveratrol, horsetail and sumac 'tone the tissues that support your bladder'. Amounts aren't disclosed.",
  use="Two capsules a day with a glass of water.",
  packages=[[3, 177, "See order page"], [6, 294, "Free US shipping"]],
  price_note="A single bottle is also offered; its price appears on the order page. The 'you save $888' figure compares against a list price it isn't sold at.",
  guarantee_days=60,
  bonuses=["Two bonus guides with the 6-bottle package"],
  checks=["There's no evidence that resveratrol, horsetail or sumac 'tone' the pelvic floor or bladder.",
          "The references cited are about resveratrol and kidney function, which is a different organ and a different problem.",
          "Vitamin D deficiency has been linked to pelvic floor weakness in observational studies, but supplement trials are lacking.",
          "Pelvic floor muscle training is the first-line, proven treatment for stress incontinence in women."],
  pros=["Clear 3- and 6-bottle prices", "60-day guarantee", "Generally well-tolerated ingredients"],
  cons=["No evidence for bladder leakage", "Advertorial-style 'breakthrough' page", "Horsetail isn't suited to long-term use", "Inflated savings claims"],
  verdict="NewEra Protect's ingredients don't match its purpose. Most women with leakage improve with pelvic floor training, ideally guided by a women's health physiotherapist; vaginal estrogen, devices and treatments for overactive bladder also help. Talk to your doctor; it's a common, treatable problem."),

"pawbiotix": dict(checked=C, form="dog supplement (drops)",
  hook="The Natural Formula That Supports Your Dog's Health",
  claim="Pawbiotix is a probiotic supplement for dogs combining gut bacteria with a mix of greens, fiber, liver and collagen. The seller says it suits all breeds, ages and medical conditions.",
  ingredients=["kelp", "chlorella", "turmeric", "fennel", "l-glutamine", "chicory", "flaxseed", "beef liver", "collagen", "sodium copper chlorophyllin"],
  ing_note="The probiotic strains and CFU count aren't listed in text, and there's no dosing guide by body weight.",
  packages=[], price_note="Pawbiotix is sold as 2 bottles (+$9.99 shipping) or 3+3 bottles with free shipping; the order page shows crossed-out totals of $358 and $1,074, with the actual price at checkout.",
  refund_note="For a refund you must send back all bottles, even empty ones.",
  checks=["Dog probiotics with named strains have some evidence for acute diarrhea; Pawbiotix doesn't name its strains.",
          "Kelp adds iodine, which can affect thyroid function in dogs as in people.",
          "The claim that it suits dogs with any medical condition isn't something any supplement can promise.",
          "The claim that all ingredients are 'proven safe in clinical trials' isn't supported by cited trials."],
  pros=["Includes prebiotic fiber and palatable liver", "Money-back guarantee"],
  cons=["Probiotic strains and dose not stated", "No weight-based dosing", "Kelp iodine for dogs with thyroid issues", "Inflated crossed-out prices"],
  verdict="Pawbiotix is a general dog-wellness topper with an unnamed probiotic. If your dog has ongoing digestive problems, see a vet, who can recommend a veterinary probiotic with proven strains, or check for parasites and food intolerance."),
}

if __name__ == "__main__":
    for k, v in D.items():
        json.dump(v, open(os.path.join(HERE, k + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(D), "written")
