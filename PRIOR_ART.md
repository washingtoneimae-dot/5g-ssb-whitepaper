# Prior Art: GRIN-Fiber HCF Adapter

This document catalogues known prior art for using GRIN (graded-index) fiber as a
mode-field adapter between single-mode fiber (SMF) and hollow-core fiber (HCF).

## Verdict

**The concept of a GRIN fiber segment as an SMF-to-HCF mode adapter is fully
anticipated by published literature and granted patents.** This repo's contribution
is an independent theoretical re-derivation, a clean analytic MMI model, and a cost
analysis — not a novel invention.

## Academic Publications

### Suslov et al. 2021 — *Scientific Reports*
- **Title:** "Low-loss SMF to NANF coupling via GRIN fiber"
- **Key result:** SMF → OM4 GRIN → NANF, **0.15 dB loss**, optimal GRIN length
  250–350 μm (quarter-pitch regime with free-space gap)
- **Authors:** ORC University of Southampton (Poletti, Slavík group)
- **Significance:** Same fiber types (OM4 GRIN, SMF-28, anti-resonant HCF/NANF).
  Achieved <0.2 dB experimentally — better than our simulation prediction.

### Zhong et al. 2024 — *Journal of Lightwave Technology*
- **Title:** "SMF-to-HCF coupling via GRIN fiber with 0.074 dB loss"
- **Key result:** Experimentally demonstrated **0.074 dB loss** with gap optimization
- **Authors:** ORC Southampton
- **Significance:** Our simulation predicted 0.003 dB (idealized analytic) to 0.077 dB
  (numerical). They achieved 0.074 dB — validating the approach.

### Zhong et al. 2024 — *ACS Photonics*
- **Title:** "Offset-spliced SMF-GRIN + angle-cleaved HCF"
- **Key result:** 0.6 dB loss, **−64 dB back-reflection**
- **Significance:** Engineering refinement for low back-reflection applications

### Mičín et al. 2025 — *IEEE IPC*
- **Title:** "GRIN + coreless fiber for high-power beam expansion"
- **Key result:** Beam expansion to 50 μm MFD, <0.2 dB loss
- **Significance:** Extension to high-power regime (different target MFD)

## Patents

### US12517303B2 (Granted 2026, Priority 2018)
- **Assignee:** Microsoft Technology Licensing (Lumenisity)
- **Title:** "GRIN fiber lens as a mode field adapter in a connector ferrule"
- **Coverage:** SMF-to-HCF mode field adapter using GRIN fiber in a connector
  ferrule — **exactly the concept described in this repo**
- **Status:** Granted. Claims cover GRIN fiber segment fusion-spliced between SMF
  and HCF within a ferrule assembly.

### US20240353621A1 (Filed 2024)
- **Assignee:** Unknown (Sterlite?)
- **Title:** "All-fiber GRIN + hollow fiber for SMF-to-HCF coupling"
- **Coverage:** GRIN fiber with an intermediate hollow fiber segment, fusion
  spliced, FC/APC packaging
- **Status:** Published application. Uses custom hollow fiber between GRIN and
  target HCF — different from our OM4-direct-to-HCF approach, but same principle.

### US20240151904A1 (Filed 2024)
- **Assignee:** Unknown
- **Title:** "HCF connector with air gap and mode adapter"
- **Coverage:** Connector design for HCF mentioning mode adapter requirement
- **Status:** Published application. Peripheral — describes the problem space.

## Key Differences (This Repo vs. Prior Art)

| Aspect | Prior Art | This Repo |
|--------|-----------|-----------|
| Optimal length | L/4 + free-space gap (Suslov, Zhong) | **L/2** (half-pitch, no gap) |
| GRIN fiber type | OM4, custom GRIN | **Standard OM4 only** ($0.50/m) |
| Cost analysis | None | **$0.38–0.81 BOM**, $5–15 retail |
| Mechanism description | Brief | **Full analytic MMI derivation** |
| Monte Carlo tolerance | None | **2000-sample sensitivity analysis** |
| Release | Closed / paywalled | **Open source (MIT)** |

## Implications

- **Not patentable** — fully anticipated by Microsoft's granted patent
  (US12517303B2, priority 2018) and Southampton's publications since 2021
- **Scientifically correct** — our independent derivation reaches the same
  conclusions as published experimental results (0.074–0.15 dB loss)
- **Open-source value** — this repo provides the cleanest public derivation of
  the MMI mechanism, a full tolerance analysis, and a cost model not found in
  the academic literature
