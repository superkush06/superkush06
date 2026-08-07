#!/usr/bin/env python3
"""Validation strip for the profile README.

One row per library: what it's checked against, and the number its own
committed docs/validation.md currently reports. Nothing in the measured
column is typed here. Each cell is pulled over raw.githubusercontent.com and
lifted out with an anchored regex, so if a repo's numbers move and this file
doesn't, the strip either changes with them or says "unavailable". A stale
number is the failure this artefact exists to prevent, so a pattern that
stops matching is never allowed to fall back to a remembered value.

The row colour is the conclusion of that repo's most recent push-triggered CI
run, read from the public GitHub API. Green passed, red failed, amber still
running.

Unauthenticated the API allows 60 requests an hour and this makes six, which
is fine, but a rate-limited response aborts the whole run rather than
emitting a strip with holes in it. Set GITHUB_TOKEN to raise the ceiling.

Regenerate with `python3 make_strip.py`.
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import ssl
import sys
import time
import urllib.error
import urllib.request

OWNER = "superkush06"
API = "https://api.github.com/repos/{owner}/{repo}/actions/runs?per_page=1&event=push"
RAW = "https://raw.githubusercontent.com/{owner}/{repo}/main/{path}"
UA = "superkush06-profile-strip"

WORDS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19, "twenty": 20,
}


class Unavailable(Exception):
    """A pattern that should have matched didn't. Say so, don't guess."""


def word(w: str) -> int:
    if w not in WORDS:
        raise Unavailable(f"not a number word: {w!r}")
    return WORDS[w]


def anchored(pattern: str, text: str, where: str) -> tuple[str, ...]:
    m = re.search(pattern, text, re.M)
    if not m:
        raise Unavailable(f"no match for {where}")
    return m.groups()


# --- the six rows ---------------------------------------------------------
#
# "against" is a description of the reference, not a measurement, so it lives
# here. Everything in the third column is lifted out of the fetched document
# by the function beside it.

def m_transformer(doc: str) -> str:
    n, err = anchored(
        r"^\[1\] gradients: ([\d,]+) scalars over \d+ tensors, [\d,]+ signs "
        r"agree, worst relative error ([0-9]+\.[0-9]+e[+-][0-9]+)\s*$",
        doc, "gradient sweep line")
    return f"{n} scalars, worst {err}"


def m_tinydiff(doc: str) -> str:
    n, failed = anchored(
        r"^([\d,]+) \(op, shape\) pairs checked at tol=[^;]+; ([\d,]+) "
        r"failed\s*$", doc, "op/shape sweep line")
    return f"{n} op/shape pairs, {failed} failed"


def m_bandit(doc: str) -> str:
    floor, meas, bound = anchored(
        r"^\s*Lai-Robbins floor\s+C ln T\s+([\d.]+)\s+\(C = [\d.]+\)\n"
        r"\s*measured regret\s+R\(T\)\s+([\d.]+)\n"
        r"\s*Auer et al\. Thm 1\s+upper bound\s+([\d.]+)\s*$",
        doc, "two-sided regret block")
    return f"UCB1 {meas} in [{floor}, {bound}]"


def m_lobster(doc: str) -> str:
    agree, against, split = anchored(
        r"Across the two tables:\s+([a-z]+)\s+rows agree,\s+([a-z]+)\s+"
        r"disagree outright,\s+and\s+([a-z]+)\s+agrees for one agent mix",
        doc, "stylised-facts tally")
    a = word(agree)
    total = a + word(against) + word(split)
    return f"{a} of {total} published facts"


def m_vol(doc: str) -> str:
    draws, _worst, viol = anchored(
        r"\|\s*SSVI inside the Gatheral-Jacquier conditions\s*\|\s*min "
        r"`g\(k\)` over ([\d,]+) near-boundary draws = `([+-][\d.]+)`, "
        r"violations `([\d,]+)`\s*\|", doc, "butterfly screen row")
    cal, = anchored(
        r"\|\s*The surface's calendar check\s*\|\s*worst decrease in `w` "
        r"over a [\dx×]+ `\(k,T\)` grid = `([\d.e+-]+)`\s*\|",
        doc, "calendar screen row")
    return f"{viol}/{draws} butterfly, cal {cal}"


def m_factor(doc: str) -> str:
    got, _se, _z, planted = anchored(
        r"\|\s*\d+\s*\|\s*A universe with no premium in it yields no premium"
        r"\s*\|\s*([+-][\d.]+) bp/day \(s\.e\. ([\d.]+)\), ([+-][\d.]+) "
        r"s\.e\. from truth\s*\|\s*([+-][\d.]+) bp/day\s*\|",
        doc, "placebo row")
    return f"{got} bp/day vs planted {planted}"


LIBS = [
    ("transformer-from-scratch", "docs/validation.md",
     "central differences, Press et al.", m_transformer),
    ("tinydiff", "docs/validation.md",
     "closed forms, Giles (2008) matmul", m_tinydiff),
    ("gauss-bandit", "docs/validation.md",
     "Lai-Robbins 1985, Auer et al. 2002", m_bandit),
    ("lobster", "docs/validation.md",
     "Cont 2001, Roll 1984, Bouchaud 2004", m_lobster),
    ("vol-surface", "docs/validation.md",
     "Gatheral-Jacquier 2014, Hagan 2002", m_vol),
    ("factor-zoo", "docs/validation.md",
     "a planted zero, and placebos", m_factor),
]


# --- fetching -------------------------------------------------------------

def fatal(msg: str) -> None:
    print(f"make_strip: {msg}", file=sys.stderr)
    sys.exit(1)


def trust() -> ssl.SSLContext:
    """Default verification, with a bundle found for it if the box has none.

    A python.org install whose Install Certificates.command was never run has
    no CA file at all, and every fetch here dies on it. Borrow certifi's
    bundle when that happens. Verification stays on in both branches; a strip
    built over an unverified connection is not evidence of anything.
    """
    ctx = ssl.create_default_context()
    if ctx.cert_store_stats()["x509_ca"] == 0:
        try:
            import certifi
        except ImportError:
            fatal("no CA certificates available. On macOS run "
                  "'Install Certificates.command' from your Python "
                  "install, or pip install certifi.")
        ctx.load_verify_locations(certifi.where())
    return ctx


CTX = trust()


def get(url: str, token: str | None) -> tuple[int, bytes, dict]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    if "api.github.com" in url:
        req.add_header("Accept", "application/vnd.github+json")
    try:
        with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
            return r.status, r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read(), dict(e.headers)
    except urllib.error.URLError as e:
        fatal(f"could not reach {url}: {e.reason}")


def ci_state(repo: str, token: str | None) -> str:
    """A theme colour key: ok, bad, wait or none.

    Rate limiting aborts the whole run rather than colouring a row on a
    guess.
    """
    url = API.format(owner=OWNER, repo=repo)
    status, body, headers = get(url, token)

    # A token scoped to another repo can be rejected where the anonymous read
    # would have succeeded, so drop it once and try again before giving up.
    if status in (401, 403, 404) and token:
        status, body, headers = get(url, None)
        token = None

    if status in (403, 429):
        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")
        detail = ""
        if reset and reset.isdigit():
            detail = " until " + time.strftime(
                "%H:%M UTC", time.gmtime(int(reset)))
        if remaining == "0" or b"rate limit" in body.lower():
            fatal(f"GitHub API rate-limited on {repo}{detail}. Refusing to "
                  f"write a strip with a guessed CI state. Set GITHUB_TOKEN "
                  f"or wait.")
        fatal(f"GitHub API returned 403 for {repo}: {body[:200]!r}")
    if status != 200:
        fatal(f"GitHub API returned {status} for {repo}")

    runs = json.loads(body).get("workflow_runs", [])
    if not runs:
        return "none"
    run = runs[0]
    if run.get("status") != "completed":
        return "wait"
    return "ok" if run.get("conclusion") == "success" else "bad"


def measured(repo: str, path: str, fn) -> str:
    """The number the repo's own doc currently reports, or "" for unavailable.

    raw.githubusercontent.com serves public files anonymously, so no token
    goes anywhere near this one.
    """
    url = RAW.format(owner=OWNER, repo=repo, path=path)
    status, body, _ = get(url, None)
    if status != 200:
        print(f"  {repo}: {path} returned {status}", file=sys.stderr)
        return ""
    try:
        return fn(body.decode("utf-8"))
    except Unavailable as e:
        print(f"  {repo}: {e}", file=sys.stderr)
        return ""


# --- drawing --------------------------------------------------------------

FS = 11.5
CH = FS * 0.66          # generous advance, so no column can bleed into the next
LH = 26
PAD_X, PAD_TOP = 26, 30
DOT_W = 18
MIN_W = 806             # the header card's width, so the two line up

# dim carries the "checked against" column, which is content rather than
# chrome, so it takes Primer's muted foreground. The subtle greys the header
# card uses for its section labels sit at 2.9:1 on paper, under AA for text
# this small.
THEMES = {
    "dark": dict(bg="#0d1117", stroke="#30363d", key="#58a6ff", val="#F0F6FC",
                 dim="#8b949e", rule="#21262d", accent="#d29922",
                 ok="#3fb950", bad="#f85149", wait="#d29922", none="#8b949e"),
    "light": dict(bg="#f6f8fa", stroke="#d0d7de", key="#0969da",
                  val="#1F2328", dim="#656d76", rule="#d8dee4",
                  accent="#9a6700", ok="#1a7f37", bad="#cf222e",
                  wait="#9a6700", none="#656d76"),
}

LEGEND = [("ok", "last push passed"), ("bad", "failed"),
          ("wait", "still running"), ("none", "no run")]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(theme: str, rows: list[tuple], stamp: str) -> str:
    t = THEMES[theme]

    w_name = max(len(r[0]) for r in rows)
    w_ag = max(len(r[1]) for r in rows)
    w_ms = max(len(r[2] or "unavailable") for r in rows)

    body = (PAD_X + DOT_W + (w_name + w_ag + w_ms) * CH + PAD_X)
    gap = max(16.0, (MIN_W - body) / 2)
    W = int(round(body + 2 * gap))

    x_name = PAD_X + DOT_W
    x_ag = x_name + w_name * CH + gap
    x_ms = x_ag + w_ag * CH + gap

    y_head = PAD_TOP + 20
    y0 = y_head + 22
    y_rule = y0 - 16
    y_last = y0 + (len(rows) - 1) * LH
    y_foot = y_last + 30
    H = int(round(y_foot + 34))

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-size="{FS}" '
         f'font-family="MonoFallback,ui-monospace,SFMono-Regular,Menlo,'
         f'Consolas,monospace">',
         '<style>@font-face{font-family:MonoFallback;'
         'src:local("SFMono-Regular"),local("Consolas"),'
         'local("DejaVu Sans Mono");size-adjust:105%;}</style>',
         f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" '
         f'fill="{t["bg"]}" stroke="{t["stroke"]}"/>']

    o.append(f'<text x="{PAD_X}" y="{PAD_TOP}" fill="{t["dim"]}" '
             f'font-size="12">VALIDATION</text>')
    o.append(f'<text x="{W-PAD_X}" y="{PAD_TOP}" fill="{t["dim"]}" '
             f'font-size="11" text-anchor="end">read {esc(stamp)}</text>')

    for x, label in ((x_name, "LIBRARY"), (x_ag, "CHECKED AGAINST"),
                     (x_ms, "LAST MEASURED")):
        o.append(f'<text x="{x:.1f}" y="{y_head}" fill="{t["dim"]}" '
                 f'font-size="10" letter-spacing="0.6">{label}</text>')
    o.append(f'<line x1="{PAD_X}" y1="{y_rule}" x2="{W-PAD_X}" y2="{y_rule}" '
             f'stroke="{t["rule"]}"/>')

    for i, (name, against, value, state) in enumerate(rows):
        y = y0 + i * LH
        o.append(f'<circle cx="{PAD_X+4:.1f}" cy="{y-4:.1f}" r="3.4" '
                 f'fill="{t[state]}"/>')
        o.append(f'<text x="{x_name:.1f}" y="{y}" fill="{t[state]}">'
                 f'{esc(name)}</text>')
        o.append(f'<text x="{x_ag:.1f}" y="{y}" fill="{t["dim"]}">'
                 f'{esc(against)}</text>')
        fill = t["val"] if value else t["accent"]
        o.append(f'<text x="{x_ms:.1f}" y="{y}" fill="{fill}">'
                 f'{esc(value or "unavailable")}</text>')

    o.append(f'<line x1="{PAD_X}" y1="{y_last+14}" x2="{W-PAD_X}" '
             f'y2="{y_last+14}" stroke="{t["rule"]}"/>')

    seen = {r[3] for r in rows}
    x = float(PAD_X)
    for state, label in LEGEND:
        if state not in seen:
            continue
        o.append(f'<circle cx="{x+3:.1f}" cy="{y_foot-4:.1f}" r="3" '
                 f'fill="{t[state]}"/>')
        o.append(f'<text x="{x+12:.1f}" y="{y_foot}" fill="{t["dim"]}" '
                 f'font-size="10.5">{label}</text>')
        x += 12 + (len(label) + 3) * 6.4

    o.append(f'<text x="{W-PAD_X}" y="{y_foot}" fill="{t["dim"]}" '
             f'font-size="10.5" text-anchor="end">every number read out of '
             f'that repo&#8217;s docs/validation.md</text>')
    o.append(f'<text x="{PAD_X}" y="{y_foot+19}" fill="{t["dim"]}" '
             f'font-size="10.5">nothing on this row is typed by hand; a '
             f'pattern that stops matching reads unavailable, never a '
             f'remembered value</text>')

    o.append("</svg>")
    return "\n".join(o)


def main() -> None:
    token = os.environ.get("GITHUB_TOKEN") or None
    stamp = time.strftime("%Y-%m-%d", time.gmtime())
    rows, missing = [], 0

    for repo, path, against, fn in LIBS:
        state = ci_state(repo, token)
        value = measured(repo, path, fn)
        if not value:
            missing += 1
        print(f"{repo:26} ci={state:5} {value or 'UNAVAILABLE'}")
        rows.append((repo, against, value, state))

    here = pathlib.Path(__file__).parent
    for name in THEMES:
        p = here / f"validation-{name}.svg"
        svg = build(name, rows, stamp)
        p.write_text(svg, encoding="utf-8")
        print(f"wrote {p.name}  {len(svg.encode()):,} bytes")

    if missing:
        print(f"{missing} cell(s) unavailable", file=sys.stderr)


if __name__ == "__main__":
    main()
