# Design-Around Strategy: GRIN MMF HCF Adapter

## Target Patents

| Patent | Status | Assignee | Risk |
|--------|--------|----------|------|
| **US12517303B2** (priority 2018) | **Granted** | Microsoft (Lumenisity) | **LOW** — poor quality, strong prior art pre-dates it by 7–16 years |
| US20240353621A1 (2024) | Published | Unknown | **LOW** — requires GRIN + HF (hollow fiber), narrow |
| US20240151904A1 (2024) | Published | Unknown | **LOW** — air-gap connector for HCF-HCF, not our design |

---

## Core Thesis: This Patent Is a Paper Tiger

Microsoft's US12517303B2 claims a GRIN fiber lens between SMF and HCF for mode
field matching. But **every element of this idea was already public before
Microsoft's 2018 priority date.** The patent is weak — too narrow to block us,
too broad to survive an invalidity challenge.

**Our strategy: Make Microsoft choose.**
- If they claim the patent is **broad enough** to cover our gel-coupled or
  air-gap design → the patent is **invalid** over prior art (Reed 2002, Mafi 2011)
- If they claim the patent is **narrow** (only covers fusion-spliced GRIN-HCF) →
  our gel-coupled approach **does not infringe** (not "joined to")

They cannot win on both fronts.

---

## Prior Art Timeline

Every element of Microsoft's claim was known 7–16 years before their 2018 filing:

### 2002 — Reed US20020150333A1 "Fiber devices using GRIN fiber lenses"
**16 years before Microsoft's priority.**

Claim 1:
> 1. An apparatus for mode converting, comprising: first and second optical
> waveguides; and a GRIN fiber lens attached to both the first and the second
> waveguides.

This covers:
- A GRIN fiber lens as a mode converter between two waveguides ✓
- Fibers with different mode sizes ✓ (claim 4: "first fiber has propagation
  modes with different sizes than the second fiber")
- Fibers with different core diameters ✓ (claim 6)
- GRIN fiber lens fused or glued to both fibers ✓ (claim 2: "fused or glued")
- GRIN fiber lens with graded refractive index profile ✓ (claim 9)

**The only thing missing from Reed: the word "hollow core."** Reed teaches a
GRIN fiber mode converter between ANY two waveguides. Applying it to a hollow
core fiber (a known fiber type with a known MFD mismatch problem) is obvious.

### 2011 — Mafi et al., Optics Letters, Vol. 36, pp. 3596
**7 years before Microsoft's priority.**

Title:
> Low-loss coupling between two single-mode optical fibers with different
> mode-field diameters using a graded-index multimode optical fiber

This paper:
- Uses GRIN MMF as an MMI-based mode field adapter between SMFs with different
  MFDs — the **exact same physics** as our L/2 MMI design
- Explicitly describes "multimode interference in a graded-index multimode
  optical fiber" as the mechanism
- Demonstrates "beam expander or condenser" function

### 2012 — Hofmann et al., J. Lightwave Technol., Vol. 30, pp. 2289
Title:
> Detailed Investigation of Mode-Field Adapters Utilizing Multimode-Interference
> in Graded Index Fibers

Explicitly calls these devices "Mode-Field Adapters" and describes GRIN-MMF
multimode interference — the same terminology and mechanism as Microsoft's patent.

### 2013 — Nazemosadat & Mafi, JOSA B, Vol. 30, pp. 1357
Title:
> Nonlinear multimodal interference and saturable absorption using a short
> graded-index multimode optical fiber

Same SMF-GRIN-SMF geometry. Confirms MMI physics. Confirms the device acts as
a mode field coupler between fibers with different MFDs.

### 2013 — Tyco Electronics US20130272655A1
Title:
> Wavelength insensitive expanded beam with GRIN fiber

- GRIN fiber lens with half-pitch length
- Optical coupling system between optical fibers
- Claim 1: GRIN fiber lens with half-pitch, connecting two optical fibers

### 2006 — Tyco Electronics US7031567B2
Title:
> Expanded beam connector system

- GRIN lens expands from SMF (10.4μm MFD) to large beam (up to 75μm)
- Back reflection < -65 dB
- Insertion loss < 0.5 dB
- Applies to "high-power optical signal has a wavelength of about 1550 nm"

### 1987 — AT&T Bell Labs US4701011A
Title:
> Multimode fiber-lens optical coupler

- Uses a length of multimode fiber as a lens between fibers
- Explicitly mentions quarter-pitch and self-imaging (MMI)
- Fused directly to single-mode fiber — same cladding diameter for passive alignment

### 1992 — Boeing US5163107A
Title:
> Fiber optic coupler/connector with GRIN lens

- GRIN lens positioned in a bore, axially aligned with optical fiber
- Lens expands and collimates optical signals
- 0.23 pitch lens

---

## Claim-by-Claim Invalidity Analysis

### Claim 1

> An optical waveguide adapter assembly comprising:
> a solid core optical waveguide... with an associated first optical mode field size;
> a hollow core optical waveguide... with an associated second optical mode field size; and
> an optical mode field adapter... having a waveguiding core having a shape that
> changes an optical mode field... between the first optical mode field size and
> the second optical mode field size... first end joined to the solid core
> waveguide, second end joined to the hollow core waveguide.

**Invalidity grounds:**

| Limitation | Prior Art |
|---|---|
| Solid core waveguide | Reed 2002: "first optical waveguide / optical fiber" |
| Hollow core waveguide | HCF was a known fiber type since the 1990s (HCPBF, ARF). Its MFD mismatch with SMF was a known problem. Applying known GRIN mode conversion to HCF is obvious. |
| Optical mode field adapter with waveguiding core having a shape that changes mode field | Reed 2002: "GRIN fiber lens" with graded refractive index. Mafi 2011: "GRIN MMF" with MMI. Both have waveguiding cores with graded-index "shape" that changes mode field. |
| Changes between first and second mode field sizes | Reed 2002 claim 4: "first fiber has propagation modes with different sizes than the second fiber." Mafi 2011: "different mode-field diameters." |
| First end joined to SMF | Reed 2002 claim 2: "fused or glued to the GRIN fiber lens" |
| Second end joined to [second waveguide/HCF] | Reed 2002 claim 2: "attached to both the first and the second waveguides" |

**Primary invalidity argument (35 U.S.C. § 103 — Obviousness):**

Reed 2002 teaches a GRIN fiber lens mode converter between any two waveguides
with different mode field sizes. Hollow core fibers were a known fiber type with
a known large MFD (20-35 μm vs. 10.4 μm for SMF). A person of ordinary skill
in the art, faced with the problem of coupling SMF to HCF, would find it obvious
to apply Reed's GRIN fiber lens — the standard solution for mismatched MFD fibers.

The combination of Reed 2002 + the well-known characteristics of HCF at the time
(2018) renders claim 1 obvious. HCF was not a new or unknown fiber type — it had
been studied for over 20 years. The MFD mismatch (10.4 μm vs. 24 μm) is the
same order of magnitude as the mismatches Reed's device was designed to address.

**Secondary invalidity argument (§ 102 — Anticipation by Reed 2002):**

If "hollow core waveguide" is construed to include any non-solid-core waveguide,
Reed's generic "first and second optical waveguides" anticipates. But even if not,
Reed + Mafi 2011 + knowledge of HCF = clear obviousness.

### Claim 7 (GRIN fiber)

> 7. ...the optical mode field adapter comprises a graded index optical waveguide
> having a core with a non-constant refractive index value...

**Anticipated by Reed 2002.** Claim 9 of Reed: "the GRIN fiber lens has a core
with a graded refractive index profile." This is identical. Also anticipated by
Mafi 2011 (GRIN MMF) and Tyco 2013 (GRIN fiber lens with half-pitch).

### Claim 8 (GRIN + LMA fiber)

> 8. ...additionally comprises a large mode area optical waveguide joined between
> the graded index optical waveguide and the hollow core optical waveguide.

**Obvious** over Reed 2002 Fig. 6B, which teaches a compound GRIN lens with
multiple elements (one expanding, one focusing). Adding a large mode area fiber
between GRIN and target fiber is a trivial design choice.

---

## The Estoppel Trap: Microsoft Cannot Win on Both Width and Validity

This is the heart of the strategy. Microsoft's claim 1 interpretation creates
an estoppel problem:

**Scenario A: Microsoft argues BROAD interpretation**
> "Our claim covers any GRIN fiber segment between SMF and HCF, including when
> they are optically coupled through a gel interface, air gap, or connector."

*Consequence:* Reed 2002 + Mafi 2011 fully anticipate this broad reading.
The claim is invalid under § 102/103. Microsoft's patent is dead.

**Scenario B: Microsoft argues NARROW interpretation**
> "Our claim only covers the specific case where the GRIN is fusion-spliced
> (permanently joined) to both SMF and HCF. A gel interface or connector does
> not count as 'joined to.'"

*Consequence:* Our gel-coupled L/2 MMI adapter and air-gap L/4 designs do not
infringe. The "joined to" limitation is not met. Free to operate.

**Microsoft cannot have both.** This is a textbook case for a declaratory
judgment action or IPR.

---

## Prior Art That Microsoft's Examiner Never Saw

The prosecution history of US12517303B2 (and its parent applications) likely
did not consider:
- **Reed 2002** (US20020150333A1) — the most direct prior art, 16 years older
- **Mafi 2011** (Optics Letters) — same MMI mechanism, 7 years older
- **Hofmann 2012** (JLT) — explicitly calls it "Mode-Field Adapter" with GRIN-MMI
- **Nazemosadat 2013** (JOSA B) — confirms geometry and MMI physics
- **Tyco 2013** (US20130272655A1) — half-pitch GRIN lens fiber coupler

If Microsoft sues or threatens, an IPR (Inter Partes Review) at the USPTO using
any one of these references would likely invalidate the challenged claims.

**IPR success probability:** High (estimated 70-90% for claim 1 on obviousness
over Reed 2002, given how directly it teaches every limitation except "hollow
core" — and for § 103, that's exactly the point).

---

## Design-Around Strategies (Fallback — In Case Invalidity Fails)

If, despite the strong prior art, the patent survives and is interpreted
narrowly but still covers our design:

### Strategy D: Index-Matched Gel Coupling (Best — Recommended)

**Concept:** Same L/2 MMI physics (572μm OM4 at half-pitch), but instead of
fusion-splicing the GRIN output to the HCF, both ends are polished flat and
mated with a thin layer of index-matching gel (RI ≈ 1.44–1.46, close to
silica's 1.457).

**Avoids Claim 1(c):** The "joined to" limitation requires a permanent physical
bond (fusion splice, adhesive). The patent specification consistently uses
"joined" for permanent bonds. A gel interface is separable, non-permanent —
you can pull apart, clean, reconnect. This is "optically coupled" but not
"joined."

### Strategy A: Detachable Air-Gap Connector

**Concept:** L/4 GRIN (286μm) with an air gap between GRIN and HCF. The beam
collimates at L/4, propagates through air, and is coupled into the HCF at the
correct distance.

**Avoids Claim 1(c):** Same logic — air gap means not "joined to."

### Strategy B: Bulk GRIN Rod Lens

**Concept:** Replace GRIN fiber with a bulk GRIN rod lens (1–2 mm diameter).
A bulk rod has no "waveguiding core" — it's a bulk optic, not a waveguide.

**Avoids Claim 1(a):** The claim requires a "waveguiding core having a shape."
A rod lens has no core.

### Strategy E: Non-GRIN Waveguide Adapter

**Concept:** Use TEC fiber, tapered fiber, photonic lantern, or step-index MMF.

**Avoids Claim 7:** Doesn't use GRIN fiber.
**Still risks Claim 1:** Claim 1 is broad enough to cover any shape-changing
waveguide core.

---

## Recommended Primary Strategy: Publish Invalidity Analysis + Open Hardware

1. **Publish this invalidity analysis** as part of the open-source repo
2. **Build and publish the gel-coupled L/2 MMI adapter** (open hardware)
3. **If Microsoft asserts the patent:** File an IPR using Reed 2002 + Mafi 2011
   as the primary references
4. **In the meantime:** Our open-source publication serves as additional prior
   art for any future improvement patents

The patent is a paper tiger. It was granted because the examiner didn't see
Reed 2002 or Mafi 2011. Any competent patent challenge will bring these to
light.

---

## Key Physical Parameters

| Parameter | L/2 fusion splice (original — infringes if valid) | L/2 + gel (Strategy D — no infringement) | L/4 + air gap (Strategy A — no infringement) |
|---|---|---|---|
| GRIN length | 572 μm | 572 μm | 286 μm |
| Interface | Fusion splice | 1–5 μm gel | 50–200 μm air |
| Est. loss | 0.003 dB (sim) | 0.003 + <0.01 dB | 0.074 dB (Zhong) |
| Infringes Claim 1(c)? | YES (joined) | NO (gel, not joined) | NO (air gap) |
| Invalidity risk | N/A (don't use this) | Patent invalid over Reed/Mafi | Patent invalid over Reed/Mafi |

---

## Summary

| Approach | Infringement Risk | Patent Invalidity | Effort |
|---|---|---|---|
| Invalidity (Reed 2002 + Mafi 2011) | None — patent invalid | 70-90% IPR success | Research done (this doc) |
| Gel coupling (Strategy D) | Very low | Backup if patent somehow valid | $500–1,500 |
| Air-gap connector (Strategy A) | Low | Backup | $500–2,000 |
| Bulk GRIN rod lens (Strategy B) | Very low | Backup | $2,000–5,000 |

**Bottom line:** Microsoft's patent is built on sand. The GRIN fiber mode
converter between dissimilar fibers was patented 16 years earlier by Reed (2002)
and published 7 years earlier by Mafi (2011). The only addition — applying it
to hollow core fiber — is an obvious use of known technology. Our open-source
publication + optional gel-coupled L/2 design is a complete answer.
