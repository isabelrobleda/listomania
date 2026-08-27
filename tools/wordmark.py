"""Turn Archivo Black into the wordmark's outlines.

The logo is outlines, not live text. A logo that depends on a webfont loading is
briefly the wrong logo on every cold visit, and the highlighter swipe is sized
to these exact letterforms — a fallback face would leave the band hanging off
the end of the word.

    npm i --no-save @fontsource/archivo
    python3 tools/wordmark.py > components/Wordmark.tsx
"""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Identity

SRC = "node_modules/@fontsource/archivo/files/archivo-latin-900-normal.woff2"
WORD = "Listomania"
TRACK = -0.03      # em; the tracking that looked right at header size
SIZE = 100         # design size, so the viewBox reads in round numbers

f = TTFont(SRC)
gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]
upm = f["head"].unitsPerEm
scale = SIZE / upm
cap = f["OS/2"].sCapHeight

x, paths = 0.0, []
for ch in WORD:
    g = cmap[ord(ch)]
    pen = SVGPathPen(gs)
    gs[g].draw(TransformPen(pen, Identity.translate(x, 0)))
    if pen.getCommands():
        paths.append(pen.getCommands())
    x += hmtx[g][0] + TRACK * upm

width = (x - TRACK * upm) * scale
top = -cap * scale
pad_x, pad_y = 6, 9

# The swipe: steeper than level and unequal at both ends, because a marker laid
# down by a human hand is neither. A level band reads as a box, not a stroke.
band = (f"M{-pad_x - 5:.1f} {top + 3:.1f} L{width + pad_x + 5:.1f} {top - 7:.1f} "
        f"L{width + pad_x + 1:.1f} 5.0 L{-pad_x - 1:.1f} 13.5 Z")

glyphs = "".join('<path d="%s"/>' % d for d in paths)
viewbox = f"{-pad_x} {top - pad_y:.1f} {width + pad_x * 2:.1f} {-top + pad_y * 2:.1f}"

svg = (
    f'<svg className="wm" viewBox="{viewbox}" xmlns="http://www.w3.org/2000/svg" '
    f'role="img" aria-label="Listomania">'
    f'<path d="{band}" fill="var(--mark-logo, #C9F224)"/>'
    f'<g transform="scale({scale},{-scale})" fill="#0B0B0F">{glyphs}</g>'
    f'</svg>'
)

print("""/**
 * The wordmark: Archivo Black converted to outlines by tools/wordmark.py, with
 * a highlighter swipe behind it. The letters are hard-coded dark rather than
 * var(--ink): they sit on lime in every theme, and cream on lime is unreadable.
 */
export default function Wordmark() {
  return (
    """ + svg + """
  );
}
""")
