## Kushagra Behl

Math &amp; Computing at Georgia Tech.

I like the problems where the math *is* the product. An order book is just a priority queue until you ask who wins a race to the same quote — then it's a latency model. A vol surface is just interpolation until you notice that careless interpolation invents arbitrage out of nothing. A bandit is a for-loop until someone asks you to prove the regret bound.

Most of what's below started with me being unsatisfied by knowing the *name* of something.

<img src="https://raw.githubusercontent.com/superkush06/vol-surface/main/docs/demo.png" width="100%" alt="calibrated SVI implied volatility surface" />

<sub>SVI fitted across five expiries with no calendar arbitrage — total variance has to be non-decreasing in T at every strike, or a calendar spread is free money. From <a href="https://github.com/superkush06/vol-surface">vol-surface</a>.</sub>

<br>

**Now** &nbsp;·&nbsp; ML research at MIT's Center for Collective Intelligence, on LLM argument mining &nbsp;·&nbsp; growth engineering at Slashy (YC S25)

**Before** &nbsp;·&nbsp; Health economics research at Wharton &nbsp;·&nbsp; DECA ICDC Business Finance, 2× international qualifier &nbsp;·&nbsp; 3rd in Pennsylvania, Financial Math &nbsp;·&nbsp; SIG Discovery

<br>

### Markets

|  |  |
| :-- | :-- |
| [**lobster**](https://github.com/superkush06/lobster) | An order book that matches the way an exchange actually does: price-time priority, partial fills, self-trade prevention. Replays real NASDAQ message data and tells you when the reconstruction drifts |
| [**vol-surface**](https://github.com/superkush06/vol-surface) | Black-Scholes, Hagan SABR, and SVI fitted across expiries. Keeping the surface arbitrage-free is the entire difficulty |
| [**factor-zoo**](https://github.com/superkush06/factor-zoo) | Momentum, value, quality, low-vol — reproduced with the look-ahead traps removed, which is most of why published premia are hard to hit |
| [**optune**](https://github.com/superkush06/optune) | Greeks by adjoint autodiff. Barriers priced with a Brownian bridge, because discrete monitoring quietly overprices a knock-out by 20% |
| [**portopt**](https://github.com/superkush06/portopt) · [**garch**](https://github.com/superkush06/garch) · [**risk**](https://github.com/superkush06/risk) · [**kalman**](https://github.com/superkush06/kalman) | Markowitz through Black-Litterman · GARCH and its asymmetric cousins · VaR, expected shortfall, and where VaR stops being coherent · Kalman, EKF, UKF |

<img src="https://raw.githubusercontent.com/superkush06/lobster/main/docs/demo.png" width="100%" alt="limit order book simulation" />

<sub>Four agents — two noise, one momentum, one market maker — trading against each other in <a href="https://github.com/superkush06/lobster">lobster</a>. Mid price on top, bid-ask spread below.</sub>

<br>

### Machine learning

|  |  |
| :-- | :-- |
| [**gauss-bandit**](https://github.com/superkush06/gauss-bandit) | UCB1, Thompson, EXP3, LinUCB — with measured regret plotted against the bound each paper actually promises |
| [**transformer-from-scratch**](https://github.com/superkush06/transformer-from-scratch) | A GPT-style decoder in pure NumPy, backprop derived by hand, then checked against finite differences until all 29 parameter tensors agreed |
| [**tinydiff**](https://github.com/superkush06/tinydiff) | Reverse-mode autodiff in under 500 lines. Enough to train a real network, small enough to read in one sitting |
| [**regimes**](https://github.com/superkush06/regimes) · [**bayes**](https://github.com/superkush06/bayes) · [**rl-gym**](https://github.com/superkush06/rl-gym) · [**mlrun**](https://github.com/superkush06/mlrun) | HMMs and PELT change-point detection · HMC and variational inference · Q-learning through A2C · a zero-dependency experiment tracker |

<img src="https://raw.githubusercontent.com/superkush06/gauss-bandit/main/docs/demo.png" width="100%" alt="cumulative regret curves" />

<sub>Cumulative regret over 2,000 rounds. Thompson sampling flattens out early; EXP3 keeps paying for an adversary that was never there. From <a href="https://github.com/superkush06/gauss-bandit">gauss-bandit</a>.</sub>

<br>

Every one of these ships with tests, CI, and a validation document that checks its numbers against published results or closed-form answers — including the rows where they *disagree*. I'd rather ship a library that admits a 2.7% miss than one that quietly widens the tolerance until the test goes green. I build them with Claude Code.

There's also a betting stack, because pricing a match is the same problem in a smaller suit: [oddslib](https://github.com/superkush06/oddslib) strips the vig out of market odds, [dixoncoles](https://github.com/superkush06/dixoncoles) models the scoreline, [kelly-bet](https://github.com/superkush06/kelly-bet) sizes the bet, and [arbfinder](https://github.com/superkush06/arbfinder) finds the arb when two books disagree.

<br>

---

[LinkedIn](https://www.linkedin.com/in/kushagra-behl/) &nbsp;·&nbsp; [kushagra@gatech.edu](mailto:kushagra@gatech.edu)
