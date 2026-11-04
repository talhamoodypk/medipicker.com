"""Batch 5 of hand-checked blog data (sources: work/sales/<slug>.txt and .root.txt, checked 2026-11-05)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
C = "2026-11-05"
D = {
"refirmance": dict(checked=C, form="topical serum (drops)",
  hook="The Natural \"Lift Serum\"",
  claim="ReFirmance is a facial serum applied as drops to the face and neck, sold to support collagen and firmer, less saggy skin. The sales page says it has a proprietary formula of 17 skin-supporting ingredients.",
  story="The sales story says collagen fragments 'jam' an enzyme called HAS2, so hyaluronic acid pools in the skin and causes sagging. HAS2 (hyaluronan synthase 2) is a real enzyme, but this sagging explanation is a simplification that isn't established in dermatology research.",
  ingredients=["palmitoyl oligopeptide", "chrysin", "micrococcus lysate", "aloe vera", "cucumber", "glycerin"],
  ing_note="The ingredient list also shows deionized water, carbomer (a thickener) and phenoxyethanol (a preservative), which is a standard cosmetic serum base. Concentrations are not disclosed.",
  use="Apply a few drops to the face and neck twice a day, morning and evening, and massage or tap in until absorbed.",
  packages=[], price_note="ReFirmance is sold as 1, 3 or 6 bottles with free shipping on every order; totals appear only on the order page. The seller says most customers order six bottles.",
  bonuses=["Two free bonus guides (listed at $55 and $54)"],
  checks=["Palmitoyl peptides (as in Matrixyl) have small studies showing modest improvements in fine lines; effects are far smaller than retinoids or professional treatments.",
          "Chrysin is sometimes included for under-eye puffiness, with very limited evidence.",
          "No serum can 'lift' sagging skin the way the name suggests; sagging is caused by loss of collagen, fat and bone structure over time.",
          "The claim that all ingredients 'have been proven to be safe in clinical trials' isn't backed by any cited trial of the product."],
  pros=["Contains a peptide used in mainstream anti-aging skincare", "Easy twice-daily routine", "Free shipping on all packages", "Ingredient list is published"],
  cons=["Proprietary concentrations", "'Lift serum' overstates what a topical product can do", "Simplified HAS2 sagging story", "Prices hidden until checkout"],
  verdict="ReFirmance is a fairly ordinary peptide serum marketed with a dramatic scientific-sounding story. It may help skin feel more hydrated, but don't expect a lift. A daily sunscreen and a retinoid (tretinoin or retinol) have far stronger evidence for firmer, smoother skin. Patch-test any new serum on a small area first."),

"terracalm": dict(checked=C, form="topical clay (jar)",
  hook="This French Antifungal Mineral Mud Supports Healthy Toenails",
  claim="Terracalm is a mineral mud applied to the toenails and feet, based on French green clay mixed with essential oils, sold to support healthy-looking toenails and to soothe itchy feet.",
  ingredients=["french green clay", "tea tree", "oregano oil", "thyme oil", "lavender", "clove oil", "manuka honey", "aloe vera", "vitamin e"],
  ing_note="The jar also contains cedarwood essential oil, bearberry extract, jojoba oil, shea butter and menthol. Amounts are not disclosed.",
  packages=[], price_note="Terracalm is sold in multi-jar packages; totals appear only on the order page. Shipping is free in the US and $15.95 to Canada, the UK and Australia.",
  guarantee_days=60, refund_note="To get a refund within 60 days you must send back all jars, including empty ones.",
  checks=["Tea tree oil has the best evidence here: one older trial found 100% tea tree oil worked about as well as clotrimazole cream for toenail fungus, though both cleared only a minority of nails.",
          "Thyme and oregano oils kill fungi in lab dishes, but there are no good clinical trials on toenails.",
          "Clay has no proven antifungal effect on nails; the 'starving the fungus' explanation on the sales page isn't backed by research.",
          "Topical products struggle to reach fungus under the nail; prescription topical and oral antifungals still have the best cure rates."],
  pros=["Contains tea tree oil, which has some trial evidence", "Soothing, moisturizing base (shea, jojoba, aloe)", "Free US shipping", "60-day guarantee"],
  cons=["Concentrations of active oils not disclosed", "Clay has no proven antifungal effect", "Refund requires returning all jars", "Prices hidden until checkout"],
  verdict="Terracalm is a pleasant foot mask with one ingredient (tea tree oil) that has some evidence against nail fungus, but it's unlikely to clear an established infection. Get a nail sample tested to confirm fungus first; if it is, ask about prescription topical solutions such as efinaconazole or oral terbinafine. Essential oils can irritate skin, so test a small area first."),

"audifort": dict(checked=C, form="liquid drops",
  hook="Take care of your hearing starting today",
  claim="Audifort is a liquid supplement sold to support and 'shield' hearing health. It is taken as a dropper under the tongue or in a drink.",
  ingredients=["maca", "grape seed", "green tea", "capsicum", "gymnema", "gaba"],
  ing_note="The website lists these as the main ingredients and offers a label image; amounts are not given in text. Several of them (gymnema, green tea and capsicum) are more typical of blood sugar or weight formulas than hearing products.",
  use="One full dropper a day, under the tongue or mixed into water or juice, according to the website. The seller recommends at least four months of use.",
  packages=[], price_note="Audifort is sold in 1-, 3- and 6-bottle packages, with free shipping on 6 bottles; totals appear on the order page.",
  guarantee_days=90, refund_note="The seller calls it a 'No Questions Asked' 90-day guarantee.",
  checks=["None of Audifort's ingredients has clinical evidence for improving hearing or tinnitus.",
          "Hearing loss from age or noise damage involves loss of inner-ear hair cells, which no supplement has been shown to restore.",
          "Grape seed and green tea antioxidants have been studied for ear protection only in animals.",
          "The references cited are general reviews (such as B vitamins and the brain), not studies of the product."],
  pros=["90-day refund window, longer than most", "Liquid form for people who dislike capsules", "Label image is available"],
  cons=["No ingredient with evidence for hearing", "Blood sugar herbs (gymnema) in a hearing product", "Recommends four months of use before judging", "Amounts not given in text"],
  verdict="Audifort's ingredients don't match its hearing promise, and no supplement has been shown to reverse hearing loss. If you notice hearing changes or ringing in the ears, see a doctor or audiologist; earwax, infections and medication side effects are treatable, and hearing aids help a great deal. If you try Audifort, the 90-day guarantee gives you time to ask for a refund."),

"revanail": dict(checked=C, form="capsules",
  hook="This breakthrough solution helps your immune system identify, lock on, and kill the fungus",
  claim="RevaNail is a capsule sold for toenail fungus. The sales page links nail fungus to blood sugar 'compromised by a hidden problem' and says the formula helps the immune system find and kill fungus from the inside.",
  ingredients=["cinnamon", "gymnema", "green tea", "theobromine"],
  ing_note="The website names cinnamon, gymnema, green tea and theobromine plus 'a powerful blend of vitamins and minerals', without amounts.",
  packages=[[2, 138, "$9.99 US shipping"], [3, 177, "Free US shipping"], [6, 294, "Free US shipping"]],
  guarantee_days=60, refund_note="The seller calls it a 'no-questions-asked' guarantee.",
  checks=["People with diabetes do get nail fungus more often, but blood sugar herbs have never been shown to treat fungal nail infections.",
          "None of the named ingredients is an antifungal medicine or has trial evidence against nail fungus.",
          "The 'immune system locks on and kills the fungus' claim isn't supported by any study of the product.",
          "List prices of $447 and $894 are shown crossed out, but the product isn't sold at those prices."],
  pros=["Clear package prices", "Free US shipping on 3 and 6 bottles", "60-day money-back guarantee"],
  cons=["Blood sugar formula sold as a nail fungus treatment", "No antifungal ingredient", "Inflated 'was' prices", "Amounts not disclosed"],
  verdict="RevaNail is a blood sugar supplement marketed to people with toenail fungus. It won't kill nail fungus. If you have diabetes and nail changes, see your doctor or podiatrist: proven antifungal treatments exist, and good blood sugar control and foot care matter for your overall health."),
}

if __name__ == "__main__":
    for k, v in D.items():
        json.dump(v, open(os.path.join(HERE, k + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(D), "written")
