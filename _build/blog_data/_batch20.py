"""Batch 20 of hand-checked blog data (sources: work/sales/<slug>.txt and .root.txt, checked 2026-11-05).

Skipped (kept noindex, off-topic for a supplement review site): derila-ergo-pillow, certified-concealed-first.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
C = "2026-11-05"
D = {
"foliprime": dict(checked=C, form="topical scalp balm",
  hook="The Natural Egyptian Balm That Supports Hair Health",
  claim="FoliPrime is a scalp balm massaged into thinning areas twice a day, sold as a natural 'Egyptian balm' for fuller, thicker hair. The seller says it contains 13 plant extracts.",
  ingredients=["turmeric", "capsicum", "lemon oil", "biotin", "hyaluronic acid"],
  ing_note="These are the ingredients named on the website; concentrations aren't disclosed. Several of the cited references are about cancer biology (capsaicin and curcumin in cancer signaling), not hair growth.",
  use="Massage a quarter-sized amount into thinning areas of the scalp twice a day, morning and evening, and run any leftover through your hair.",
  packages=[], price_note="FoliPrime is sold as 1, 3 or 6 bottles with free shipping on every order; totals appear on the order page.",
  bonuses=["Two bonus guides (listed at $55 and $54)"],
  checks=["Topical capsaicin has been explored for hair growth in very small studies; evidence is weak.",
          "Biotin applied to the scalp has no proven effect; biotin only helps hair when you're deficient.",
          "Minoxidil (topical) and, for men, finasteride are the proven, widely available treatments for pattern hair loss.",
          "The claim that all ingredients are 'proven safe in clinical trials' isn't backed by cited trials."],
  pros=["Easy to use", "Free shipping", "Money-back guarantee"],
  cons=["No proven hair-growth ingredient", "Irrelevant cancer references", "Capsicum and essential oils can irritate the scalp", "Concentrations not disclosed"],
  verdict="FoliPrime is a scented scalp balm without a proven hair-growth ingredient. If you're losing hair, a doctor or dermatologist can check for causes such as thyroid problems, iron deficiency or hormonal changes, and recommend treatments like minoxidil that are proven to work."),

"serenity-prime": dict(checked=C, form="capsules",
  hook="One Simple Way To Maintain A Normal Hearing",
  claim="Serenity Prime is a capsule sold to support normal hearing, presented in a letter from 'Adam B. Davis' of Boston and his wife.",
  story="Its ingredients (melatonin, chamomile, lemon balm, passionflower, hops, skullcap, ashwagandha, magnesium and St. John's Wort) are a typical sleep and relaxation formula, not a hearing one.",
  ingredients=["melatonin", "chamomile", "lemon balm", "passionflower", "hops", "skullcap", "ashwagandha", "st. john's wort", "magnesium", "taurine", "goji", "calcium", "vitamin b6"],
  ing_note="The letter names these 'such as'; amounts aren't disclosed.",
  packages=[[1, 69, "Free shipping"], [3, 177, "Free shipping"], [6, 294, "Free shipping"]],
  one_time=True, guarantee_days=60, refund_note="The seller says refunds are given within 60 days even if the bottle is used up.",
  checks=["None of the ingredients has evidence for hearing.",
          "A calming formula might help people sleep despite tinnitus, which is a different benefit from 'normal hearing'.",
          "Melatonin can cause next-day drowsiness, so be careful with driving.",
          "St. John's Wort interacts with many common medicines."],
  pros=["May help relaxation and sleep", "Clear package prices", "60-day guarantee"],
  cons=["Sleep formula sold for hearing", "St. John's Wort interactions", "Melatonin in a daily capsule", "Template sales letter"],
  verdict="Serenity Prime is a sleep blend marketed for hearing. If tinnitus keeps you awake, sound therapy and tinnitus-focused CBT help, and an audiologist can check your hearing. Avoid this formula if you take antidepressants, birth control or blood thinners."),
}

if __name__ == "__main__":
    for k, v in D.items():
        json.dump(v, open(os.path.join(HERE, k + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(D), "written")
