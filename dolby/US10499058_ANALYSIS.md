# US10499058 — "Quantization Control for Variable Bit Depth"

## Key Facts

| Field | Value |
|-------|-------|
| **Patent** | US10499058B2 |
| **Title** | Quantization Control for Variable Bit Depth |
| **Priority Date** | May 19, 2004 |
| **Original Assignee** | Dolby Laboratories Licensing Corp |
| **Current Owner** | Dolby Laboratories Licensing Corp |
| **Status** | **Expired** (expired May 11, 2025) |
| **Sisvel AV1 Designation** | AV1-003 (also US10728554B2) |
| **AV1 Sections Mapped** | 2, 4.7, 4.8, 5.5.1, 5.5.2, 5.11.35, 5.11.39, 6.4.1, 6.4.2, 6.4.5, 6.10.33, 6.10.34, 7.12, 7.12.1, 7.12.2, 7.12.3, E, E.1, E.2, E.3, E.3.1 |

## Summary

US10499058 claims a method for quantizing video data where the quantization step-size is normalized to the bit depth of the data, so that a given quantization parameter (QP) produces the same rate-distortion performance regardless of whether the input is 8-bit, 10-bit, or higher. This "QP invariance" allows bitstreams at different bit depths to share the same syntax and semantics.

The patent's key idea: prior codecs normalized quantization step-size to the **least significant bit** (LSB), causing QP to mean different things at different bit depths. This patent normalizes to the **most significant bit** (MSB) instead.

---

## Prior Art

### H.264/AVC Fidelity Range Extensions (FRExt, 2004)

H.264 FRExt, finalized concurrently with this patent's priority date (2004), already supported:
- Bit depths up to 14 bits per sample
- 4:4:4 chroma sampling
- The patent itself discusses H.264 extensively as prior art (col. 4-6)

The patent admits: "H.264/AVC is considered the state-of-the-art in modern video coding" and that H.264 already had "an in-loop deblocking filter, many modes for intra-prediction, a new integer transform, two modes of entropy coding... and so on."

### MPEG-4 N-Bit Profile (2001)

MPEG-4 Visual's N-Bit profile (ISO/IEC 14496-2:2001/Amd 1:2002) already supported:
- Bit depths of up to 12 bits
- The patent explicitly discusses this as prior art: "the prior art does nothing to normalize the effects of varying bit depth"

### MPEG-2 Studio Profile (1995)

MPEG-2 Studio Profile already supported:
- 10-bit and 12-bit sampling
- Higher bit depth quantization

### JPEG 2000 (2000)

JPEG 2000 (ISO/IEC 15444-1:2000) already:
- Supported bit depths from 1 to 38 bits
- Used a normalization approach where quantization was designed to be independent of bit depth
- Defined explicit quantization step-size signaling that accounted for bit depth

### Key Admission in the Patent

The patent acknowledges that in H.264, the quantization step-size distribution already used an "exponential mapping" that was more uniform than prior MPEG-2 "identity mapping." This means H.264 was already closer to achieving QP invariance:
> "The exponential mapping has the same density of quantization step-sizes for each octave... this makes the extension of quantization to higher bit depth much more efficient for H.264 with its exponential mapping than with the identity mapping of MPEG-2."

---

## Invalidity Arguments

### Argument 1: Obviousness over H.264 FRExt + Standard Practice

By 2004, extending quantization parameter ranges to accommodate higher bit depths was a well-known engineering practice:
- H.264 FRExt (2004) already extended 8-bit H.264 to support up to 14 bits
- The exponential QP-to-QStep mapping in H.264 inherently provided uniform step-size coverage
- The patent's "invention" is simply continuing the QStep curve to cover additional bit depths

### Argument 2: Anticipation by JPEG 2000 (2000)

JPEG 2000 (published Dec 2000, 4 years before priority date) already:
- Supported variable bit depths from 1 to 38 bits
- Defined quantization step-size explicitly, with independent control of step-size magnitude relative to the data range
- Used a normalization that was independent of bit depth

### Argument 3: Anticipation by MPEG-4 N-Bit (2002)

MPEG-4 N-Bit profile (standardized 2002) already:
- Extended MPEG-4 Visual to support 12-bit data
- Used quantization parameters mapped to step-sizes
- The patent admits this and admits that the prior art "does nothing to normalize the effects of varying bit depth" — which means the claimed MSB normalization is the only difference, and it's a well-known design choice.

### Argument 4: Lacks Novelty Over H.264 FRExt

H.264 FRExt (joint final draft, March 2004 — 2 months before priority date) already:
- Defined QP values and quantization for bit depths up to 14 bits
- Used the same exponential QP-to-QStep mapping that the patent relies on
- The difference (MSB vs LSB normalization) is a mathematical equivalence — normalizing to MSB produces the same mathematical result as adjusting QP values to account for bit depth in the LSB-normalized system

---

## Current Status

**This patent has expired** (expired May 11, 2025). It cannot be asserted for past infringement, and any future products using AV1 would not be subject to this patent after its expiration date unless the patent has been extended.

However, the Sisvel AV1 pool still lists it (AV1-003), and continuation patents (US10728554B2, US10951893B2, US11812020B2) may extend the family.

---

## Continuation Patents

| Patent | Filing Date | Status | Expiry |
|--------|-------------|--------|--------|
| US10499058B2 (AV1-003) | Oct 2, 2018 | **Expired** | May 11, 2025 |
| US10728554B2 | Nov 26, 2019 | Active | TBD |
| US10951893B2 | Jul 27, 2020 | Active | TBD |
| US11812020B2 | Mar 15, 2021 | Active | TBD |

---

## Design-Around

AV1 uses a different quantization structure than Dolby's patent. Specifically, AV1 uses:
- **Quantizer index** → DC/AC delta QP per block
- **Separate quantization matrices** for luma/chroma
- **Quantization step-size** derived from a base index with per-block delta values

To avoid any potential claim in the continuation family, AV1 implementers should ensure:
1. Quantization step-size derivation is explicitly based on the AV1-specified formula (not the Dolby-normalized formula)
2. Bit depth normalization, if implemented, follows the JPEG 2000 approach (which predates the patent)
3. Any continuation patents are evaluated independently — their claims may differ

---

## Sources

- US10499058B2: https://patents.google.com/patent/US10499058B2/en
- US9113165B2 (parent): https://patents.google.com/patent/US9113165/en
- H.264/AVC FRExt (JVT document JVT-L047, March 2004)
- JPEG 2000: ISO/IEC 15444-1:2000
- MPEG-4 N-Bit: ISO/IEC 14496-2:2001/Amd 1:2002
- MPEG-2 Studio Profile: ISO/IEC 13818-2:1995/Amd 1:1996
