#!/usr/bin/env python3
"""Neofetch-style terminal panel for the profile README.

Left: an order book ladder (what lobster simulates). Right: key/value rows with
dot leaders. SVG so it can carry colour and a monospace grid markdown can't.
Two variants so the README switches on prefers-color-scheme.

Layout: the two columns are positioned INDEPENDENTLY at fixed x offsets rather
than padded into one shared character grid. Block-drawing glyphs (U+258C etc.)
do not always advance one cell, so character-count padding cannot be trusted to
keep a second column clear; fixed offsets can.
"""
from __future__ import annotations

import pathlib

FS = 14
CH = 9.0          # conservative advance for 14px monospace (real ~8.4)
LH = 22
PAD_X, PAD_TOP = 24, 36
INFO_X = 296      # left edge of the right-hand column, px

THEMES = {
    "dark": dict(bg="#0d1117", stroke="#30363d", key="#58a6ff", val="#c9d1d9",
                 dim="#6e7681", bid="#3fb950", ask="#f85149", dots="#373e47",
                 accent="#d29922"),
    "light": dict(bg="#ffffff", stroke="#d0d7de", key="#0969da", val="#1f2328",
                  dim="#8c959f", bid="#1a7f37", ask="#cf222e", dots="#c9d1d9",
                  accent="#9a6700"),
}

ROWS = [
    ("School",   "Georgia Tech, Math & Computing"),
    ("Work",     "Growth engineering @ Slashy (YC S25)"),
    ("Research", "ML @ MIT, Collective Intelligence"),
    ("Before",   "Wharton, DECA ICDC x2, SIG Discovery"),
    (None, None),
    ("Building", "order books, vol surfaces, autodiff"),
    ("Stack",    "Python, NumPy, C, TypeScript"),
    ("Contact",  "kushagra@gatech.edu"),
]

BOOK = [("ask", "100.04", 3), ("ask", "100.03", 6), ("ask", "100.02", 4),
        ("mid", "", 0),
        ("bid", "100.00", 7), ("bid", "99.99", 4), ("bid", "99.98", 2)]

KEY_W = max(len(k) for k, _ in ROWS if k)
VAL_W = max(len(v) for _, v in ROWS if v)
BODY = max(len(BOOK), len(ROWS))

W = int(INFO_X + (KEY_W + 4 + VAL_W) * CH + PAD_X)
H = int(PAD_TOP + (BODY + 1) * LH + 12)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(theme: str) -> str:
    t = THEMES[theme]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-size="{FS}" '
         f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,'
         f'&quot;Liberation Mono&quot;,monospace">',
         f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" '
         f'fill="{t["bg"]}" stroke="{t["stroke"]}"/>']

    def y(n): return PAD_TOP + n * LH

    # divider between the columns
    rx = INFO_X - 26
    o.append(f'<line x1="{rx}" y1="{y(0)-16}" x2="{rx}" y2="{y(BODY)+6}" '
             f'stroke="{t["stroke"]}"/>')

    # ---- headers
    o.append(f'<text x="{PAD_X}" y="{y(0)}" fill="{t["dim"]}">ORDER BOOK</text>')
    o.append(f'<text x="{INFO_X}" y="{y(0)}" xml:space="preserve">'
             f'<tspan fill="{t["accent"]}">kush</tspan>'
             f'<tspan fill="{t["dim"]}">@</tspan>'
             f'<tspan fill="{t["accent"]}">github</tspan></text>')

    # ---- left column: ladder
    for i, (kind, px, size) in enumerate(BOOK):
        n = i + 1
        if kind == "mid":
            o.append(f'<line x1="{PAD_X}" y1="{y(n)-14}" x2="{rx-14}" '
                     f'y2="{y(n)-14}" stroke="{t["stroke"]}"/>')
            o.append(f'<text x="{PAD_X}" y="{y(n)+2}" fill="{t["accent"]}" '
                     f'font-size="12">spread 0.02 · mid 100.01</text>')
            continue
        col = t["bid"] if kind == "bid" else t["ask"]
        o.append(f'<text x="{PAD_X}" y="{y(n)}" fill="{t["dim"]}">{kind}</text>')
        o.append(f'<text x="{PAD_X+34}" y="{y(n)}" fill="{t["val"]}">{px}</text>')
        # bars as rects, not glyphs: exact widths, no font dependency
        o.append(f'<rect x="{PAD_X+96}" y="{y(n)-10}" width="{size*13}" '
                 f'height="11" rx="1.5" fill="{col}"/>')

    # ---- right column: neofetch rows
    for i, (key, val) in enumerate(ROWS):
        if key is None:
            continue
        n = i + 1
        dots = "." * (KEY_W - len(key) + 2)
        o.append(f'<text x="{INFO_X}" y="{y(n)}" xml:space="preserve">'
                 f'<tspan fill="{t["key"]}">{key}</tspan>'
                 f'<tspan fill="{t["dots"]}"> {dots} </tspan>'
                 f'<tspan fill="{t["val"]}">{esc(val)}</tspan></text>')

    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    here = pathlib.Path(__file__).parent
    for name in THEMES:
        p = here / f"panel-{name}.svg"
        p.write_text(build(name))
        print(f"wrote {p.name}  {W}x{H}")
