"""MediPicker editorial ratings (1–5), shown on every review and marked up as a schema.org Review.

Rubric (published on /how-we-review), each criterion scored and combined into one overall rating:
  1. Evidence: does research support the product's main claim at the doses provided?
  2. Transparency: is the full label with amounts published?
  3. Safety: interaction or safety concerns with the ingredients.
  4. Value & terms: price, billing, refund window and refund conditions.
Ratings follow each page's written verdict; update both together.
"""

# Blog reviews on medipicker.com/blog/<slug>/
BLOG = {
  # Better-evidenced formulas
  "jointgen": 3.5, "titanflow": 3.5,
  "sciaticyl": 3.0, "kerassentials": 3.0, "synaptigen": 3.0, "neurotest": 3.0,
  "synadentix": 2.5, "brain-memory-keeper": 2.5, "nervesana": 2.5, "terracalm": 2.5, "marineflex-ultra": 2.5,
  # Some plausible ingredients, weak doses or overstated claims
  "cleansesana": 2.0, "metabosana": 2.0, "triple-blood-balance": 2.0, "bladdershield": 2.0, "vitrafoxin": 2.0,
  "tonicgreens": 2.0, "glucosana": 2.0, "artivorin": 2.0, "prostastream": 2.0, "glucotrust-german": 2.0,
  "genesis-revival": 2.0, "refirmance": 2.0, "fitspresso": 2.0, "synogut": 2.0, "optiplax": 2.0,
  "powerbite": 2.0, "dentitox-pro": 2.0, "fortbite": 1.5, "honeyburn": 1.5, "glucoguard-pro": 1.5,
  "purpleburn-pro": 1.5, "triple-liver-health": 2.0, "endopeak": 2.0, "hydracellum": 1.5, "flush-factor-plus": 1.5,
  "vidacalm": 1.5, "keyslim": 1.5, "glycofortin": 1.5, "fluxactive": 1.5, "protoflow": 1.5, "all-day-slimming-tea-uk": 1.5,
  "primebiome": 1.5, "neotonics": 1.5, "pawbiotix": 1.5, "ultrak9-pro": 1.5, "emperor-s-vigor-tonic": 1.5,
  "aquapeace": 1.5, "memo-max-pro": 1.5, "newera-protect": 1.5, "eyefortin": 1.5, "prostadine": 1.5,
  "flowforce-max": 1.5, "vital-flow": 1.5, "hidragenix": 1.5, "triple-fungus-blast": 1.5, "derma-prime-plus": 1.5,
  "audifort": 1.5, "tinnitrol": 1.5, "promind-complex": 1.5, "memodefend": 1.5, "neurozoom": 1.5, "vertiaid": 1.5,
  # Formula doesn't match the claim, formula hidden, or misleading/unsafe marketing
  "vivogut": 1.0, "visium-plus": 1.0, "claritox-pro": 1.0, "metaglucent": 1.0, "goldalign": 1.0, "quietum-plus": 1.0,
  "supranail": 1.0, "dentasmile-pro": 1.0, "sharpear": 1.0, "free-sugar-pro": 1.0, "lungora": 1.0, "revanail": 1.0,
  "glucoflush": 1.0, "cleanest-body": 1.0, "mycosyn-pro": 1.0, "keravita-pro": 1.0, "keragenis": 1.0,
  "digestistart": 1.0, "nerve-soothe": 1.0, "forti-prime": 1.0, "serenity-prime": 1.0, "foliprime": 1.0,
}

# In-depth reviews on <sub>.medipicker.com
SUB = {
  "glucoarmor": 3.0, "dentavive": 3.0, "trimology": 3.0, "alphafuelpro": 3.0,
  "glycomute": 2.5, "glucoextend": 2.5, "visiflora": 2.5, "vigorsana": 2.5, "seroburn": 2.5, "nervealive": 2.5,
  "cellucare": 2.5, "biodentex": 2.0, "fastleanpro": 2.0, "flashburn": 2.0, "gelatinesculpt": 2.0, "prostapeak": 2.0,
  "neuroserge": 2.0, "sugarmute": 2.0, "whispeara": 1.5, "sonovive": 1.5, "slimboosttea": 1.5, "arterisplus": 1.5,
  "titantransform": 1.0, "titanflow": 3.5,
}

# Written verdicts for the three oldest sub-sites that had pros/cons but no verdict paragraph.
SUB_VERDICT = {
  "cellucare": "CelluCare is a broad blood sugar support formula with some ingredients that have modest research behind them, such as berberine and cinnamon, but the proprietary blend means you can't see the doses. It may offer gentle support alongside healthy habits; it isn't a substitute for diabetes care. Check with your doctor first if you take glucose-lowering medicine.",
  "gelatinesculpt": "Gelatine Sculpt packages the popular 'gelatin trick' with green tea, turmeric and berberine. Gelatin can help you feel full, and green tea and berberine have small effects in studies, but expect gradual, modest results rather than dramatic weight loss. It works best as one part of a calorie-controlled diet and regular activity.",
  "trimology": "Trimology is one of the more interesting gut-health formulas we've reviewed: it combines prebiotic fibers with named probiotic strains, including Akkermansia, an area of promising early research. The evidence for weight loss is still early, and results vary. The 180-day guarantee gives you plenty of time to judge it.",
}


def label(score):
    return {5.0: "Excellent", 4.5: "Very good", 4.0: "Good", 3.5: "Above average", 3.0: "Average", 2.5: "Below average",
            2.0: "Weak", 1.5: "Poor", 1.0: "Not recommended"}[score]
