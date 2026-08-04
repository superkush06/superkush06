<!-- The panel is a real gradient-descent run on an ill-conditioned quadratic:
     the contours are true level sets, the zig-zag is what a fixed learning
     rate actually does. Regenerate with `python3 make_panel.py`. -->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="gd-dark.svg">
  <img alt="Kushagra Behl — MIT Center for Collective Intelligence, Slashy (YC S25), Math & Computing at Georgia Tech" src="gd-light.svg" width="806">
</picture>

The work at MIT, Slashy, and the Philly AI Lab lives behind private repos. This is the part you can read: nineteen quant and ML libraries, written to find out how the things actually work.

**LLM pipelines** — RAG, vector DBs, prompt evaluation · **ML from scratch** — autodiff, transformers, backprop by hand · **quant methods** — SVI calibration, Fama-MacBeth, regret analysis · Python · NumPy · Next.js · R · MATLAB · GAMS · C++

## Six worth your time

**[transformer-from-scratch](https://github.com/superkush06/transformer-from-scratch)** — GPT-style decoder in pure NumPy
Backprop derived by hand. All 29 parameter tensors agree with finite differences, and the causal mask is verified by ablation rather than assumed.

**[tinydiff](https://github.com/superkush06/tinydiff)** — reverse-mode autodiff in under 500 lines
Batched and broadcast matmul adjoints, PyTorch-correct double-`backward()` semantics, and a 3000-op graph that doesn't blow the stack.

**[gauss-bandit](https://github.com/superkush06/gauss-bandit)** — UCB1, Thompson, EXP3, LinUCB
Measured regret checked against the bound each paper actually proves, including the Lai-Robbins lower bound computed exactly rather than sketched.

**[lobster](https://github.com/superkush06/lobster)** — limit order book simulator
Price-time priority, self-trade prevention, latency and market-impact models, and NASDAQ LOBSTER replay that reports when reconstruction drifts instead of silently dropping messages.

**[vol-surface](https://github.com/superkush06/vol-surface)** — implied volatility surfaces
SVI calibrated across five expiries at 10–14 bp per-slice residuals, calendar arbitrage ruled out: total variance is non-decreasing in T at every strike.

**[factor-zoo](https://github.com/superkush06/factor-zoo)** — equity factor reproductions
Momentum, value, quality, low-vol with Fama-MacBeth and Newey-West. Look-ahead removed from the winsorizer, worth 0.165 z-units of leakage.

<img src="https://raw.githubusercontent.com/superkush06/gauss-bandit/main/docs/demo.png" width="100%" alt="cumulative regret: Thompson flattens out, EXP3 keeps paying for an adversary that was never there" />

## Every number here is checked against something outside itself

Each library ships a `docs/validation.md` that runs its own numbers against a published result or a closed-form answer. The verdicts are derived from the measurements, so breaking the library turns the table red.

| Library | Checked against | Result |
| :-- | :-- | :-- |
| transformer-from-scratch | finite differences, every parameter tensor | 29/29 agree |
| tinydiff | analytic derivatives + finite differences | all ops, mutation-tested |
| gauss-bandit | Auer et al. (2002), Lai-Robbins bound | regret inside both |
| optune | Longstaff-Schwartz (2001) Table 1, finite-difference column | max gap 0.0087 |
| vol-surface | Hagan et al. (2002) SABR, Gatheral-Jacquier no-arbitrage | butterfly + calendar clean |
| lobster | Cont (2001) stylized facts | fat tails, clustering reproduced |

Where a library disagrees with its reference, the doc says so instead of widening the tolerance.

<img src="https://raw.githubusercontent.com/superkush06/vol-surface/main/docs/demo.png" width="100%" alt="calibrated SVI implied volatility surface, five expiries" />

## The rest

[optune](https://github.com/superkush06/optune) · [portopt](https://github.com/superkush06/portopt) · [garch](https://github.com/superkush06/garch) · [risk](https://github.com/superkush06/risk) · [kalman](https://github.com/superkush06/kalman) · [regimes](https://github.com/superkush06/regimes) · [bayes](https://github.com/superkush06/bayes) · [rl-gym](https://github.com/superkush06/rl-gym) · [mlrun](https://github.com/superkush06/mlrun)

A quant sports-betting stack: [oddslib](https://github.com/superkush06/oddslib) de-vigs market prices · [dixoncoles](https://github.com/superkush06/dixoncoles) models the scoreline · [kelly-bet](https://github.com/superkush06/kelly-bet) sizes the bet · [arbfinder](https://github.com/superkush06/arbfinder) finds the arb when two books disagree.

<br>

<sub>[LinkedIn](https://www.linkedin.com/in/kushagra-behl/) · kushagra@gatech.edu</sub>
