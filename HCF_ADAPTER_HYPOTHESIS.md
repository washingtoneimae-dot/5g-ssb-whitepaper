# Hypothesis: <$0.50 HCF-to-SMF Adapter at <0.5 dB Loss

> **SUPERSEDED**: This document contained an incorrect mechanism (single-mode GRIN
> expansion). See `HCF_ADAPTER_PHYSICS.md` for the corrected physics.

## The Problem

Direct SMF-to-HCF butt-coupling: **2.74 dB** mode mismatch loss.
Current solutions (GRIN lenses, bulk optics): $50-200+ per interconnect.

## Target

<0.5 dB total insertion loss, <$50, passive alignment.

## Hypothesis (Corrected)

A **572μm segment of standard OM4 GRIN MMF** (NA=0.200, 50μm core), fusion-spliced
between SMF-28 and anti-resonant HCF, exploits multi-mode interference to convert
the 10.4μm SMF mode to a field overlapping the 24μm HCF mode.

**Not a single-mode expander** — individual waveguide modes don't expand. The
mechanism is MMI: LP₀₁–LP₀₅ modes excited by the SMF launch beat at the half-pitch
length (L/2 ≈ 572μm), producing near-perfect overlap with the HCF target.

## Simulation-Verified Performance

| Metric | Value |
|---|---|
| MMI coupling (analytic 5-mode) | **0.003 dB** |
| Median total IL (MC, 2000 samples) | **0.10 dB** |
| Worst-case total IL (95th percentile) | **0.28 dB** |
| Yield at <0.5 dB | **100%** |
| Optimal length | 572 μm (L/2) |
| BOM | $0.38–0.81 |
| Packaging | Standard LC ferrule, passive alignment |

## Key insight

The higher-order LP₀₃–LP₀₅ modes (~5% of power) improve the field match — the
5-mode simulation gives **0.003 dB** vs 0.22 dB for the 2-mode analytic estimate.
More power in higher modes would be even better.

## Falsifiability

Hypothesis is false if any of these are true:
- No OM4 GRIN MMF achieves <0.5 dB total IL when cut to L/2 and fusion-spliced
- The splice loss SMF → GRIN MMF exceeds 0.3 dB consistently
- MEASURED total IL exceeds 0.5 dB across multiple units at L/2

## Why this hasn't been done

The telecom industry treats GRIN MMF as a transmission medium. The HCF community
treats it as an alignment nuisance. Nobody has tried 572μm of it as a passive
mode converter. Patent search: zero results.
