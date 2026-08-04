<!-- The panel is a real gradient-descent run on an ill-conditioned quadratic:
     the contours are true level sets, the zig-zag is what a fixed learning
     rate actually does. Regenerate with `python3 make_panel.py`. -->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="gd-dark.svg">
  <img alt="Kushagra Behl — ML research at MIT, growth engineering at Slashy (YC S25), Math & Computing at Georgia Tech" src="gd-light.svg" width="788">
</picture>

### Six I'd actually show you

> **[transformer-from-scratch](https://github.com/superkush06/transformer-from-scratch)** — a GPT-style decoder in pure NumPy, backprop derived by hand.
> All 29 parameter tensors agree with finite differences, and the causal mask is verified by ablation rather than assumed.

> **[tinydiff](https://github.com/superkush06/tinydiff)** — reverse-mode autodiff in under 500 lines.
> Batched and broadcast matmul adjoints, correct double-`backward()` semantics, and a 3000-op graph that doesn't blow the stack.

> **[gauss-bandit](https://github.com/superkush06/gauss-bandit)** — UCB1, Thompson, EXP3, LinUCB.
> Measured regret is checked against the bound each paper actually proves, including the Lai-Robbins lower bound computed exactly rather than sketched.

> **[lobster](https://github.com/superkush06/lobster)** — a limit order book that matches the way an exchange does.
> Price-time priority, self-trade prevention, and NASDAQ LOBSTER replay that reports when reconstruction drifts instead of silently dropping messages.

> **[vol-surface](https://github.com/superkush06/vol-surface)** — SVI calibrated across five expiries.
> Per-slice residuals of 10–14 bp with calendar arbitrage ruled out: total variance is non-decreasing in T at every strike.

> **[factor-zoo](https://github.com/superkush06/factor-zoo)** — momentum, value, quality, low-vol, with Fama-MacBeth and Newey-West.
> Look-ahead removed from the winsorizer, which was worth 0.165 z-units of leakage and most of the gap between paper premia and real ones.

<br>

<img src="https://raw.githubusercontent.com/superkush06/gauss-bandit/main/docs/demo.png" width="100%" alt="cumulative regret: Thompson flattens out, EXP3 keeps paying" />

<img src="https://raw.githubusercontent.com/superkush06/vol-surface/main/docs/demo.png" width="100%" alt="calibrated SVI implied volatility surface" />

<br>

Every one has tests, CI, and a validation doc checking its numbers against published results or closed-form answers — including the rows where they disagree. Built with Claude Code.

<sub>Also around: [optune](https://github.com/superkush06/optune) · [portopt](https://github.com/superkush06/portopt) · [garch](https://github.com/superkush06/garch) · [risk](https://github.com/superkush06/risk) · [kalman](https://github.com/superkush06/kalman) · [regimes](https://github.com/superkush06/regimes) · [bayes](https://github.com/superkush06/bayes) · [rl-gym](https://github.com/superkush06/rl-gym) · [mlrun](https://github.com/superkush06/mlrun) · and a betting stack: [oddslib](https://github.com/superkush06/oddslib) · [dixoncoles](https://github.com/superkush06/dixoncoles) · [kelly-bet](https://github.com/superkush06/kelly-bet) · [arbfinder](https://github.com/superkush06/arbfinder)</sub>

<sub>[LinkedIn](https://www.linkedin.com/in/kushagra-behl/) · kushagra@gatech.edu</sub>
