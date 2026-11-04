"""Batch 19 of hand-checked blog data (sources: work/sales/<slug>.txt and .root.txt, checked 2026-11-05).

Skipped (kept noindex, no ingredient facts on the seller's pages): dentivive.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
C = "2026-11-05"
D = {
"hidragenix": dict(checked=C, form="liquid drops",
  hook="One Simple Way To Maintain A Healthy Weight!",
  claim="Hidragenix is a liquid dropper sold for weight loss, described as targeting 'even the deepest, most hardened fat layers'. Its letter is written by an author who says weight has been their 'number one enemy' for 30 years.",
  ingredients=["capsicum", "forskolin", "grape seed", "gymnema", "green tea"],
  ing_note="The letter names five plant extracts; amounts aren't disclosed.",
  packages=[[1, 69, "Free shipping"]],
  price_note="3- and 6-bottle packages are discounted, with free shipping; totals appear on the order page.",
  one_time=True, guarantee_days=60, refund_note="The seller says refunds are given within 60 days even if the bottle is used up.",
  checks=["No supplement selectively targets 'hardened fat layers'.",
          "Forskolin and capsicum have weak, small-trial evidence for weight.",
          "Green tea adds caffeine with a small effect on energy use.",
          "The letter follows a template shared with several other $69 products."],
  pros=["Short, simple ingredient list", "One-time price with free shipping", "60-day guarantee"],
  cons=["'Hardened fat' claim is unfounded", "Weak evidence for every ingredient", "Amounts not disclosed"],
  verdict="Hidragenix is a small fat-burner blend with no ingredient that meaningfully changes body weight. Sustainable weight loss comes from diet, activity and sleep, and medical treatment is available for people who need it."),

"triple-fungus-blast": dict(checked=C, form="capsules",
  hook="Over 1,000,000 Bottles Sold!",
  claim="Triple Fungus Blast, from Triple Naturals, is a capsule sold for antifungal and antibacterial support and healthy toenails.",
  story="The page uses the same '1,000,000 bottles sold' claim and layout as the company's Triple Blood Balance formula.",
  ingredients=["green tea", "garlic", "turmeric", "olive leaf", "pomegranate"],
  ing_note="These are described as immune-supporting ingredients; amounts aren't disclosed.",
  packages=[], price_note="Prices appear after choosing a package under a '55% off' banner.",
  checks=["None of the ingredients is an antifungal medicine or has clinical evidence against nail fungus.",
          "Garlic compounds (ajoene) have been tested topically on skin fungus, not as capsules for nails.",
          "The '1,000,000 bottles' claim appears identically on another product's page.",
          "Nail fungus needs months of targeted treatment to clear."],
  pros=["Made by an established US supplement brand", "Generally well-tolerated ingredients"],
  cons=["No antifungal ingredient", "Recycled sales claims", "No amounts", "Prices hidden behind discount banners"],
  verdict="Triple Fungus Blast is a general antioxidant capsule. It won't clear nail fungus. A podiatrist or doctor can confirm the infection and offer topical or oral antifungals that work."),

"mycosyn-pro": dict(checked=C, form="capsules",
  hook="Simple Indian Ritual Flushes Away Nail Fungus In Seconds",
  claim="Mycosyn Pro is a capsule sold to 'flush away nail fungus in seconds'. Its letter is written by an author who says they worked at a Chicago dermatology clinic, together with a research colleague.",
  story="The ingredients it names (horsetail, saw palmetto, fo-ti, spirulina, biotin, folate, alfalfa and barley grass) are a typical hair-loss formula, not an antifungal one.",
  ingredients=["horsetail", "saw palmetto", "fo-ti", "spirulina", "vitamin c", "folate", "biotin", "alfalfa", "barley grass"],
  ing_note="The letter names these ingredients 'and more'; amounts aren't disclosed.",
  packages=[[1, 69, "Free shipping"]],
  price_note="3- and 6-bottle packages are discounted, with free shipping; totals appear on the order page.",
  one_time=True, guarantee_days=60, refund_note="The seller says refunds are given within 60 days even if the bottle is used up.",
  checks=["Nothing clears nail fungus 'in seconds'; even prescription treatment takes months while the nail grows out.",
          "None of the ingredients has antifungal evidence for nails.",
          "Fo-ti (He Shou Wu) has been linked to liver injury in several countries.",
          "The author and colleague can't be verified."],
  pros=["One-time price with free shipping", "60-day guarantee"],
  cons=["Hair formula sold for nail fungus", "Impossible 'in seconds' claim", "Fo-ti liver risk", "Unverifiable author"],
  verdict="Mycosyn Pro doesn't contain anything that treats nail fungus, and fo-ti carries a liver risk. See a doctor or podiatrist for proven antifungal treatment."),

"promind-complex": dict(checked=C, form="capsules",
  hook="6 Simple Memory Techniques Anyone Can Try Today",
  claim="ProMind Complex is a memory capsule sold through a letter from 'Carl Henderson', introduced as a professor of psychology in Austin, Texas, who shares six memory techniques before introducing the formula.",
  story="Its five named ingredients (huperzine A, ginkgo, vinpocetine, St. John's Wort and bacopa) are exactly the same as SharpEar's, which is sold for hearing.",
  ingredients=["huperzine a", "ginkgo biloba", "vinpocetine", "st. john's wort", "bacopa"],
  ing_note="The letter names these 'and many others'; amounts aren't disclosed.",
  packages=[[1, 69, "Free shipping"]],
  price_note="3- and 6-month packages bring the cost down to about $1.63 a day ($49 a bottle), according to the letter.",
  guarantee_days=60, refund_note="The seller offers an empty-bottle guarantee: a refund within 60 days even if all bottles are used.",
  checks=["Some of the memory techniques (using several senses, staying hydrated, avoiding alcohol) are reasonable.",
          "Bacopa has modest trial evidence for memory; ginkgo didn't prevent dementia in the large GEM trial.",
          "Vinpocetine carries an FDA warning about pregnancy, and huperzine A acts like a prescription drug.",
          "St. John's Wort interacts with many common medicines."],
  pros=["Sensible memory tips", "Includes bacopa", "Empty-bottle guarantee"],
  cons=["Several ingredients with safety concerns", "Same formula sold for hearing", "Unverifiable professor", "Amounts not disclosed"],
  verdict="ProMind Complex combines one modestly useful herb (bacopa) with several that raise safety and interaction concerns. If you take antidepressants, blood thinners or birth control, or could become pregnant, avoid it. A doctor can check for treatable causes of memory problems."),
}

if __name__ == "__main__":
    for k, v in D.items():
        json.dump(v, open(os.path.join(HERE, k + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(D), "written")
