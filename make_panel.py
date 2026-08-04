#!/usr/bin/env python3
"""Terminal panel for the profile README.

Left: a real causal self-attention map — scores are generated, masked, and
softmaxed here, so the triangle and the row weights are actual numbers rather
than decoration. Right: neofetch-style key/value rows.

Rendered as SVG so it can carry colour and a monospace grid markdown can't do.
Two variants so the README switches on prefers-color-scheme.

Layout: the two columns are positioned independently at fixed x offsets rather
than padded into a shared character grid — block glyphs don't reliably advance
one cell, so character-count padding can't keep columns from colliding.
"""
from __future__ import annotations

import math
import pathlib
import random

FS = 14
LH = 22
PAD_X, PAD_TOP = 26, 40
INFO_X = 316

N = 12            # sequence length for the attention map
CELL, GAP = 15, 3

THEMES = {
    "dark": dict(bg="#0d1117", stroke="#30363d", key="#58a6ff", val="#c9d1d9",
                 dim="#6e7681", dots="#373e47", accent="#d29922",
                 hot=(88, 166, 255), cold="#161b22", spark="#3fb950"),
    "light": dict(bg="#ffffff", stroke="#d0d7de", key="#0969da", val="#1f2328",
                  dim="#8c959f", dots="#c9d1d9", accent="#9a6700",
                  hot=(9, 105, 218), cold="#f6f8fa", spark="#1a7f37"),
}

ROWS = [
    ("School",   "Georgia Tech, Math & Computing"),
    ("Work",     "Growth engineering @ Slashy (YC S25)"),
    ("Research", "ML @ MIT, Collective Intelligence"),
    ("Before",   "Wharton, DECA ICDC x2, SIG Discovery"),
    (None, None),
    ("Building", "transformers, autodiff, order books"),
    ("Stack",    "Python, NumPy, C, TypeScript"),
    ("Contact",  "kushagra@gatech.edu"),
]

KEY_W = max(len(k) for k, _ in ROWS if k)
VAL_W = max(len(v) for _, v in ROWS if v)
CH = 9.0

W = int(INFO_X + (KEY_W + 4 + VAL_W) * CH + PAD_X)
H = int(PAD_TOP + max(N * (CELL + GAP) + 58, (len(ROWS) + 1) * LH) + 14)


def attention(n: int, seed: int = 7) -> list[list[float]]:
    """Causal single-head attention weights: mask the future, then softmax.

    A mild recency prior in the scores keeps the picture legible instead of
    uniform — the diagonal stays bright the way it does in a trained model.
    """
    rng = random.Random(seed)
    rows = []
    for i in range(n):
        scores = [rng.gauss(0, 0.9) + 1.6 * math.exp(-(i - j) / 3.0)
                  if j <= i else float("-inf") for j in range(n)]
        m = max(s for s in scores if s > float("-inf"))
        exp = [math.exp(s - m) if s > float("-inf") else 0.0 for s in scores]
        z = sum(exp)
        rows.append([e / z for e in exp])
    return rows


ATTN = attention(N)


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

    o.append(f'<text x="{PAD_X}" y="{y(0)}" fill="{t["dim"]}" font-size="12">'
             f'SELF-ATTENTION · causal mask</text>')

    # ---- attention heatmap
    gx, gy = PAD_X, y(0) + 14
    r, g, b = t["hot"]
    peak = max(max(row) for row in ATTN)
    for i in range(N):
        for j in range(N):
            x = gx + j * (CELL + GAP)
            yy = gy + i * (CELL + GAP)
            if j > i:
                o.append(f'<rect x="{x}" y="{yy}" width="{CELL}" '
                         f'height="{CELL}" rx="2.5" fill="{t["cold"]}"/>')
            else:
                a = (ATTN[i][j] / peak) ** 0.55
                o.append(f'<rect x="{x}" y="{yy}" width="{CELL}" '
                         f'height="{CELL}" rx="2.5" '
                         f'fill="rgb({r},{g},{b})" fill-opacity="{a:.3f}"/>')

    # ---- loss sparkline under the map
    sy = gy + N * (CELL + GAP) + 26
    span = N * (CELL + GAP) - GAP
    losses = [2.63, 1.94, 1.42, 1.08, 0.83, 0.61, 0.44, 0.31, 0.22, 0.16,
              0.12, 0.09]
    lo, hi = min(losses), max(losses)
    pts = " ".join(
        f"{PAD_X + k * span / (len(losses) - 1):.1f},"
        f"{sy - 22 * (v - lo) / (hi - lo):.1f}"
        for k, v in enumerate(losses))
    o.append(f'<polyline points="{pts}" fill="none" stroke="{t["spark"]}" '
             f'stroke-width="1.8" stroke-linejoin="round"/>')
    o.append(f'<text x="{PAD_X}" y="{sy + 20}" fill="{t["dim"]}" '
             f'font-size="11">train loss 2.63 → 0.09</text>')

    # ---- divider
    rx = INFO_X - 28
    o.append(f'<line x1="{rx}" y1="{y(0)-16}" x2="{rx}" y2="{H-24}" '
             f'stroke="{t["stroke"]}"/>')

    # ---- right column
    o.append(f'<text x="{INFO_X}" y="{y(0)}" xml:space="preserve">'
             f'<tspan fill="{t["accent"]}">kush</tspan>'
             f'<tspan fill="{t["dim"]}">@</tspan>'
             f'<tspan fill="{t["accent"]}">github</tspan></text>')
    for i, (key, val) in enumerate(ROWS):
        if key is None:
            continue
        dots = "." * (KEY_W - len(key) + 2)
        o.append(f'<text x="{INFO_X}" y="{y(i + 2)}" xml:space="preserve">'
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
