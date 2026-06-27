# Open-Source Fiber Optics Research

Independent research into telecom and fiber optic problems. Two projects in this repo:

---

## 1. HCF-to-SMF Adapter — GRIN MMF Mode Converter

A **$0.50 passive adapter** for connecting hollow-core fiber (HCF) to standard
single-mode fiber (SMF-28), using **572 μm of standard OM4 GRIN MMF** as a
multi-mode interference (MMI) mode converter.

### Performance (simulated)

| Metric | Value |
|---|---|
| MMI coupling (analytic 5-mode) | **0.003 dB** |
| Median total IL (MC, 2000 samples) | **0.10 dB** |
| 95th percentile total IL | **0.28 dB** |
| Yield at <0.5 dB | **100%** |
| Optimal length | 572 μm (L/2 half-pitch) |
| BOM | **$0.38–0.81** |

### Status

**Prior art exists** (see [PRIOR_ART.md](PRIOR_ART.md)). The concept is fully
anticipated by:
- University of Southampton ORC group — experimental 0.074 dB loss since 2021
- Microsoft/Lumenisity — granted patent US12517303B2 (priority 2018)

This repo provides the **cleanest public derivation** of the MMI physics, a
full tolerance analysis, Monte Carlo simulation, cost model, and a **patent
design-around strategy** — released as open source.

### Files

- [`HCF_ADAPTER_PHYSICS.md`](HCF_ADAPTER_PHYSICS.md) — Full physics derivation
- [`HCF_ADAPTER_HYPOTHESIS.md`](HCF_ADAPTER_HYPOTHESIS.md) — Hypothesis statement
- [`PATENT_DESIGN_AROUND_STRATEGY.md`](PATENT_DESIGN_AROUND_STRATEGY.md) — Four strategies to work around US12517303B2
- [`simulate_adapter.py`](simulate_adapter.py) — Numerical eigenvalue solver
- [`fast_sweeps.py`](fast_sweeps.py) — Vectorized analytic sweeps + MC
- [`PRIOR_ART.md`](PRIOR_ART.md) — Prior art documentation
- [`simulation/`](simulation/) — Diagnostic plots and results

---

## 2. 5G SSB Phase-Shift Observer (Archived)

A zero-hardware structural health monitoring concept for telecom towers using
existing 5G BBU phase correction logs.

**Status: Abandoned** — raw beam phase correction data is not exportable via
any standard BBU interface. See [`ACQUISITION_PATHWAY.md`](ACQUISITION_PATHWAY.md)
for the analysis.

### Archived Files

- [`5G_SSB_Phase-Shift_Observer.md`](5G_SSB_Phase-Shift_Observer.md) — Original whitepaper
- [`ACQUISITION_PATHWAY.md`](ACQUISITION_PATHWAY.md) — Data acquisition analysis
- [`BBU_LOG_RETENTION_RESEARCH.md`](BBU_LOG_RETENTION_RESEARCH.md) — BBU log research
- [`FEMTOSECOND_LASER_WAVEGUIDE_RESEARCH.md`](FEMTOSECOND_LASER_WAVEGUIDE_RESEARCH.md)
- [`INVESTOR_THESIS.md`](INVESTOR_THESIS.md)

---

## Author

**Washington Imae** — [github.com/washingtoneimae-dot](https://github.com/washingtoneimae-dot)
GPG: `7989 D2E2 1C9D 29E6 5742 2BCA 2B88 E816 5712 F528`

## License

MIT — see [LICENSE](LICENSE)
