# EP2721819 — "Entropy Coding Supporting Mode Switching"

## Key Facts

| Field | Value |
|-------|-------|
| **Patent** | EP2721819B1 |
| **Title** | Entropy Coding Supporting Mode Switching |
| **Priority Date** | June 16, 2011 |
| **Original Applicant** | Fraunhofer-Gesellschaft |
| **Current Owner** | Dolby Video Compression LLC (via GE acquisition, 2024) |
| **Status** | Granted (Aug 2023), Active, expires June 2032 |
| **Litigation** | Asserted against AV1 implementers at UPC (2025-2026) |
| **Assignee at Filing** | Fraunhofer (German publicly-funded research institute) |

## Summary

EP2721819 claims an entropy coding/decoding system that supports two modes:
- **Low-complexity mode** (cheaper coding, less compression)
- **High-efficiency mode** (better compression, higher complexity)

The mode is selected based on the data stream, and the entropy decoding scheme used depends on which mode is active.

The patent admits this concept was already present in H.264/AVC (2003) — wherein Baseline profile used CAVLC (low complexity) and Main profile used CABAC (high efficiency) — but argues that its novelty lies in making both modes available within a single decoder/profile rather than requiring separate profiles.

---

## Prior Art Timeline

```
1988 ─ IBM US5045852A: Dynamic model selection during arithmetic coding
2003 ─ H.264/AVC Standard: Baseline (CAVLC) / Main (CABAC) profiles
2005 ─ Samsung US20060233254A1: Adaptive context model selection for entropy coding
2006 ─ US20060158355A1: Adaptive entropy encoding for scalable video
2009 ─ Apple US20090304071A1: Switching between CAVLC and CABAC per constraints
2011 ─ EP2721819 priority date
```

---

## Claim Construction & Prior Art Mapping

### Independent Claim 1 (Decoder)

| Limitation | H.264/AVC (2003) | Apple US20090304071A1 (2009) | IBM US5045852A (1991) |
|------------|-------------------|-------------------------------|------------------------|
| **1a. A decoder for decoding a data stream into which media data is coded** | H.264 decoder decodes a bitstream containing coded video data. | "Video decoder 150 receives encoded data from the channel 190" [FIG. 1] | "Decoding... compressed data stream" |
| **1b. A mode switch configured to activate a low-complexity mode or a high-efficiency mode depending on the data stream** | **ADMITTED PRIOR ART**: "The H.264 video coding standard offers a baseline profile and a main profile" where "CABAC is available only in the main profile rather than the base line profile" (spec [0004]). Profile is signaled in SPS. | "Input data is encoded into a set of encoded data... selecting an encoding that maximizes quality... based on at least one of a bitrate constraint and a computational complexity constraint" [Abstract]. Selector 533 chooses between CAVLC (low complexity) and CABAC (high efficiency). | "at least two models are run... and the model with the best coding performance... is selected" [Abstract]. Model selection is coded into compressed data. |
| **1c. An entropy decoding engine configured to retrieve each symbol of a sequence of symbols by entropy decoding from the data stream using a selected one of a plurality of entropy decoding schemes** | H.264 Baseline uses CAVLC (variable length decoding); Main profile uses CABAC (arithmetic decoding). Both are "plurality of entropy decoding schemes." | "Entropy coding methods (e.g. CABAC and CAVLC in H.264)" [0038]. Two separate entropy encoders (534, 536) selected by selector 533. | "each model... with a given model... coded with an adaptive arithmetic coder" [Abstract]. Multiple coding models available. |
| **1d. A desymbolizer configured to desymbolize the sequence of symbols in order to obtain a sequence of syntax elements** | H.264 defines binarization/desymbolization: CABAC uses binarization to convert syntax elements to bin strings; CAVLC directly decodes syntax elements from variable-length codes. | Not explicitly claimed (standard H.264 desymbolization applies to both CAVLC and CABAC paths). | "strings of decisions or data, based on phenomena or events... generated using a model" [col 6]. |
| **1e. A reconstructor configured to reconstruct the media data based on the sequence of syntax elements** | H.264 decoder uses inverse transform, motion compensation, and intra prediction to reconstruct video frames from decoded syntax elements. | "Video decoder 150... replica of the source video sequence from the coded video data is decoded" [0023]. | Standard decoder reconstruction from decompressed data. |
| **1f. Wherein the selection depends on the activated one of the low-complexity mode and the high-efficiency mode** | **DIRECTLY DISCLOSED**: If Main profile is selected → CABAC used. If Baseline profile is selected → CAVLC used. The entropy decoding scheme depends entirely on the profile (mode). | "the entropy coding for each picture may be predetermined based on... selected model of the target decoder... switching by the encoder between CABAC and CAVLC" [0044]. Controller 540 controls selector 533 based on models 550, 560. | "the best model is chosen on the basis of which model coded the most input symbols" [Abstract]. Model selection is explicit and coded in stream. |

### Key Observation

**Limitations 1d (desymbolizer) and 1e (reconstructor) are generic video decoder functions present in every block-based video codec since H.261 (1990).** These are not inventive elements. The only potentially novel element is 1b + 1f (mode-dependent entropy scheme selection), but that is:

1. **Admitted prior art** in H.264/AVC (2003): profile determines entropy scheme
2. **Explicitly anticipated** by US20090304071A1 (Apple, 2009): CAVLC/CABAC switching based on constraints

---

## Independent Claim 12 (Decoder, Alternative)

This claim adds the limitation that the control parameter (e.g., probability model adaptation rate) varies at a first rate in high-efficiency mode and is constant or varies at a slower second rate in low-complexity mode.

### Prior Art Mapping

| Limitation | IBM US5045852A (1991) | Samsung US20060233254A1 (2006) |
|------------|----------------------|----------------------------------|
| **Control parameter varies at first rate in high-efficiency mode** | "The statistics, or probability estimates, for the unused model paths are reset" — i.e., active model's statistics are continuously adapted (first rate). | "the coding method for the residual prediction flag according to the calculated value of the CBP" — different context models with different adaptation rates. |
| **Control parameter constant or slower rate in low-complexity mode** | "the statistics for the unused model paths are reset to the values they had at the start of the block" — slower adaptation or no adaptation for non-selected models. | Standard H.264 CAVLC uses fixed VLC tables with minimal context adaptation (slower rate than CABAC). |

---

## Invalidity Arguments

### Argument 1: Anticipation by H.264/AVC (Admitted Prior Art)

EP2721819's own specification admits that H.264/AVC (2003) had exactly the claimed invention:

- H.264 Baseline profile = low-complexity mode (CAVLC, variable length coding)
- H.264 Main profile = high-efficiency mode (CABAC, arithmetic coding)
- Profile selection signaled in bitstream (SPS) → mode switching "depending on the data stream"
- Entropy decoding scheme determined by profile selection → "selection depends on activated mode"

The patent attempts to distinguish by arguing that in H.264, "base line profile conform decoders may be configured less complex than main profile conform decoders" and that "main profile conform de/encoders have to be backwards compatible with baseline profile." But the **claimed invention does not require a single decoder that handles both modes** — the claims recite "a decoder" with a mode switch, which is exactly what an H.264 Main profile decoder is: a decoder that handles both CAVLC (baseline) and CABAC (main) bitstreams.

**Conclusion:** All limitations of claim 1 are found in H.264/AVC (2003), which predates the priority date by 8 years.

### Argument 2: Anticipation by US20090304071A1 (Apple, 2009)

This application explicitly discloses:

- **Two entropy coding methods**: CAVLC (low complexity) and CABAC (high efficiency) — see [0004]: "The H.264 standard allows two types of entropy coding: CAVLC and CABAC... CABAC has better coding efficiency than CAVLC, but is much more computationally complex."
- **Mode switching based on constraints**: "bitrate constraint and a computational complexity constraint" — see [0013]: "the set of encoded data complies with a given set of constraints, which include at least one of a bitrate constraint and a computational complexity constraint."
- **Granular switching**: "entropy coding for each picture may be predetermined... switching by the encoder 110 between CABAC and CAVLC" — see [0044].
- **Signaling**: "may include an indicator of the type of entropy encoding used" — see [0045].

This predates EP2721819's priority date by 2 years and anticipates every limitation.

### Argument 3: Anticipation by IBM US5045852A (1991)

This patent is a 21-year predated fundamental disclosure of:

- Dynamic model selection between multiple coding models during arithmetic coding
- Running multiple models in parallel and selecting the best-performing one
- Coding the model selection decision in the compressed stream
- Starting each block with coder parameters from the previous block

While this is framed in general data compression (not specifically video), it covers the general concept of "entropy coding supporting mode switching" in its broadest sense.

### Argument 4: Obviousness (All Prior Art Combined)

Even if a single reference does not anticipate each limitation, the combination of:

- H.264/AVC (2003): established the framework of profile-based entropy coding selection
- US20090304071A1 (2009): explicitly teaches dynamic CAVLC/CABAC switching within a single encoder/decoder
- US5045852A (1991): teaches dynamic model selection during arithmetic coding

...makes the claimed invention obvious under any standard. A person of ordinary skill in 2011 would have found it trivial to:
1. Take H.264's existing CAVLC/CABAC dual-mode framework
2. Apply Apple's teaching of constraint-based switching between them
3. Implement within a single decoder

---

## Estoppel Analysis for Dolby

If Dolby attempts to narrow EP2721819 during litigation to avoid H.264/AVC prior art, they face the following estoppel traps:

| Narrowing Argument | Estoppel Consequence | What Becomes Unenforceable |
|--------------------|----------------------|---------------------------|
| "Prior art uses profiles, not modes within a single profile" | Cannot assert against single-profile bitstreams (e.g., AV1 Main profile that switches entropy schemes) | AV1, VP9, HEVC Main |
| "Prior art uses global switching, not per-slice/per-block" | Cannot assert against per-picture or per-slice switching (H.264 already does per-picture via SPS) | Most implementations |
| "Prior art doesn't have a desymbolizer with controllable mapping" | Narrow to specific binarization scheme not found in AV1 | AV1 uses different binarization |
| "Our invention uses rate-adaptive probability estimation" | IBM 1991 already does this | Cannot exclude IBM's prior art |

---

## Recommended Design-Around for AV1 Implementers

### Option A: Always use AV1's native symbol-to-symbol adaptation

AV1's entropy coding uses a fundamentally different approach: forward-adaptive symbol-to-symbol adaptation (Daala-style) rather than mode-switching between two distinct entropy coders. If Dolby asserts EP2721819, argue that AV1 does not have "a low-complexity mode and a high-efficiency mode" — it has a single unified entropy coding system that adapts continuously.

### Option B: Uniform adaptation rate

AV1 can be configured where the entropy adaptation rate is uniform (or where the "low complexity" path uses a separately-coded non-adaptive scheme like the "palette" or "compound" modes). Configure the codec to avoid any explicit "mode switch" that selects between fundamentally different entropy decoding engines.

### Option C: Prove anticipation in IPR/PGR

File an IPR (Inter Partes Review) at the USPTO or opposition at the EPO using the prior art identified in this document. The combination of H.264 + Apple 2009 provides a strong invalidity case under any standard.

---

## Sources

- EP2721819A1: https://patents.google.com/patent/EP2721819A1/en
- US20090304071A1 (Apple, 2009): https://patents.google.com/patent/US20090304071A1/en
- US20060233254A1 (Samsung, 2006): https://patents.google.com/patent/US20060233254A1/en
- US5045852A (IBM, 1991): https://patents.google.com/patent/US5045852A/en
- H.264/AVC Standard (ITU-T Rec. H.264 | ISO/IEC 14496-10, 2003)
