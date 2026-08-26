"""Custom Listomania letterforms: a monoline 'marker' alphabet.

Each glyph is a skeleton of strokes drawn with round caps/joins at a heavy
weight — so the letters are literally made the way a marker makes them.
That ties the sticker (route 01) and the highlighter (route 05) together
honestly, instead of bolting one onto the other.
"""

# baseline 78, x-height top 34, cap top 12, dot centre 15
G = {
 "L": (60, ['M13 12 V78 H52']),
 "i": (26, ['M13 32 V78'], [(13, 12)]),
 "s": (64, ['M51 41 C51 31 40 27 31 27 C19 27 12 33 12 41 C12 56 51 51 51 67 '
            'C51 77 41 83 30 83 C18 83 11 77 11 68']),
 "t": (50, ['M24 10 V62 C24 78 34 82 44 78', 'M7 32 H43']),
 "o": (80, ['M13 55 C13 37 26 27 40 27 C54 27 67 37 67 55 C67 73 54 83 40 83 '
            'C26 83 13 73 13 55 Z']),
 "m": (122, ['M13 78 V33',
             'M13 50 C13 35 25 27 34 27 C47 27 56 36 56 52 V78',
             'M56 50 C56 35 68 27 77 27 C90 27 99 36 99 52 V78']),
 # Single-storey 'a': a full bowl plus a stem. The old double-storey shape gave
 # the counter only half the x-height, which closes up entirely at this weight.
 "a": (84, ['M13 55 C13 38 25 28 36 28 C47 28 59 38 59 55 C59 72 47 82 36 82 '
            'C25 82 13 72 13 55 Z',
            'M59 28 V78']),
 "n": (74, ['M13 78 V33', 'M13 50 C13 35 26 27 36 27 C49 27 59 36 59 52 V78']),
}

WORD = "Listomania"
SP = 4           # sidebearing between glyphs
W_OUT = 33       # black outline weight
W_IN = 23        # inner (paper) weight
PAD = 28


def build(word=WORD):
    x = PAD
    outline, inner, dots = [], [], []
    for ch in word:
        w, strokes, *rest = G[ch]
        for d in strokes:
            outline.append((x, d))
            inner.append((x, d))
        for (dx, dy) in (rest[0] if rest else []):
            dots.append((x + dx, dy))
        x += w + SP
    return outline, inner, dots, x - SP + PAD


def svg(fg="#FFFFFF", shadow="#FF2E88", ink="#0B0B0F", shadow_dx=7, shadow_dy=8):
    outline, inner, dots, width = build()
    height = 78 + PAD + 14

    def layer(items, dotitems, stroke, w, dx=0, dy=0):
        out = [f'<g transform="translate({dx},{dy})" fill="none" stroke="{stroke}" '
               f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">']
        for x, d in items:
            out.append(f'<path transform="translate({x},0)" d="{d}"/>')
        out.append('</g>')
        for cx, cy in dotitems:
            out.append(f'<circle cx="{cx+dx}" cy="{cy+dy}" r="{w/2:.1f}" fill="{stroke}"/>')
        return "".join(out)

    # The viewBox has to allow for half the stroke weight bleeding past every
    # skeleton endpoint, plus the offset shadow. Sizing it to the skeleton alone
    # clips the tops of the letters and the right edge of the shadow.
    half = W_OUT / 2 + 3
    top_y, bottom_y = 10, 83          # highest and lowest points in any glyph
    x0 = -half
    y0 = top_y - half
    vw = width + half * 2 + shadow_dx
    vh = (bottom_y + half + shadow_dy) - y0

    return (
        f'<svg viewBox="{x0:.1f} {y0:.1f} {vw:.1f} {vh:.1f}" '
        f'xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="Listomania">'
        + layer(outline, dots, shadow, W_OUT, shadow_dx, shadow_dy)
        + layer(outline, dots, ink, W_OUT)
        + layer(inner, dots, fg, W_IN)
        + '</svg>'
    )


if __name__ == "__main__":
    open("wordmark.svg", "w").write(svg())
    print("width x height:", build()[3])
