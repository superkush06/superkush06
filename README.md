<!-- The panel is a real gradient-descent run on an ill-conditioned quadratic:
     the contours are true level sets, the zig-zag is what a fixed learning
     rate actually does. Regenerate with `python3 make_panel.py`. -->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="gd-dark.svg">
  <img alt="Kushagra Behl, MIT Center for Collective Intelligence, Slashy (YC S25), Math & Computing at Georgia Tech" src="gd-light.svg" width="806">
</picture>

Hi. I'm into ML, startups and finance, and I learn things by building them.
Most of what's here started as something I wanted to understand and didn't, so
I wrote it out from scratch and then made it prove it was right.

## Three you can run right now

No install, no clone. Each page compiles the actual Python package to
WebAssembly and runs it in your tab, so every number on it is computed while
you read and none of it is precomputed.

**[transformer-from-scratch](https://superkush06.github.io/transformer-from-scratch/demo/)** &nbsp;·&nbsp; audit the chain rule\
A GPT with no autograd, so every backward pass is code I derived by hand.
Click any of its 1,312 weights and the page measures that derivative against
the definition of a derivative, in front of you, on tokens you type. Then
break one of the backward passes on purpose and watch 20 of 29 gradients go
wrong while the loss curve carries on as if nothing happened.

**[lobster](https://superkush06.github.io/lobster/demo/)** &nbsp;·&nbsp; a stock exchange you can take apart\
A matching engine with latency on the wire. Change who's trading and the book
reshapes underneath you, then five experiments measure what changed: what
queue position is worth, what a big order costs, and where the simulated tape
stops looking like a real one.

**[vol-surface](https://superkush06.github.io/vol-surface/demo/)** &nbsp;·&nbsp; break an arbitrage-free surface\
Drag five SVI parameters until the fitted smile implies negative probability,
and watch the no-arbitrage screen catch it before the fit is returned.

## The six I'd actually point at

**[transformer-from-scratch](https://github.com/superkush06/transformer-from-scratch)** &nbsp;·&nbsp; a GPT written the long way\
No autograd, no tape, no `.backward()`. Every backward pass derived on paper
and typed out as NumPy, then held to it: **1,312 hand-computed partial
derivatives**, each checked against a central difference, worst relative error
3.1e-07. When you read `tfs/attention.py`, you're reading the chain rule.

**[tinydiff](https://github.com/superkush06/tinydiff)** &nbsp;·&nbsp; reverse mode, written out in full\
Run the program once, walk the graph back once, get every partial derivative
for about the price of the forward pass. **654 lines**, including the parts
micrograd clones wave through: broadcasting, the whole of `np.matmul`'s shape
space, a graph walk that survives 100,000 operations, and a `backward()` that
would rather raise than hand back a number it can't stand behind.

**[gauss-bandit](https://github.com/superkush06/gauss-bandit)** &nbsp;·&nbsp; held to the bound it's supposed to meet\
Most bandit libraries ship UCB1 and a chart of regret going up, and the chart
can't tell you whether the number at the end is any good. **Lai and Robbins
settled that in 1985**: no consistent policy beats *C* ln *T*, and *C* is
computable from the environment. This computes it, implements a policy that
attains it, and measures everything else against the same yardstick.

**[lobster](https://github.com/superkush06/lobster)** &nbsp;·&nbsp; a queue, and the only way to the front is to be early\
A matching engine and agent simulator built around that sentence. Orders reach
the book over a wire with latency, price-time priority decides who fills, and
everything reported is measured off the tape those races produce.
**About 2,130 lines, no dependencies**, and more than that again in tests.

**[vol-surface](https://github.com/superkush06/vol-surface)** &nbsp;·&nbsp; a smile is a claim about a distribution\
Fit one carelessly and the claim quietly becomes incoherent: negative
probability over a band of outcomes, quoted and hedged as though nothing were
wrong. So the incoherent cases are made loud. **Every SVI fit is screened
against the Gatheral–Jacquier butterfly condition** before it's returned, and
every surface for calendar monotonicity.

**[factor-zoo](https://github.com/superkush06/factor-zoo)** &nbsp;·&nbsp; run on a universe that knows the answer\
A backtest that agrees with you is worth nothing until you can tell whether it
agrees because the signal is real or because the code leaked. So it **writes
known premia into a synthetic panel** and demands the pipeline read them back,
and read back *nothing* when they're switched off.

<img src="https://raw.githubusercontent.com/superkush06/lobster/main/docs/book_depth.png" width="100%" alt="every resting order at every price level over 1,400 ticks, coloured by queue depth" />

<sub>Every resting order, every level, every tick of a <a href="https://github.com/superkush06/lobster">lobster</a> run. Colour is queue depth on a log scale, with the best bid and ask threaded through it.</sub>

## Checked against something outside itself

Those six each ship a `docs/validation.md` that runs their own numbers against
a published result or a closed-form answer, with the verdicts derived from the
measurements. Breaking the library turns the table red rather than leaving a
stale claim behind.

| Library | Checked against | Result |
| :-- | :-- | :-- |
| transformer-from-scratch | central differences, every parameter tensor | 1,312 gradients, worst 3.1e-07 |
| tinydiff | analytic derivatives and finite differences | all ops, mutation-tested |
| gauss-bandit | Lai–Robbins (1985), Auer et al. (2002) | regret inside both bounds |
| vol-surface | Hagan et al. (2002), Gatheral–Jacquier | butterfly and calendar clean |
| lobster | published microstructure facts | 11 of 14 agree; the 3 that don't are written up |
| factor-zoo | planted premia, and placebos with none | recovers both |

Where a library disagrees with its reference, the doc says so instead of
widening the tolerance. lobster's order-flow memory dies after about a hundred
trades where real flow lasts thousands, and vol-surface's SABR expansion is
393 basis points from a Monte Carlo of the SDE it approximates. Both are on
the page rather than filed off.

<img src="https://raw.githubusercontent.com/superkush06/vol-surface/main/docs/hero.png" width="100%" alt="a quoted smile that implies negative probability, and the nearest arbitrage-free one" />

<sub>A quoted smile 1.83 vol points from the nearest admissible one. Middle: the Gatheral–Jacquier condition it breaks. Right: the consequence, a negative risk-neutral density between k = 0.64 and 1.25, which is a butterfly that pays you to own it. From <a href="https://github.com/superkush06/vol-surface">vol-surface</a>.</sub>

## The rest

[optune](https://github.com/superkush06/optune) · [portopt](https://github.com/superkush06/portopt) · [garch](https://github.com/superkush06/garch) · [risk](https://github.com/superkush06/risk) · [kalman](https://github.com/superkush06/kalman) · [regimes](https://github.com/superkush06/regimes) · [bayes](https://github.com/superkush06/bayes) · [rl-gym](https://github.com/superkush06/rl-gym) · [mlrun](https://github.com/superkush06/mlrun)

Reach me at **kushagra@gatech.edu**.
