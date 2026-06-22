# Addendum: Signal Integrity, UE Confound, and Redundancy Mechanisms

## The UE Movement Problem (Revisited)

The whitepaper signal model is:

Δθ_k = θ_elastic(wind_k) + δ_plastic(k) + ε_k

This assumes the logged phase correction reflects tower deformation. A valid question: does UE movement also create a confound?

## Answer: Two Layers of Redundancy

### Layer 1 — 3-Sector Panels

Typical 5G macro sites deploy 3 panels at 120° intervals. Tower tilt is common mode — affects all panels proportionally. UE movement affects only the serving panel. Differential across panels cancels thermal drift and local noise.

### Layer 2 — Stationary-UE Filtering

With 10+ active UEs per sector: identify stationary UEs via doppler shift and timing advance, then average phase corrections across them. Tower tilt is common to all UEs; a moving phone affects only its own beam.

### Combined: 3 panels × 10+ stationary UEs = 30x+ redundancy

## Open Question

Does the vendor BBU expose per-UE beam weight data or internal calibration measurements through standard interfaces? Unknown without real logs from a tower operator.

## Tower Operators to Approach

IHS Towers, ATC, Helios Towers, Eaton Towers (Africa). Offer: free 3-month pilot, anonymized logs only, no hardware/truck roll/risk.
