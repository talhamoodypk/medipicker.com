"""Batch 6 of hand-checked blog data (sources: work/sales/<slug>.txt and .root.txt, checked 2026-11-05)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
C = "2026-11-05"
D = {
"keyslim": dict(checked=C, form="liquid drops",
  hook="Regain Your Confidence And Take Control Of Your Life!",
  claim="KeySlim Drops is a liquid weight-loss supplement that claims to work in 'three unique stages' using a proprietary formula of 24 fat-burning and metabolism ingredients.",
  ingredients=["l-ornithine", "chromium", "eleuthero", "gymnema", "gaba", "l-glutamine", "l-carnitine", "guarana", "raspberry ketone", "green tea", "african mango", "forskolin", "capsicum", "maca", "beta-alanine", "l-arginine", "ginseng"],
  ing_note="The page also lists licorice, grapefruit, grape seed extract and astragalus. With about 24 ingredients in a few drops of liquid, each one can only be present in a very small amount, far below the doses used in studies.",
  packages=[[1, 79, "Shipping extra"], [3, 177, "See order page"], [6, 294, "Free US shipping"]],
  guarantee_days=60,
  bonuses=["1-Day Detox Miracle Guide", "Biohacking Secrets", "Supercharge Your Body"],
  checks=["Raspberry ketones have never been shown to cause weight loss in humans.",
          "Forskolin (coleus) and African mango studies are small and of low quality.",
          "Guarana and green tea add caffeine, which slightly raises energy use; the effect on weight is small.",
          "Many ingredients (beta-alanine, L-arginine, L-ornithine) are sports supplements with no proven fat-loss effect."],
  pros=["Full ingredient list published", "Clear package prices", "60-day money-back guarantee"],
  cons=["24 ingredients in drops means tiny doses", "Several ingredients have no human weight-loss evidence", "Contains caffeine (guarana, green tea)", "'Three stages' claim is marketing, not science"],
  verdict="KeySlim Drops is a 'kitchen sink' formula: lots of popular ingredient names, each almost certainly at a dose too small to matter. Weight loss comes from sustained changes to diet and activity, and for people with obesity, from medical treatments that have strong trial evidence. If you try KeySlim, watch your total caffeine intake."),

"honeyburn": dict(checked=C, form="liquid honey (dropper)",
  hook="Purple Weight Loss Honey Activates Your Metabolic Switch With Incredible Results",
  claim="HoneyBurn is a liquid honey-based weight-loss supplement taken with a dropper. The seller calls it 'the first and only purple honey designed to boost lipase levels'.",
  ingredients=["berberine", "kudzu", "honey", "holy basil", "olive leaf", "bee pollen", "royal jelly", "propolis"],
  ing_note="Amounts are not disclosed. Raw honey is mostly sugar, so the honey base adds a small number of calories with each serving.",
  use="One dropper serving in the morning and one at night, squeezed into the mouth or a drink.",
  packages=[], price_note="HoneyBurn is sold as 1, 3 or 6 bottles with free shipping; totals appear on the order page. The page shows crossed-out 'retail prices' of $79 and $89.",
  guarantee_days=60, refund_note="To get a refund you must send back all bottles, even empty ones.",
  checks=["'Boosting lipase' isn't a recognized way to lose weight; lipase is the enzyme that digests fat in the gut.",
          "Berberine is the only ingredient with modest weight evidence (about 2 kg in meta-analyses at 1–1.5 g a day), and its dose here is unknown.",
          "Kudzu has been studied for reducing alcohol intake, not weight.",
          "Bee pollen, royal jelly and propolis can cause serious allergic reactions in people allergic to bees or pollen."],
  pros=["Contains berberine", "Easy liquid format", "Free shipping", "60-day guarantee"],
  cons=["'Purple honey' and 'lipase switch' claims aren't scientific", "Bee products are an allergy risk", "No amounts", "Refund requires returning all bottles"],
  verdict="HoneyBurn wraps one modestly studied ingredient (berberine) in a honey base with bee products and big marketing claims. People with pollen or bee allergies, diabetes, or who are pregnant should avoid it. For weight loss, there's no shortcut around diet, activity and, where appropriate, medical treatment."),

"tinnitrol": dict(checked=C, form="sublingual spray",
  hook="Take care of your hearing starting today",
  claim="Tinnitrol is an under-the-tongue spray sold to support hearing and relieve ringing in the ears (tinnitus). Its formula is built around brain-chemistry ingredients rather than traditional ear herbs.",
  ingredients=["alpha-gpc", "gaba", "mucuna pruriens", "l-arginine", "l-tyrosine"],
  ing_note="These are the ingredients named and referenced on the website; amounts are not given in text.",
  use="Shake well and spray under the tongue: 2 sprays in the morning and 4 sprays before bed. Hold for 20 seconds, then swallow, and avoid eating or drinking for 30 minutes before and after, according to the seller.",
  packages=[], price_note="The sales page headline reads 'Try One Bottle For Just $179 And Get 3 Free Bonuses', and 6-bottle orders ship free. Check the actual total carefully at checkout. The seller warns that it doesn't refund purchases made on unauthorized sites.",
  guarantee_days=90, refund_note="The seller calls it a 'No Questions Asked' 90-day guarantee.",
  checks=["There is no supplement with good evidence for tinnitus; reviews of ginkgo, zinc and melatonin found little or no benefit.",
          "Mucuna pruriens contains L-dopa, a prescription Parkinson's drug ingredient, which is a powerful compound to take without medical supervision.",
          "The references cited are about Alpha-GPC for Alzheimer's, GABA and L-arginine for exercise, none about tinnitus.",
          "Sublingual sprays absorb some ingredients faster, but there is no evidence this makes them work for hearing."],
  pros=["90-day money-back guarantee", "Clear usage instructions", "Ingredients named"],
  cons=["No evidence for tinnitus", "Contains L-dopa (from mucuna), which interacts with many medicines", "High single-bottle price", "Amounts not disclosed"],
  verdict="Tinnitrol uses neurotransmitter ingredients that have nothing to do with tinnitus research, including L-dopa from Mucuna pruriens, which shouldn't be taken casually. Tinnitus can be helped by hearing aids, sound therapy and CBT-based programs. See a doctor or audiologist, especially if the ringing is in one ear or came on suddenly."),

"glucoflush": dict(checked=C, form="liquid drops",
  hook="This Mayan Cleanse Supports Healthy Blood Sugar Levels",
  claim="GlucoFlush is a liquid 'Mayan cleanse' sold to support healthy blood sugar. The sales page blames 'gut-invaders' for blood sugar problems and weight gain and recommends three to six months of use.",
  story="Its ingredients (fennel, marshmallow root, pumpkin seed, slippery elm, clove, garlic, oregano oil, peppermint oil and papaya seed) are the classic make-up of a herbal 'parasite cleanse', not a blood sugar formula.",
  ingredients=["fennel", "marshmallow root", "pumpkin seed", "slippery elm", "clove oil", "garlic", "oregano oil", "peppermint", "papaya seed"],
  ing_note="Amounts are not disclosed.",
  use="The bottle comes with a dropper; the seller describes taking it as a quick daily dose and recommends using it for at least three to six months.",
  packages=[], price_note="GlucoFlush is sold as 2, 3 or 6 bottles with free shipping on every order; totals appear on the order page. Crossed-out 'retail prices' of $97 and $79 are shown.",
  guarantee_days=60,
  checks=["Intestinal parasites don't cause type 2 diabetes or common blood sugar problems in developed countries.",
          "None of the ingredients has meaningful clinical evidence for lowering blood sugar.",
          "Garlic and oregano oil kill microbes in lab tests; human evidence for 'cleansing' is lacking.",
          "Recommending three to six months before judging results makes it hard to use the 60-day guarantee."],
  pros=["Gentle digestive herbs that most people tolerate", "Free shipping", "60-day money-back guarantee"],
  cons=["Parasite-cleanse formula sold for blood sugar", "'Gut invader' story isn't supported", "No amounts", "Suggested use outlasts the refund window"],
  verdict="GlucoFlush is a herbal parasite cleanse rebranded as a blood sugar product. It won't lower blood sugar in any meaningful way. If your blood sugar is high, get an HbA1c test and work with your doctor; diet, activity, weight loss and medicines like metformin have strong evidence."),
}

if __name__ == "__main__":
    for k, v in D.items():
        json.dump(v, open(os.path.join(HERE, k + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(D), "written")
