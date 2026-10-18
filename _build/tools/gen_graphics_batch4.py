import io, re, os
T = os.path.dirname(os.path.abspath(__file__))
SEAL = re.search(r'<path d="M100\.0 4\.0[^"]*"', io.open(os.path.join(T, "alphafuelpro-graphics.svg"), encoding="utf-8").read()).group(0)
CAP = ('<rect x="54" y="8" width="112" height="46" rx="8" fill="url(#capBody)" stroke="#b9bfc6" stroke-width="1"/>'
       '<g stroke="#b9bfc6" stroke-width="1.5" opacity=".8">' + "".join(f'<line x1="{x}" y1="12" x2="{x}" y2="50"/>' for x in range(66, 147, 16)) + '</g>'
       '<rect x="60" y="54" width="100" height="12" fill="#e4e7eb"/>'
       '<rect x="26" y="64" width="168" height="228" rx="26" fill="url(#bottleBody)" stroke="#c3c8ce" stroke-width="1"/>')
GRADS = ('<linearGradient id="bottleBody" x1="0" x2="1"><stop offset="0" stop-color="#d9dde2"/><stop offset=".45" stop-color="#ffffff"/><stop offset="1" stop-color="#cfd4da"/></linearGradient>'
         '<linearGradient id="capBody" x1="0" x2="1"><stop offset="0" stop-color="#d3d7dc"/><stop offset=".5" stop-color="#ffffff"/><stop offset="1" stop-color="#c9ced4"/></linearGradient>')
J = "Jost, Arial, sans-serif"
R = "Roboto Condensed, Arial Narrow, Arial, sans-serif"


def gold(c0, c1, c2):
    return f'<radialGradient id="goldG" cx=".5" cy=".4" r=".6"><stop offset="0" stop-color="{c0}"/><stop offset=".7" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></radialGradient>'


def seal(days, font, ink):
    t = lambda y, size, w, txt, ln: f'<text x="100" y="{y}" text-anchor="middle" font-family="{font}" font-weight="{w}" font-size="{size}" fill="{ink}" textLength="{ln}" lengthAdjust="spacingAndGlyphs">{txt}</text>'
    return (f'<symbol id="seal" viewBox="0 0 200 200">{SEAL} fill="url(#goldG)"/>'
            '<circle cx="100" cy="100" r="70" fill="none" stroke="#ffffff" stroke-opacity=".7" stroke-width="3" stroke-dasharray="4 5"/>'
            + t(88, 30, 800, f"{days}-DAY", 100) + t(113, 19, 700, "MONEY-BACK", 112) + t(137, 19, 700, "GUARANTEE", 104) + '</symbol>')


def write(name, defs):
    io.open(os.path.join(T, name), "w", encoding="utf-8").write(f'<svg width="0" height="0" style="position:absolute"><defs>{defs}</defs></svg>')


write("prostapeak-graphics.svg", GRADS +
      '<linearGradient id="labelG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eaf3fd"/><stop offset="1" stop-color="#9cc8f0"/></linearGradient>'
      + gold("#fff3a8", "#ffe145", "#d4b000") +
      f'<symbol id="bottle" viewBox="0 0 220 300">{CAP}'
      '<rect x="26" y="92" width="168" height="10" fill="#1c3561"/><rect x="26" y="102" width="168" height="160" fill="url(#labelG)"/><rect x="26" y="262" width="168" height="10" fill="#1c3561"/>'
      '<path d="M92 114l18-10 18 10v20l-18 10-18-10z" fill="#2e5693"/><path d="M103 118c0 7 3 12 7 12s7-5 7-12M110 130v8" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/>'
      f'<text x="110" y="176" text-anchor="middle" font-family="{J}" font-weight="800" font-size="31" fill="#1c3561" textLength="120" lengthAdjust="spacingAndGlyphs">PROSTA</text>'
      f'<text x="110" y="198" text-anchor="middle" font-family="{J}" font-weight="800" font-size="20" fill="#2e7fd0" textLength="64" lengthAdjust="spacingAndGlyphs">PEAK</text>'
      f'<text x="110" y="222" text-anchor="middle" font-family="{J}" font-size="9.5" font-weight="700" fill="#1c3561" textLength="136" lengthAdjust="spacingAndGlyphs">PROSTATE &amp; URINARY SUPPORT</text>'
      f'<text x="110" y="250" text-anchor="middle" font-family="{J}" font-size="9" font-weight="700" fill="#1c3561">60 CAPSULES</text></symbol>'
      + seal(180, J, "#1c3561"))

write("sugarmute-graphics.svg", GRADS +
      '<linearGradient id="labelG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7a1712"/><stop offset=".5" stop-color="#c4231b"/><stop offset="1" stop-color="#5e1f1a"/></linearGradient>'
      + gold("#fff3a8", "#ffe145", "#d4b000") +
      f'<symbol id="bottle" viewBox="0 0 220 300">{CAP}'
      '<rect x="26" y="96" width="168" height="170" fill="url(#labelG)"/>'
      '<g fill="#ffffff" opacity=".12"><circle cx="50" cy="120" r="14"/><circle cx="170" cy="240" r="18"/><circle cx="160" cy="118" r="9"/></g>'
      f'<text x="72" y="161" font-family="{J}" font-weight="800" font-size="26" fill="#ffffff" text-anchor="middle" textLength="62" lengthAdjust="spacingAndGlyphs">Sugar</text>'
      f'<rect x="106" y="136" width="80" height="32" rx="4" fill="#ffffff"/><text x="146" y="161" text-anchor="middle" font-family="{J}" font-weight="800" font-size="26" fill="#a01d16">Mute</text>'
      f'<text x="110" y="196" text-anchor="middle" font-family="{J}" font-size="11" font-weight="700" fill="#ffffff" textLength="140" lengthAdjust="spacingAndGlyphs">BLOOD SUGAR SUPPORT</text>'
      f'<text x="110" y="212" text-anchor="middle" font-family="{J}" font-size="8.5" fill="#ffe145" textLength="124" lengthAdjust="spacingAndGlyphs">FIBER · PROBIOTIC · 10 INGREDIENTS</text>'
      f'<text x="110" y="250" text-anchor="middle" font-family="{J}" font-size="9" font-weight="700" fill="#ffffff">60 CAPSULES</text></symbol>'
      + seal(90, J, "#5e1f1a"))

write("glycomute-graphics.svg", GRADS +
      '<linearGradient id="labelG" x1="0" x2="1"><stop offset="0" stop-color="#e8774f"/><stop offset="1" stop-color="#f4a081"/></linearGradient>'
      + gold("#fff3a0", "#fcdd09", "#cfae00") +
      f'<symbol id="bottle" viewBox="0 0 220 300">{CAP}'
      '<path d="M110 104l20 11.5v23L110 150l-20-11.5v-23z" fill="none" stroke="#1f2937" stroke-width="2.5"/>'
      '<path d="M110 114c6 8 9 12 9 16a9 9 0 0 1-18 0c0-4 3-8 9-16z" fill="none" stroke="#1f2937" stroke-width="2.5"/>'
      f'<text x="110" y="186" text-anchor="middle" font-family="{J}" font-weight="700" font-size="30" fill="#1f2937" textLength="132" lengthAdjust="spacingAndGlyphs">GlycoMute</text>'
      f'<text x="110" y="204" text-anchor="middle" font-family="{J}" font-size="10" fill="#374151" textLength="112" lengthAdjust="spacingAndGlyphs">Daily Glucose Support</text>'
      '<rect x="26" y="222" width="168" height="46" fill="url(#labelG)"/>'
      f'<text x="110" y="250" text-anchor="middle" font-family="{J}" font-size="9" font-weight="700" fill="#ffffff" textLength="140" lengthAdjust="spacingAndGlyphs">DIETARY SUPPLEMENT · 30 CAPSULES</text></symbol>'
      + seal(90, J, "#1f2937"))

write("titantransform-graphics.svg",
      '<linearGradient id="body" x1="0" x2="1"><stop offset="0" stop-color="#0b1220"/><stop offset=".5" stop-color="#1e293b"/><stop offset="1" stop-color="#050913"/></linearGradient>'
      '<linearGradient id="pump" x1="0" x2="1"><stop offset="0" stop-color="#94a3b8"/><stop offset=".5" stop-color="#f1f5f9"/><stop offset="1" stop-color="#64748b"/></linearGradient>'
      '<linearGradient id="bolt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7dd3fc"/><stop offset="1" stop-color="#0284c7"/></linearGradient>'
      + gold("#7dd3fc", "#0ea5e9", "#0369a1") +
      '<symbol id="bottle" viewBox="0 0 220 300">'
      '<rect x="100" y="6" width="20" height="16" rx="3" fill="url(#pump)"/><rect x="120" y="10" width="26" height="7" rx="3" fill="url(#pump)"/>'
      '<rect x="94" y="22" width="32" height="30" rx="4" fill="url(#pump)"/><rect x="86" y="52" width="48" height="26" rx="5" fill="#111827"/>'
      '<rect x="56" y="78" width="108" height="216" rx="22" fill="url(#body)"/>'
      '<path d="M118 100l-26 46h20l-8 40 30-52h-20z" fill="url(#bolt)"/>'
      f'<text x="110" y="222" text-anchor="middle" font-family="{R}" font-weight="800" font-size="34" fill="#ffffff" textLength="92" lengthAdjust="spacingAndGlyphs">TITAN</text>'
      f'<rect x="66" y="230" width="88" height="20" fill="#e2e8f0"/><text x="110" y="245" text-anchor="middle" font-family="{R}" font-weight="800" font-size="14" fill="#0b1220" textLength="80" lengthAdjust="spacingAndGlyphs">TRANSFORM</text>'
      f'<text x="110" y="272" text-anchor="middle" font-family="{R}" font-size="9" font-weight="700" fill="#cbd5e1">ORAL SPRAY · 1 FL OZ</text></symbol>'
      + seal(90, R, "#ffffff"))
print("ok")
