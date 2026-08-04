<!-- The panel is a real gradient-descent run on an ill-conditioned quadratic:
     the contours are true level sets, the zig-zag is what a fixed learning
     rate actually does. Regenerate with `python3 make_panel.py`. -->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="gd-dark.svg">
  <img alt="Kushagra Behl — MIT Center for Collective Intelligence, Slashy (YC S25), Math & Computing at Georgia Tech" src="gd-light.svg" width="806">
</picture>

The work at MIT, Slashy, and the Philly AI Lab lives behind private repos. This is the part you can read: nineteen quant and ML libraries, each written to find out how the thing actually works, and each made to prove it did.

**LLM pipelines** — RAG, vector DBs, prompt evaluation · **ML from scratch** — autodiff, transformers, backprop by hand · **quant methods** — SVI calibration, Fama-MacBeth, regret analysis · Python · NumPy · Next.js · R · MATLAB · GAMS · C++

## Six worth your time

**[transformer-from-scratch](https://github.com/superkush06/transformer-from-scratch)** — a GPT written the long way
No autograd, no tape, no `.backward()`. Every backward pass derived on paper and typed out as NumPy, then held to it: **1,312 hand-computed partial derivatives**, each checked against the definition of a derivative. When you read `tfs/attention.py`, you are reading the chain rule.

**[tinydiff](https://github.com/superkush06/tinydiff)** — reverse mode, written out in full
Run the program once, walk the graph back once, get every partial derivative for about the price of the forward pass. **~420 lines**, including the parts micrograd clones wave through: broadcasting, the whole of `np.matmul`'s shape space, a graph walk that survives 100,000 operations, and a `backward()` that would rather raise than hand back a number it can't stand behind.

**[gauss-bandit](https://github.com/superkush06/gauss-bandit)** — held to the bound it's supposed to meet
Every bandit library ships UCB1 and a chart of regret going up; the chart can't tell you whether the number at the end is any good. **Lai and Robbins settled that in 1985** — no consistent policy beats *C* ln *T*, and *C* is computable from the environment. This computes it, implements a policy that attains it, and measures everything else against the same yardstick.

**[lobster](https://github.com/superkush06/lobster)** — a queue, and the only way to the front is to be early
A matching engine and agent simulator built around that sentence. Orders reach the book over a wire with latency, price-time priority decides who fills, and everything reported — queue position, adverse selection, market-maker P&L — is measured off the tape those races produce. **~1,900 lines, no dependencies**, and more than that again in tests.

**[vol-surface](https://github.com/superkush06/vol-surface)** — a smile is not a curve, it's a claim about a distribution
Fit it carelessly and the claim quietly becomes incoherent: negative probability over a band of outcomes, quoted and hedged as though nothing were wrong. So the incoherent cases are made loud — **every SVI fit is checked against the Gatheral–Jacquier butterfly condition before it is returned**, and every surface for calendar monotonicity.

**[factor-zoo](https://github.com/superkush06/factor-zoo)** — run on a universe that knows the answer
A backtest that agrees with you is worth nothing until you can tell whether it agrees because the signal is real or because the code leaked. So it **writes known premia into a synthetic panel** and demands the pipeline read them back — and read back *nothing* when they're switched off.

<img src="https://raw.githubusercontent.com/superkush06/gauss-bandit/main/docs/demo.png" width="100%" alt="cumulative regret: Thompson flattens out, EXP3 keeps paying for an adversary that was never there" />

## Every number is checked against something outside itself

Each library ships a `docs/validation.md` that runs its own numbers against a published result or a closed-form answer, with verdicts derived from the measurements — so breaking the library turns the table red rather than leaving a stale claim behind.

| Library | Checked against | Result |
| :-- | :-- | :-- |
| transformer-from-scratch | central differences, every parameter tensor | 1,312 gradients, worst 3.1e-07 |
| tinydiff | analytic derivatives + finite differences | all ops, mutation-tested |
| gauss-bandit | Lai–Robbins (1985), Auer et al. (2002) | regret inside both bounds |
| optune | Longstaff–Schwartz (2001) Table 1 | max gap 0.0087 |
| vol-surface | Hagan et al. (2002), Gatheral–Jacquier | butterfly + calendar clean |
| factor-zoo | planted premia, and placebos with none | recovers both |

Where a library disagrees with its reference, the doc says so instead of widening the tolerance.

<img src="https://raw.githubusercontent.com/superkush06/vol-surface/main/docs/demo.png" width="100%" alt="calibrated SVI implied volatility surface, five expiries" />

## The rest

[optune](https://github.com/superkush06/optune) · [portopt](https://github.com/superkush06/portopt) · [garch](https://github.com/superkush06/garch) · [risk](https://github.com/superkush06/risk) · [kalman](https://github.com/superkush06/kalman) · [regimes](https://github.com/superkush06/regimes) · [bayes](https://github.com/superkush06/bayes) · [rl-gym](https://github.com/superkush06/rl-gym) · [mlrun](https://github.com/superkush06/mlrun)

A quant sports-betting stack: [oddslib](https://github.com/superkush06/oddslib) de-vigs market prices · [dixoncoles](https://github.com/superkush06/dixoncoles) models the scoreline · [kelly-bet](https://github.com/superkush06/kelly-bet) sizes the bet · [arbfinder](https://github.com/superkush06/arbfinder) finds the arb when two books disagree.

<br>

<sub>[LinkedIn](https://www.linkedin.com/in/kushagra-behl/) · kushagra@gatech.edu</sub>
