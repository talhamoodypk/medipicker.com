import io, re, os
T = os.path.dirname(os.path.abspath(__file__))
SEAL = re.search(r'<path d="M100\.0 4\.0[^"]*"', io.open(os.path.join(T, "alphafuelpro-graphics.svg"), encoding="utf-8").read()).group(0)
CAP = ('<rect x="54" y="8" width="112" height="46" rx="8" fill="url(#capBody)" stroke="#b9bfc6" stroke-width="1"/>'
       '<g stroke="#b9bfc6" stroke-width="1.5" opacity=".8">' + "".join(f'<line x1="{x}" y1="12" x2="{x}" y2="50"/>' for x in range(66, 147, 16)) + '</g>'
       '<rect x="60" y="54" width="100" height="12" fill="#e4e7eb"/>'
       '<rect x="26" y="64" width="168" height="228" rx="26" fill="url(#bottleBody)" stroke="#c3c8ce" stroke-width="1"/>')
GRADS = ('<linearGradient id="bottleBody" x1="0" x2="1"><stop offset="0" stop-color="#d9dde2"/><stop offset=".45" stop-color="#ffffff"/><stop offset="1" stop-color="#cfd4da"/></linearGradient>'
         '<linearGradient id="capBody" x1="0" x2="1"><stop offset="0" stop-color="#d3d7dc"/><stop offset=".5" stop-color="#ffffff"/><stop offset="1" stop-color="#c9ced4"/></linearGradient>')


def gold(c0, c1, c2):
    return f'<radialGradient id="goldG" cx=".5" cy=".4" r=".6"><stop offset="0" stop-color="{c0}"/><stop offset=".7" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></radialGradient>'


def seal(days, font, ink):
    t = lambda y, size, w, txt, ln: f'<text x="100" y="{y}" text-anchor="middle" font-family="{font}" font-weight="{w}" font-size="{size}" fill="{ink}" textLength="{ln}" lengthAdjust="spacingAndGlyphs">{txt}</text>'
    return (f'<symbol id="seal" viewBox="0 0 200 200">{SEAL} fill="url(#goldG)"/>'
            '<circle cx="100" cy="100" r="70" fill="none" stroke="#ffffff" stroke-opacity=".7" stroke-width="3" stroke-dasharray="4 5"/>'
            + t(88, 30, 800, f"{days}-DAY", 100) + t(113, 19, 700, "MONEY-BACK", 112) + t(137, 19, 700, "GUARANTEE", 104) + '</symbol>')


def tx(x, y, size, txt, fill, font, w=800, ln=None, anchor="middle"):
    l = f' textLength="{ln}" lengthAdjust="spacingAndGlyphs"' if ln else ""
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{font}" font-weight="{w}" font-size="{size}" fill="{fill}"{l}>{txt}</text>'


def write(name, defs):
    io.open(os.path.join(T, name), "w", encoding="utf-8").write(f'<svg width="0" height="0" style="position:absolute"><defs>{defs}</defs></svg>')


IT = "Inter Tight, Arial, sans-serif"
SS = "'Source Sans 3', Arial, sans-serif"
RB = "Roboto, Arial, sans-serif"
J = "Jost, Arial, sans-serif"

# Whispeara: amber glass dropper bottle with white label
write("whispeara-graphics.svg",
      '<linearGradient id="amber" x1="0" x2="1"><stop offset="0" stop-color="#5a2a06"/><stop offset=".4" stop-color="#a65a12"/><stop offset=".6" stop-color="#b8661a"/><stop offset="1" stop-color="#4a2205"/></linearGradient>'
      '<linearGradient id="bulb" x1="0" x2="1"><stop offset="0" stop-color="#111"/><stop offset=".45" stop-color="#3a3a3a"/><stop offset="1" stop-color="#0a0a0a"/></linearGradient>'
      '<linearGradient id="ring" x1="0" x2="1"><stop offset="0" stop-color="#e5e7eb"/><stop offset=".5" stop-color="#ffffff"/><stop offset="1" stop-color="#cbd5e1"/></linearGradient>'
      + gold("#ffe7a3", "#ffc94a", "#d99a00") +
      '<symbol id="bottle" viewBox="0 0 220 300">'
      '<path d="M90 8c0-5 40-5 40 0v52H90z" fill="url(#bulb)"/>'
      '<rect x="80" y="58" width="60" height="30" rx="5" fill="url(#ring)" stroke="#cbd5e1"/>'
      '<g stroke="#cbd5e1" stroke-width="1.2">' + "".join(f'<line x1="{x}" y1="61" x2="{x}" y2="85"/>' for x in range(86, 137, 7)) + '</g>'
      '<path d="M88 88h44v14c0 6 46 12 46 34v142c0 10-8 16-18 16H60c-10 0-18-6-18-16V136c0-22 46-28 46-34z" fill="url(#amber)"/>'
      '<rect x="46" y="140" width="128" height="132" rx="6" fill="#ffffff"/>'
      '<rect x="46" y="140" width="128" height="8" rx="3" fill="#0b5563"/>'
      '<path d="M82 166h10l5-10 7 20 6-14 4 6h8" fill="none" stroke="#22a6b8" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
      '<path d="M128 156a10 10 0 0 1 20 0c0 7-7 8-7 14a5 5 0 0 1-9 2" fill="none" stroke="#0b5563" stroke-width="3.5" stroke-linecap="round"/>'
      + tx(110, 206, 27, "Whispeara", "#0b5563", IT, 800, 112)
      + tx(110, 224, 10, "HEARING SUPPORT", "#0e7490", IT, 700, 96)
      + tx(110, 237, 10, "FORMULA", "#0e7490", IT, 700, 50)
      + tx(110, 262, 9, "1 fl oz (30 ml)", "#475a5e", IT, 600)
      + '</symbol>' + seal(90, IT, "#06323b"))

# SeroBurn: capsule bottle, purple label with orange flame
write("seroburn-graphics.svg", GRADS +
      '<linearGradient id="labelG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3b0f6e"/><stop offset=".55" stop-color="#5b21b6"/><stop offset="1" stop-color="#2e1065"/></linearGradient>'
      '<linearGradient id="flame" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fdba74"/><stop offset="1" stop-color="#ea580c"/></linearGradient>'
      + gold("#ffd7a8", "#fb923c", "#c2410c") +
      f'<symbol id="bottle" viewBox="0 0 220 300">{CAP}'
      '<rect x="26" y="96" width="168" height="170" fill="url(#labelG)"/>'
      '<path d="M110 108c10 12 14 19 14 26a14 14 0 0 1-28 0c0-5 3-9 7-13 0 6 3 9 6 9-3-8-1-15 1-22z" fill="url(#flame)"/>'
      + tx(110, 182, 34, "SERO", "#ffffff", SS, 900, 96)
      + tx(110, 210, 28, "BURN", "#fb923c", SS, 900, 80)
      + '<rect x="56" y="222" width="108" height="18" rx="9" fill="#fb923c"/>'
      + tx(110, 235, 10, "AM · PM FORMULA", "#2e1065", SS, 800, 90)
      + tx(110, 258, 9, "60 CAPSULES", "#ffffff", SS, 700)
      + '</symbol>' + seal(60, SS, "#2e1065"))

# Neuro Serge: white bottle, navy & blue swoosh, brain mark
write("neuroserge-graphics.svg", GRADS +
      '<linearGradient id="swoosh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#38bdf8"/><stop offset="1" stop-color="#0369a1"/></linearGradient>'
      + gold("#ffe7a3", "#f0b429", "#b7860b") +
      f'<symbol id="bottle" viewBox="0 0 220 300">{CAP}'
      '<path d="M26 100h22c-10 40-6 110 30 166H26z" fill="url(#swoosh)" opacity=".9"/>'
      '<path d="M48 100h8c-10 40-6 110 30 166h-8C42 210 38 140 48 100z" fill="#103b55"/>'
      '<g fill="none" stroke="#103b55" stroke-width="3" stroke-linecap="round"><path d="M128 120c-8-8-22-2-20 8-8 2-8 14 0 16 0 8 12 10 16 4 4 6 16 4 16-4 8-2 8-14 0-16 2-10-12-16-20-8"/><path d="M128 122v30"/></g>'
      + tx(128, 186, 28, "NEURO", "#0284c7", RB, 900, 96)
      + tx(128, 214, 28, "SERGE", "#103b55", RB, 900, 96)
      + '<rect x="78" y="224" width="108" height="20" rx="4" fill="#103b55"/>'
      + tx(132, 238, 11, "BRAIN SUPPORT", "#ffffff", RB, 800, 88)
      + tx(132, 262, 9, "60 CAPSULES", "#103b55", RB, 700)
      + '</symbol>' + seal(180, RB, "#103b55"))

# Slim Boost Tea: green stand-up pouch
write("slimboosttea-graphics.svg",
      '<linearGradient id="pouch" x1="0" x2="1"><stop offset="0" stop-color="#14532d"/><stop offset=".45" stop-color="#1f7a4c"/><stop offset=".6" stop-color="#239157"/><stop offset="1" stop-color="#0f3f22"/></linearGradient>'
      '<linearGradient id="leaf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#bef264"/><stop offset="1" stop-color="#65a30d"/></linearGradient>'
      + gold("#fff3b0", "#ffd43b", "#d4a600") +
      '<symbol id="bottle" viewBox="0 0 220 300">'
      '<path d="M40 20h140l-4 236c0 10 10 16 14 24H30c4-8 14-14 14-24z" fill="url(#pouch)"/>'
      '<rect x="40" y="20" width="140" height="10" fill="#0f3f22" opacity=".55"/>'
      '<line x1="44" y1="42" x2="176" y2="42" stroke="#ffffff" stroke-opacity=".35" stroke-width="2" stroke-dasharray="4 3"/>'
      '<circle cx="70" cy="36" r="4" fill="#0f3f22"/>'
      '<path d="M110 66c22 2 32 18 26 40-22-2-32-18-26-40z" fill="url(#leaf)"/><path d="M112 70c6 12 12 22 22 34" stroke="#3f6212" stroke-width="2" fill="none"/>'
      '<path d="M108 74c-18 6-22 22-12 36 16-6 20-22 12-36z" fill="url(#leaf)" opacity=".85"/>'
      + tx(110, 148, 30, "SLIM BOOST", "#ffffff", J, 800, 128)
      + '<rect x="70" y="158" width="80" height="30" rx="15" fill="#ffd43b"/>'
      + tx(110, 180, 22, "TEA", "#14532d", J, 800, 46)
      + tx(110, 212, 9.5, "14-HERB WELLNESS BLEND", "#d9f99d", J, 700, 130)
      + tx(110, 228, 9.5, "LEMON &amp; MINT FLAVOR", "#ffffff", J, 600, 112)
      + tx(110, 256, 9, "LOOSE LEAF HERBAL TEA", "#ffffff", J, 700)
      + '</symbol>' + seal(60, J, "#14532d"))

# BioDentex: white bottle with tooth mark
write("biodentex-graphics.svg", GRADS +
      '<linearGradient id="tooth" x1="0" x2="1"><stop offset="0" stop-color="#7c3aed"/><stop offset=".55" stop-color="#2563eb"/><stop offset="1" stop-color="#38bdf8"/></linearGradient>'
      '<linearGradient id="band" x1="0" x2="1"><stop offset="0" stop-color="#2563eb"/><stop offset="1" stop-color="#7c3aed"/></linearGradient>'
      + gold("#e0f2fe", "#5ec8f2", "#0284c7") +
      f'<symbol id="bottle" viewBox="0 0 220 300">{CAP}'
      '<path d="M78 112c-10 0-14 10-11 20l8 30c1 5 7 5 8 0l5-16h24l5 16c1 5 7 5 8 0l8-30c3-10-1-20-11-20-8 0-10 4-17 4s-9-4-17-4z" fill="none" stroke="url(#tooth)" stroke-width="5" stroke-linejoin="round"/>'
      + tx(43, 200, 30, "BIO", "#0ea5e9", J, 800, 42, "start")
      + tx(89, 200, 30, "DENTEX", "#102a5c", J, 800, 88, "start")
      + '<rect x="40" y="212" width="140" height="3" fill="url(#band)"/>'
      + tx(110, 232, 10.5, "SUPPORTS DENTAL HEALTH", "#102a5c", J, 800, 132)
      + '<rect x="40" y="240" width="140" height="3" fill="url(#band)"/>'
      + tx(110, 262, 10, "30 CAPSULES", "#5b21b6", J, 800)
      + '</symbol>' + seal(180, J, "#102a5c"))
print("ok")
