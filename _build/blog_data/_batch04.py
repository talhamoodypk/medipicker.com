"""Batch 4 of hand-checked blog data (sources: work/sales/<slug>.txt and .root.txt, checked 2026-11-05)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
C = "2026-11-05"
D = {
"dentasmile-pro": dict(checked=C, form="capsules",
  hook="How To Rebuild Your Teeth & Gums TWICE AS FAST With This Powerful \"Dental Elixir\"",
  claim="DentaSmile Pro is sold as a 'dental elixir' to rebuild teeth and gums. The website describes a proprietary formula of eight antioxidants, minerals, vitamins and herbs.",
  story="The six ingredients it names (chromium, inulin, berberine, cinnamon, bitter melon and banaba) are a typical blood sugar formula. The website itself explains several of them as 'supporting healthy blood sugar levels'. None is a recognized dental ingredient such as fluoride, xylitol or a studied oral probiotic.",
  ingredients=["chromium", "inulin", "berberine", "cinnamon", "bitter melon", "banaba"],
  ing_note="Six of the eight ingredients are named on the website; amounts are not disclosed.",
  packages=[[1, 79, "Small shipping fee"], [3, 177, "See order page"], [6, 294, "Free US shipping"]],
  guarantee_days=60, refund_note="The refund policy asks you to return the product within 60 days of receiving it.",
  checks=["Lost tooth enamel and receded gums cannot be 'rebuilt' by any supplement; enamel does not grow back.",
          "There is a real link between poorly controlled diabetes and gum disease, but that is managed with diabetes care and dental treatment, not a capsule.",
          "Berberine has some lab evidence against oral bacteria, but no clinical trials in capsules for gum health.",
          "The product is described as 'scientifically proven' without citing a single study."],
  pros=["Clear package prices", "60-day guarantee", "Includes berberine, a studied blood sugar ingredient"],
  cons=["Formula is a blood sugar supplement, not a dental one", "'Rebuild your teeth' claim is impossible", "Ingredient amounts hidden", "Return required for refund"],
  verdict="DentaSmile Pro sells a blood sugar formula as a way to rebuild teeth, a promise no supplement can keep. If you have sensitive teeth, bleeding gums or receding gums, a dentist visit, fluoride toothpaste and daily flossing do far more. People with diabetes should also be careful, because berberine, bitter melon and banaba can lower blood sugar alongside their medicine."),

"supranail": dict(checked=C, form="capsules",
  hook="Supports every aspect of nails & feet total wellbeing",
  claim="SupraNail is marketed as an 11-ingredient formula for healthy nails and feet, aimed at people with discolored or brittle toenails.",
  story="Its ingredient list reads like a traditional 'colon cleanse' blend: cascara sagrada bark (a stimulant laxative), prune, fennel, oat bran, licorice, cayenne and Senna auriculata. It contains no antifungal ingredient with evidence against nail fungus.",
  ingredients=["senna auriculata", "cascara sagrada", "oat", "licorice", "pumpkin seed", "cayenne", "fennel", "prune", "green tea", "hops", "vitamin c", "vitamin e"],
  ing_note="The website describes Senna auriculata as a holy plant 'used by Amazonian tribes', but it is actually native to India and Sri Lanka. Amounts for the 11-ingredient blend are not disclosed.",
  packages=[[1, 79, "Small shipping fee"], [3, 177, "Small shipping fee"], [6, 294, "Free US shipping"]],
  guarantee_days=60, refund_note="Refunds require shipping the bottles back to an address in Pinellas Park, Florida.",
  bonuses=["Two bonus e-books (listed at $97 and $127)"],
  checks=["Toenail fungus (onychomycosis) is treated with antifungal medicines; none of SupraNail's ingredients has clinical evidence against it.",
          "Cascara sagrada was removed from US over-the-counter laxatives by the FDA in 2002 because its safety and effectiveness weren't shown.",
          "Vitamin C and E support collagen and skin in general, but don't treat nail infections.",
          "The website calls the formula 'well known for maximum results' but cites no study."],
  pros=["Ingredients are named", "60-day money-back guarantee", "Free shipping on 6 bottles"],
  cons=["Laxative ingredients in a nail product", "No antifungal ingredient", "Factual error about Senna auriculata's origin", "Refund requires returning bottles"],
  verdict="SupraNail is essentially a laxative and digestive herb blend marketed for nails and feet. If you have discolored, thick or crumbly toenails, see a doctor or podiatrist to confirm whether it's fungus; topical and oral antifungals are proven to work. We don't recommend SupraNail, especially for long-term daily use, because of its cascara sagrada content."),

"derma-prime-plus": dict(checked=C, form="capsules",
  hook="5 Easy Tips & Tricks That Will Help You Achieve A Normal Skin Balance",
  claim="Derma Prime Plus is a capsule sold for 'normal skin balance' and clearer skin. Its sales page is written by a 'Dr. Ally Ray', introduced as a hepatologist (liver specialist) from Cleveland, Ohio, whose formula focuses on liver-support herbs.",
  story="The page mixes reasonable skin-care tips (use sunscreen of SPF 30 or above, clean your phone screen) with a pitch for a liver-cleanse formula. We could not find any public record of a hepatologist by that name.",
  ingredients=["chanca piedra", "ginger", "burdock", "beetroot", "artichoke"],
  ing_note="The sales letter names these herbs 'such as' and doesn't publish a full label or amounts.",
  packages=[[1, 69, "Free US shipping"], [3, 177, "Free US shipping"], [6, 294, "Free US shipping"]],
  one_time=True, guarantee_days=60, refund_note="The seller says refunds are given within 60 days even if the bottle is empty.",
  checks=["There's no clinical evidence that liver-cleanse herbs improve acne, dryness or other skin problems.",
          "Chanca piedra is studied mainly for kidney stones; artichoke for digestion and cholesterol.",
          "The 'doctor' behind the product can't be verified.",
          "The page claims restocking would take '8 months' to push larger orders, a common pressure tactic."],
  pros=["Sensible general skin advice on the sales page", "One-time payment with free US shipping", "60-day guarantee"],
  cons=["Liver herbs have no proven skin benefit", "Unverifiable doctor persona", "No full label or amounts", "Scarcity pressure tactics"],
  verdict="Derma Prime Plus pairs good basic skin advice with a liver-herb capsule that has no evidence for skin. The tips themselves (daily sunscreen, gentle cleansing, a clean phone screen) are free and genuinely helpful. For persistent acne, eczema or rosacea, a dermatologist can offer treatments that are proven to work."),

"ultrak9-pro": dict(checked=C, form="liquid drops for dogs",
  hook="These Primal Nutrients Support A Healthy Happy Dog",
  claim="UltraK9 Pro is a liquid supplement for dogs, added to food, sold to support energy, digestion, joints, a healthy weight and a calmer temperament. It contains nine herbs and nutrients in an MCT oil base.",
  ingredients=["burdock", "ashwagandha", "ginseng", "astragalus", "dandelion", "turmeric", "mct oil", "horsetail"],
  ing_note="The website lists nine ingredients in a proprietary formula with no amounts and no dosing by body weight, which is unusual for a pet product. Its ingredient list differs in places from other pages that mention bovine collagen.",
  packages=[], price_note="UltraK9 Pro is sold in 3-, 6- and 12-bottle packages, and the seller says most customers order 6. Totals appear only on the order page. Shipping is free in the US and $15.95 to Canada, the UK, Ireland, Australia and New Zealand.",
  guarantee_days=60,
  bonuses=["A dog-training guide"],
  checks=["None of these herbs has been studied for energy, weight or behavior in dogs; nearly all research is in people or lab animals.",
          "Turmeric has some veterinary research for joint comfort, but curcumin is poorly absorbed without help (the MCT oil base may help slightly).",
          "Horsetail contains thiaminase, an enzyme that destroys vitamin B1 and has caused poisoning in grazing animals.",
          "Ashwagandha and ginseng can affect thyroid function, blood sugar and blood pressure; their safety in dogs is not established."],
  pros=["Liquid format is easy to add to food", "60-day money-back guarantee", "Free US shipping"],
  cons=["No amounts or weight-based dosing", "Little or no canine research for the ingredients", "Horsetail is a questionable ingredient for animals", "Prices hidden until checkout"],
  verdict="UltraK9 Pro applies human herbal supplement ideas to dogs without dog-specific research or dosing. If your dog is low on energy, gaining weight or stiff, a vet check is the best first step, because these can be signs of thyroid disease, arthritis or other treatable problems. Ask your vet before giving any herbal product, especially if your dog takes medication."),
}

if __name__ == "__main__":
    for k, v in D.items():
        json.dump(v, open(os.path.join(HERE, k + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(D), "written")
