<!-- The panel is a real gradient-descent run on an ill-conditioned quadratic:
     the contours are true level sets, the zig-zag is what a fixed learning
     rate actually does. Regenerate with `python3 make_panel.py`. -->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="gd-dark.svg">
  <img alt="Kushagra Behl — ML research at MIT, growth engineering at Slashy (YC S25), Math & Computing at Georgia Tech" src="gd-light.svg" width="824">
</picture>

Math &amp; Computing at **Georgia Tech**. ML, startups, and finance — mostly LLM systems that have to work on real traffic, and quant libraries where the math has to check out against the paper.

**LLM pipelines and agentic workflows** · **RAG over vector databases** · **prompt and eval iteration in production** · **Next.js full-stack** · **ML from scratch in NumPy** — autodiff, transformers, backprop by hand · **quant methods** — SVI calibration, Fama-MacBeth, bandit regret analysis · **econometrics** in R, MATLAB, and GAMS

## Experience

**Machine Learning Research Assistant — MIT, Center for Collective Intelligence** · Jun 2026 –
LLM-based argument mining: pulling claims and their supporting reasons out of unstructured discussion and giving them structure.

**Technologist in Residence — Trifecta Enterprises, Philly AI Lab** · May 2026 –
Built a RAG pipeline that embeds LinkedIn posts, newsletters, and articles into a vector database so the whole content library is queryable in natural language. Streams Claude API responses to surface topic gaps, engagement patterns, and next-post recommendations.

**Growth &amp; Software Engineer — Slashy** `YC S25` · May 2026 –
Shipped [slashy.com/blog](https://slashy.com/blog) — a full-stack Next.js app where agentic AI drafts and publishes content autonomously. Wired LLM pipelines into social and email outreach so distribution runs at scale. Also LLM optimization and social growth.

**Research Assistant — The Wharton School** · May 2026 –
Health economics: OECD healthcare spending and policy interventions. Collection, analysis, and visualization in R, MATLAB, and NumPy.

**Growth &amp; Operations — Knowunity** · Mar – May 2026
Ran content growth with 11 UGC creators to **1.3M+ organic views** in the US market. Knowunity is Europe's #1 AI learning app — 20M+ users, ~$50M raised.

**Market Research — dSilo.ai** · Jul – Sep 2025
Competitive analysis across finance and compliance agentic AI; fed positioning and UVP work.

**Independent research** · Apr 2024 –
Modeled minimum-wage shocks on GDP and CPI across 10 states with a graduate-level CGE model in GAMS, reviewed with economists at Villanova.

## Libraries

Nineteen of them, each with tests, CI, and a validation doc that checks its numbers against published results or closed-form answers. Six worth your time:

**[transformer-from-scratch](https://github.com/superkush06/transformer-from-scratch)** — GPT-style decoder in pure NumPy
Backprop derived by hand. All 29 parameter tensors agree with finite differences; the causal mask is verified by ablation rather than assumed.

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

## What "validated" means here

Each library ships a `docs/validation.md` that runs its own numbers against an outside source, with verdicts derived from the measurements — break the library and the table goes red.

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

## Also around

[optune](https://github.com/superkush06/optune) · [portopt](https://github.com/superkush06/portopt) · [garch](https://github.com/superkush06/garch) · [risk](https://github.com/superkush06/risk) · [kalman](https://github.com/superkush06/kalman) · [regimes](https://github.com/superkush06/regimes) · [bayes](https://github.com/superkush06/bayes) · [rl-gym](https://github.com/superkush06/rl-gym) · [mlrun](https://github.com/superkush06/mlrun)

A quant sports-betting stack: [oddslib](https://github.com/superkush06/oddslib) de-vigs market prices · [dixoncoles](https://github.com/superkush06/dixoncoles) models the scoreline · [kelly-bet](https://github.com/superkush06/kelly-bet) sizes the bet · [arbfinder](https://github.com/superkush06/arbfinder) finds the arb when two books disagree.

<br>

<sub>Outside the code: Director of Fundraising at Plover International — 130,000+ hygiene products donated and $21,200+ raised, with UPenn and YMCA partnerships. Top 70 international at DECA ICDC (2× qualifier), 3rd in Pennsylvania in Financial Math.</sub>

<sub>[LinkedIn](https://www.linkedin.com/in/kushagra-behl/) · kushagra@gatech.edu</sub>
