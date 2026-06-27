# Dolby's AV1 Patent Enforcement

## Background

AV1 is a video codec developed by the Alliance for Open Media (AOM) — Google,
Mozilla, Cisco, Amazon, Netflix, Apple, Meta, Microsoft, etc. It was explicitly
**promised to be royalty-free.** Companies adopted it based on this promise.

Dolby **is not an AOM member** and made no royalty-free commitment. In 2024,
they acquired GE Licensing for **$429M**, picking up 5,000+ video compression
patents including ones declared essential to AV1.

## Enforcement Actions (as of mid-2026)

| Target | Court | Codec | Status |
|--------|-------|-------|--------|
| **Snap Inc.** | US (Delaware) + Brazil (Rio) | AV1 + HEVC | Filed Mar 2026; 4 patents asserted (US10855990, US9924193, US9596469, US10404272) |
| **TPV/Philips** (Europe) | UPC Hamburg | AV1 | Filed Jun 2026; EP2721819 asserted — first AV1 UPC case |
| **Skyworth** | Brazil (Rio de Janeiro) | AV1 | Preliminary injunction granted May 2026 |

Dolby is seeking **injunctions** — not just royalties. They have made no FRAND
commitment for AV1. As of mid-2026, Dolby has filed 10 total UPC cases and 7 have settled.

### Key Litigation Details

- **Dolby v. Snap (Delaware)**: First AV1 lawsuit against a streamer. US10404272
  ("Entropy encoding and decoding scheme") is the key patent Dolby seeks an
  injunction over. Dolby filed in Access Advance pool, not Sisvel.
- **Dolby v. TPV (UPC Hamburg)**: First AV1 UPC case. Dolby Video Compression
  (GE subsidiary) asserting EP2721819 ("Entropy Coding Supporting Mode
  Switching") against Philips-branded TV maker.
- **Dolby v. Skyworth (Brazil)**: Preliminary injunction already granted.
  Patents licensed through Sisvel pool.

## Known Asserted Patents

| Patent | Title | Origin | Pool | Status |
|--------|-------|--------|------|--------|
| **EP2721819** | Entropy Coding Supporting Mode Switching | Fraunhofer → GE → Dolby | Sisvel AV1 | **Analyzed** — strong prior art (H.264, Apple 2009) |
| **US10404272** | Entropy Encoding and Decoding Scheme | Fraunhofer → GE → Dolby | Access Advance | **Pending analysis** — priority Jan 2011, asserted in Snap suit |
| **US10499058** | Quantization Control for Variable Bit Depth | Dolby | Sisvel AV1 (AV1-003) | **Analyzed** — **EXPIRED** May 2025; continuations may remain |
| US10728554 | Quantization Control for Variable Bit Depth (cont.) | Dolby | Sisvel AV1 (AV1-003) | Continuation of US10499058 |
| JP6561098 | [TBD - AV1-019] | Dolby | Sisvel AV1 (AV1-019) | Not yet analyzed |
| US10855990 | Inter-plane prediction | GE → Dolby | Access Advance | Asserted in Snap suit |
| US9924193 | Picture coding supporting block merging and skip mode | GE → Dolby | Access Advance | Asserted in Snap suit |
| US9596469 | Sample array coding for low-delay | GE → Dolby | Access Advance | Asserted in Snap suit |

## Prior Art Status

| Patent | Status | Key Prior Art | Confidence |
|--------|--------|---------------|------------|
| **EP2721819** | **Analysis complete** — see [EP2721819_ANALYSIS.md](./EP2721819_ANALYSIS.md) | H.264/AVC (2003), Apple US20090304071A1 (2009), IBM US5045852A (1991) | Very strong |
| **US10499058** | **Analysis complete** — see [US10499058_ANALYSIS.md](./US10499058_ANALYSIS.md) | **Patent expired** May 2025. Prior art: JPEG 2000 (2000), MPEG-4 N-Bit (2002), H.264 FRExt (2004) | Expired — moot |

## Standardization History

EP2721819 was **not disclosed during AV1 standardization** (2015-2018):
- Originally owned by **Fraunhofer** (German research institute), not an AOM member
- Fraunhofer contributed to HEVC but was not part of AOM/AV1 development
- GE acquired the patent (GE Video Compression LLC) at an unknown date
- Dolby acquired it in 2024 via the GE deal
- AOM members could not have known about this Fraunhofer patent

However, Fraunhofer had no duty to disclose to AOM, so equitable estoppel is weak.

### Prior Challenges to Dolby Patents

- **Unified Patents** (a patent defense org) has already opposed Dolby AV1 patents at the EPO:
  - Filed opposition against EP2659675 (Dolby) in Jan 2021 — related to Sisvel AV1 pool
  - **Successfully revoked EP3798988** (Dolby HEVC/AV1) in Jan 2024 — all claims revoked
- This shows the EPO is willing to revoke Dolby's patents when prior art is presented

## Sisvel AV1 Pool

The Sisvel AV1 pool lists **~1,943 patents** (as of late 2025) from 20+ licensors:
Dolby, GE, Philips, ETRI, NTT, JVCKENWOOD, Toshiba, KAIST, KBS, and others.
Dolby participates via two entities: **Dolby International AB** and
**Dolby Video Compression LLC** (formerly GE).

| Dolby Entity | Pool Count |
|-------------|------------|
| Dolby International AB | AV1-003 (US10499058 family), AV1-005 (US8374237), AV1-019 (JP6561098 family) |
| Dolby Video Compression LLC | EP2721819 + GE patents |

Fees: Sisvel charges $0.20/unit for AV1 (capped), lower for VP9.

## Why This Matters

AV1 was designed to be a royalty-free alternative to HEVC/H.265. If Dolby can
enforce old Fraunhofer/GE patents against it, the entire royalty-free premise
collapses. Small players who adopted AV1 in good faith now face licensing
demands or injunction risk.

Key points:
- **Dolby did not contribute to AV1** — they bought patents after the standard was finalized
- **No FRAND commitment** — Dolby is free to seek injunctions
- **Double-dipping**: GE patents were not committed royalty-free; Dolby acquired them post-hoc
- **AOM members' patents** were cross-licensed royalty-free, but third-party patents (Fraunhofer, GE, Nokia) were not

## Files

| File | Description |
|------|-------------|
| [EP2721819_ANALYSIS.md](./EP2721819_ANALYSIS.md) | Full claim chart & prior art for first UPC-asserted AV1 patent |
| [US10499058_ANALYSIS.md](./US10499058_ANALYSIS.md) | Analysis of expired quantization patent (AV1-003) |
| [README.md](./README.md) | Dolby overview |
| [OPUS.md](./OPUS.md) | Dolby's Opus patent pool through Vectis |
