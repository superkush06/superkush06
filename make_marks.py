"""Emit the two small marks the README uses: a tool strip and a hairline rule.

Both are hand-written SVG committed to this repo. Nothing here is fetched at
page load, which is the whole point: an image served from someone else's
Vercel function is a dependency the rest of this page does not have.

    python3 make_marks.py     # writes tools-{light,dark}.svg, rule-{light,dark}.svg

The icons are simple-icons (CC0), vendored into icons/ rather than hotlinked
from a CDN, and recoloured to text weight so they read as punctuation in a
sentence rather than as a badge wall.
"""

from __future__ import annotations

import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent

# The five that actually appear in the work below. NumPy and Python carry
# almost every repo; PyTorch is the second opinion the gradients are checked
# against; C and WebAssembly are what the browser demos compile through.
TOOLS = [("python", "Python"), ("numpy", "NumPy"), ("pytorch", "PyTorch"),
         ("c", "C"), ("webassembly", "WebAssembly")]

# Matched to the header card, so the marks read as the same object.
THEMES = {
    "light": {"ink": "#57606a", "sweep": "#1B6CA8", "rule": "#d8dee4"},
    "dark":  {"ink": "#8b949e", "sweep": "#58a6ff", "rule": "#30363d"},
}

ICON_PX, GAP, LABEL_PX = 16, 26, 11


def path_of(slug: str) -> str:
    """The single path out of a simple-icons file."""
    src = (HERE / "icons" / f"{slug}.svg").read_text()
    m = re.search(r'<path\s+d="([^"]+)"', src)
    if not m:
        raise SystemExit(f"no path in icons/{slug}.svg")
    return m.group(1)


def tool_strip(theme: str) -> str:
    """Five marks at text weight, each with its name beside it."""
    c = THEMES[theme]
    parts, x = [], 0
    for slug, label in TOOLS:
        scale = ICON_PX / 24
        parts.append(
            f'<g transform="translate({x},2) scale({scale:.5f})">'
            f'<path d="{path_of(slug)}" fill="{c["ink"]}"/></g>')
        parts.append(
            f'<text x="{x + ICON_PX + 5}" y="14" fill="{c["ink"]}" '
            f'font-size="{LABEL_PX}" font-family="ui-monospace,SFMono-Regular,'
            f'Menlo,monospace">{label}</text>')
        x += ICON_PX + 5 + int(len(label) * LABEL_PX * 0.62) + GAP
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{x}" height="20" '
            f'viewBox="0 0 {x} 20" role="img" aria-label="Python, NumPy, '
            f'PyTorch, C, WebAssembly">{"".join(parts)}</svg>\n')


def rule(theme: str) -> str:
    """A hairline with a highlight that sweeps along it.

    One rect, one gradient, two animated stops. The motion is slow and low
    contrast on purpose: it should register as the page being alive, not as
    something asking to be looked at.
    """
    c = THEMES[theme]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="880" height="2" \
viewBox="0 0 880 2" preserveAspectRatio="none" role="presentation">
<defs><linearGradient id="s" x1="0" x2="1" y1="0" y2="0">
<stop offset="0" stop-color="{c['rule']}"/>
<stop offset="0" stop-color="{c['sweep']}" stop-opacity="0.55">
<animate attributeName="offset" values="-0.25;1.25" dur="7s" \
repeatCount="indefinite"/></stop>
<stop offset="0.12" stop-color="{c['rule']}">
<animate attributeName="offset" values="-0.13;1.37" dur="7s" \
repeatCount="indefinite"/></stop>
<stop offset="1" stop-color="{c['rule']}"/>
</linearGradient></defs>
<rect width="880" height="2" fill="url(#s)"/></svg>
'''


if __name__ == "__main__":
    for theme in THEMES:
        for name, body in (("tools", tool_strip(theme)), ("rule", rule(theme))):
            out = HERE / f"{name}-{theme}.svg"
            out.write_text(body)
            print(f"wrote {out.name}  {len(body):,} bytes")
