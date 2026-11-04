"""Batch 12 of hand-checked blog data (sources: work/sales/<slug>.txt and .root.txt, checked 2026-11-05).

Skipped (kept noindex, not enough facts on the seller's pages): fast-brain-booster, triple-collagen.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
C = "2026-11-05"
D = {
"emperor-s-vigor-tonic": dict(checked=C, form="capsules",
  hook="Supports Men's Virility And Libido",
  claim="Emperor's Vigor Tonic is a once-a-day capsule sold to boost men's energy, virility and libido, using a proprietary formula of 11 plant extracts inspired by Chinese imperial medicine.",
  story="Its 11 ingredients are exactly the same as those of DigestiStart, which is sold for digestion. The formula itself is a traditional Chinese 'kidney yang' tonic, and in TCM that is closer to Emperor's Vigor Tonic's purpose than to DigestiStart's.",
  ingredients=["rehmannia", "cornus", "wild yam", "poria", "cistanche", "dodder seed", "eucommia", "achyranthes", "polygala", "schisandra", "cnidium"],
  ing_note="All ingredients are in a proprietary blend without amounts.",
  use="One capsule a day with plenty of water.",
  packages=[], price_note="Emperor's Vigor Tonic is sold as 2 bottles (+$9.99 shipping), 2+1 bottles or 3+3 bottles with free shipping; totals appear on the order page.",
  guarantee_days=60,
  bonuses=["A bedroom-tips guide"],
  checks=["Cnidium and cistanche are used for libido in TCM, but human trials are almost non-existent.",
          "The same formula is sold elsewhere for digestion, which shows how loosely these products are marketed.",
          "The claim that all ingredients are 'proven to be safe in clinical trials' isn't backed by cited trials.",
          "Imported TCM herbs have sometimes been found contaminated with heavy metals or undeclared drugs."],
  pros=["Traditional formula with a long history in Chinese medicine", "One capsule a day", "60-day guarantee"],
  cons=["Almost no clinical evidence for libido", "Identical formula sold for an unrelated purpose", "Proprietary amounts", "Prices hidden until checkout"],
  verdict="Emperor's Vigor Tonic is a classic Chinese tonic with little modern evidence. It's unlikely to do much for erections or libido. Low libido and erection problems can be linked to low testosterone, diabetes, heart disease or medications, so see a doctor; effective treatments exist."),

"bladdershield": dict(checked=C, form="capsules",
  hook="Adult Diaper Companies Panic As New \"Bladder Leak Trick\" Eliminates Pad Use",
  claim="BladderShield is a capsule sold for bladder leaks and frequent urination, with the promise that users can stop needing pads. It combines D-mannose and cranberry with hibiscus and dandelion.",
  ingredients=["d-mannose", "cranberry", "hibiscus", "dandelion"],
  ing_note="The website lists these ingredients plus a nutrient 'found in fruits like apples and oranges'. Amounts aren't disclosed.",
  use="Two capsules a day with 6–8 oz of water, according to the website.",
  packages=[[1, 69, "Shipping extra"], [3, 177, "Free US shipping"], [6, 294, "Free US shipping"]],
  guarantee_days=90, refund_note="The seller describes a 'DOUBLE Satisfaction Guarantee': a refund within 90 days even for empty bottles, plus an extra $100 'for giving it an honest try'. Read the exact terms before relying on the extra $100.",
  bonuses=["Two free bonus gifts with 3- or 6-bottle orders"],
  checks=["D-mannose and cranberry have evidence for preventing recurrent urinary tract infections, not for bladder leaks or incontinence.",
          "Dandelion and hibiscus have mild diuretic effects, which could increase how often you need to urinate.",
          "Stress incontinence (leaks when coughing or laughing) responds well to pelvic floor exercises; urge incontinence has effective medicines.",
          "'Adult diaper companies panic' is a sensational headline with no source."],
  pros=["Contains D-mannose and cranberry, useful for recurrent UTIs", "Clear package prices", "Long 90-day guarantee"],
  cons=["Ingredients don't treat leaks or incontinence", "Diuretic herbs may worsen urgency", "Sensational marketing", "Amounts not disclosed"],
  verdict="BladderShield could be a reasonable product for preventing urinary infections, but it's sold for something else: leaks. Pelvic floor exercises (ideally with a physiotherapist) cure or improve most stress incontinence, and doctors can treat overactive bladder. See a doctor about new leaks, blood in the urine or pain."),

"fortbite": dict(checked=C, form="tooth powder",
  hook="This Ancient Volcanic Clay Supports Healthy Gums And Teeth",
  claim="FortBite is a tooth powder you put on your toothbrush twice a day instead of, or as well as, toothpaste. It's based on two clays (bentonite and kaolin) with calcium carbonate and herbal flavors.",
  ingredients=["bentonite clay", "kaolin clay", "calcium carbonate", "cinnamon", "clove oil", "peppermint", "myrrh", "ginger"],
  ing_note="It also contains lemon peel and stevia for taste. FortBite does not list fluoride or hydroxyapatite, the two ingredients with the best evidence for preventing cavities.",
  use="Put a small amount of powder on your toothbrush and brush twice a day, morning and night.",
  packages=[], price_note="FortBite is sold in multi-jar packages with free US shipping; totals appear on the order page. International shipping is $15.95.",
  guarantee_days=60, refund_note="The page mentions both a 60-day and a 180-day money-back guarantee; check which applies at checkout. Empty jars can be returned for a refund.",
  checks=["Calcium carbonate is a mild abrasive used in many toothpastes; it helps remove stains and plaque but doesn't rebuild enamel.",
          "Clay 'pulling toxins out' of teeth isn't a recognized dental concept.",
          "Without fluoride, a tooth powder offers less cavity protection than standard toothpaste.",
          "The page discourages professional cleanings as 'expensive and painful', but they remove hardened tartar that brushing can't."],
  pros=["Simple, natural-ingredient tooth powder", "Mild abrasive for stain removal", "Pleasant herbal flavors", "Money-back guarantee"],
  cons=["No fluoride or hydroxyapatite", "Unsupported 'toxin' claims", "Discourages dental cleanings", "Prices hidden until checkout"],
  verdict="FortBite is a basic clay tooth powder. If you use it, keep a fluoride or hydroxyapatite toothpaste in your routine for cavity protection, and keep up regular dental check-ups and cleanings. Bleeding gums are a sign of gum disease that a dentist can treat."),
}

if __name__ == "__main__":
    for k, v in D.items():
        json.dump(v, open(os.path.join(HERE, k + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(D), "written")
