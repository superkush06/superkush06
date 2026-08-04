#!/usr/bin/env python3
"""Animated header panel for the profile README.

Left: gradient descent on an ill-conditioned quadratic. The contours are the
real level sets of f(u,v) = 1/2 (L1 u^2 + L2 v^2) and the path is an actual GD
run, so the zig-zag across the valley is the genuine behaviour of a fixed
learning rate on a badly conditioned problem rather than a drawn squiggle.
Animated with SMIL, which GitHub renders (it is how the contribution snake
works).

Right: neofetch-style key/value rows.

Colours are GitHub's own canvas and foreground values so the panel sits *in*
the page instead of on top of it. The monospace stack is metric-corrected with
@font-face so column alignment survives font substitution.
"""
from __future__ import annotations

import math
import pathlib

FS = 14
LH = 22
PAD_X, PAD_TOP = 26, 40
INFO_X = 330

# --- loss landscape -------------------------------------------------------
L1, L2 = 1.0, 7.5          # eigenvalues: a long narrow valley
THETA = math.radians(28)   # rotation of the valley in screen space
LR = 0.235                 # big enough to zig-zag, small enough to converge
START = (-2.15, 0.70)      # inside the outermost contour
STEPS = 26
SCALE = 46                 # px per unit
CX, CY = 152, 158          # centre of the plot in panel coords

THEMES = {
    "dark": dict(bg="#0d1117", stroke="#30363d", key="#58a6ff", val="#F0F6FC",
                 dim="#6e7681", dots="#373e47", accent="#d29922",
                 ring=["#1f6feb", "#388bfd", "#58a6ff", "#79c0ff", "#a5d6ff"],
                 path="#f778ba", dot="#ffffff"),
    "light": dict(bg="#f6f8fa", stroke="#d0d7de", key="#0969da", val="#1F2328",
                  dim="#8c959f", dots="#c9d1d9", accent="#9a6700",
                  ring=["#0a3069", "#0550ae", "#0969da", "#218bff", "#54aeff"],
                  path="#bf3989", dot="#ffffff"),
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
H = 330


def descend() -> list[tuple[float, float]]:
    u, v = START
    pts = [(u, v)]
    for _ in range(STEPS):
        u -= LR * L1 * u
        v -= LR * L2 * v
        pts.append((u, v))
    return pts


def to_screen(u: float, v: float) -> tuple[float, float]:
    c, s = math.cos(THETA), math.sin(THETA)
    return CX + (u * c - v * s) * SCALE, CY + (u * s + v * c) * SCALE


PATH = [to_screen(u, v) for u, v in descend()]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(theme: str) -> str:
    t = THEMES[theme]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-size="{FS}" '
         f'font-family="MonoFallback,ui-monospace,SFMono-Regular,Menlo,'
         f'Consolas,monospace">',
         '<style>@font-face{font-family:MonoFallback;'
         'src:local("SFMono-Regular"),local("Consolas"),'
         'local("DejaVu Sans Mono");size-adjust:105%;}</style>',
         f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" '
         f'fill="{t["bg"]}" stroke="{t["stroke"]}"/>']

    def y(n):
        return PAD_TOP + n * LH

    o.append(f'<text x="{PAD_X}" y="{y(0)}" fill="{t["dim"]}" font-size="12">'
             f'GRADIENT DESCENT</text>')

    deg = math.degrees(THETA)
    for k, level in enumerate([0.28, 0.62, 1.15, 1.9, 2.9]):
        rx_ = math.sqrt(2 * level / L1) * SCALE
        ry_ = math.sqrt(2 * level / L2) * SCALE
        o.append(f'<ellipse cx="{CX}" cy="{CY}" rx="{rx_:.1f}" ry="{ry_:.1f}" '
                 f'transform="rotate({deg:.1f} {CX} {CY})" fill="none" '
                 f'stroke="{t["ring"][4-k]}" stroke-width="1.1" '
                 f'stroke-opacity="{0.30 + 0.13 * k:.2f}"/>')

    d = "M " + " L ".join(f"{x:.1f},{yy:.1f}" for x, yy in PATH)
    total = sum(math.dist(PATH[i], PATH[i + 1]) for i in range(len(PATH) - 1))
    o.append(f'<path d="{d}" fill="none" stroke="{t["path"]}" '
             f'stroke-width="1.9" stroke-linejoin="round" '
             f'stroke-linecap="round" stroke-opacity="0.75"/>')

    sx, sy = PATH[0]
    o.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="2.6" '
             f'fill="{t["path"]}" fill-opacity="0.85"/>')
    o.append(f'<circle cx="{CX}" cy="{CY}" r="2.4" fill="{t["accent"]}"/>')
    o.append(f'<circle r="4.4" fill="{t["dot"]}" stroke="{t["path"]}" '
             f'stroke-width="1.7">'
             f'<animateMotion dur="3.4s" repeatCount="indefinite" '
             f'path="{d}"/></circle>')

    o.append(f'<text x="{PAD_X}" y="{H-22}" fill="{t["dim"]}" font-size="11">'
             f'condition number {L2/L1:.1f} · lr {LR} · {STEPS} steps</text>')

    rx = INFO_X - 30
    o.append(f'<line x1="{rx}" y1="{y(0)-16}" x2="{rx}" y2="{H-20}" '
             f'stroke="{t["stroke"]}"/>')
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
        p = here / f"gd-{name}.svg"
        p.write_text(build(name))
        print(f"wrote {p.name}  {W}x{H}")
