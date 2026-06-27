# Design-Around Strategy: GRIN MMF HCF Adapter

## Target Patents

| Patent | Status | Assignee | Risk |
|--------|--------|----------|------|
| **US12517303B2** (priority 2018) | **Granted** | Microsoft (Lumenisity) | **HIGH** — independent claim 1 is broad |
| US20240353621A1 (2024) | Published | Unknown | **MEDIUM** — requires GRIN + HF (hollow fiber), narrow |
| US20240151904A1 (2024) | Published | Unknown | **LOW** — air-gap connector for HCF-HCF, not our design |

## Claim Analysis — US12517303B2

**Claim 1 (independent):**
> 1. An optical waveguide adapter assembly comprising:
> a solid core optical waveguide [SMF] extending between a free end and a coupled end and having a solid waveguiding core with an associated first optical mode field size;
> a hollow core optical waveguide [HCF] extending between a free end and a coupled end and having a hollow waveguiding core with an associated second optical mode field size; and
> an optical mode field adapter extending between a first end and a second end and having a waveguiding core having a shape that changes an optical mode field of a waveguided optical signal substantially between the first optical mode field size at the first end of the optical mode field adapter and the second optical mode field size at the second end of the optical mode field adapter, wherein:
> the first end of the optical mode field adapter is joined to the coupled end of the solid core optical waveguide, and
> the second end of the optical mode field adapter is joined to the coupled end of the hollow core optical waveguide.

**Critical limitations in Claim 1:**
- **(A)** Adapter has "a waveguiding core having a shape that changes an optical mode field"
- **(B)** First end "joined to" SMF coupled end
- **(C)** Second end "joined to" HCF coupled end

**Dependent claims 7-8 (GRIN-specific):**
> 7. ...the optical mode field adapter comprises a graded index optical waveguide having a core with a non-constant refractive index value...
> 8. ...additionally comprises a large mode area optical waveguide joined between the graded index optical waveguide and the hollow core optical waveguide.

---

## Design-Around Strategies

### Strategy A: Detachable Air-Gap Connector (Recommended — #1)

**Concept:** The GRIN is fusion-spliced to SMF inside a standard LC/APC connector ferrule. The HCF is terminated in its own ferrule with an air-gap spacer. They mate in a standard adapter. The GRIN is NOT "joined to" the HCF.

**How it avoids Claim 1:**
- Element (C): The second end of the GRIN adapter is NOT "joined to" the HCF. There is an air gap (50–100 μm) between the GRIN output facet and the HCF input facet. They are mechanically mated connectors, not permanently joined.
- The "coupled end" of the HCF (per the claim) would need to be spliced to the adapter. Instead, the HCF's end is in a connector that mates via a physical interface with an air gap.

**GRIN length for air-gap operation:**
- L/2 (572 μm, half-pitch) — the beam is collimated at the GRIN output → needs the HCF immediately at the output → this is the "joined" case we're avoiding.
- L/4 + gap (≈286 μm + 50–200 μm gap) — beam focuses at a distance. The gap distance is tuned so the focused beam waist matches the HCF MFD (24 μm). This is exactly the approach validated by Zhong et al. 2024 (0.074 dB loss).
- L/4 + coreless fiber spacer (≈286 μm CSF + 50–200 μm gap) — same principle, used by Mičín et al. 2025.

**Physics for the air-gap case:**
- GRIN at L/4 collimates the SMF output → then the beam diverges → place the HCF at the distance where divergence produces the right MFD
- OR: GRIN slightly longer than L/4 → beam focuses at a distance → place HCF at the focal point with flat phase front
- Coupling efficiency: η = (2·w₁·w₂/(w₁²+w₂²))² where w₁, w₂ are the beam waist at the GRIN output and the HCF MFD
- Zhong et al. achieved 0.074 dB experimentally with this approach

**BOM comparison:**
| Component | Contact (L/2) | Air-gap (L/4) |
|---|---|---|
| GRIN segment | 572 μm | 286 μm |
| Additional parts | None | Gap spacer (ring/washer) |
| Est. loss | 0.003 dB (sim) | 0.074 dB (published) |
| Est. BOM | $0.38–0.81 | $0.45–0.95 |

**Patent risk:** Low. The air gap clearly avoids "joined to" limitation. Gap-based connectors are well-known prior art (US20240151904A1 teaches this for HCF-HCF). The combination is a straightforward extension.

**Prior art strength for invalidity:** If the patent owner argued the air-gap connector still infringes, the Southampton group's published work (Suslov 2021, Zhong 2024) all used gap-based approaches. Any claim interpretation broad enough to cover the gap would likely be invalidated by this prior art.

---

### Strategy B: Bulk GRIN Rod Lens in Connector Housing

**Concept:** Replace the GRIN FIBER segment with a bulk GRIN ROD LENS (1–2 mm diameter × 2–4 mm length). The SMF is held in a ferrule with the GRIN rod lens in a lens holder. The beam goes from SMF → free space → GRIN rod → free space → HCF.

**How it avoids Claim 1:**
- Element (A): The patent requires "a waveguiding core having a shape that changes an optical mode field." A bulk GRIN rod lens does NOT have a "waveguiding core" — light propagates through it in quasi-free-space, not confined by total internal reflection in a core. It's a bulk optic lens, classified under G02B 6/32, not G02B 6/14 (mode converters).
- Element (C): Same as Strategy A — the GRIN rod is in a connector housing, not "joined to" the HCF.

**Trade-offs:**
| Aspect | GRIN fiber segment | GRIN rod lens |
|---|---|---|
| Core/cladding structure | 125 μm cladding, 50 μm core | 1–2 mm rod, no core |
| Guidance mechanism | Waveguide (TIR + MMI) | Bulk refraction |
| Patent classification | G02B 6/14 (mode converter) | G02B 6/32 (lens) |
| Est. BOM | $0.38–0.81 | $1.50–5.00 |
| Alignment accuracy | Passive (ferrule bore) | Active (lens holder) |

**Patent risk:** Low. Bulk GRIN lenses in fiber connectors are well-known prior art predating the Microsoft patent (Corning/US Conec patents since 2013). The key limitation "waveguiding core" is genuinely missing.

**Caveat:** Some patent claims may use broad language that could arguably cover any GRIN element. But the independent claim specifically requires "a waveguiding core having a shape" — a rod lens has no core at all.

---

### Strategy C: Open Hardware + Freedom-to-Operate (Defensive)

**Concept:** Publish the L/2 MMI design as open-source hardware. Do not commercialize. If the Microsoft patent is asserted against users of the design, challenge its validity.

**Validity challenges to US12517303B2:**

1. **Anticipated by Suslov et al. 2021 (Scientific Reports):** Published before the earliest priority date? No — priority is Oct 2018, and Suslov was 2021. BUT if Suslov is prior art under pre-AIA or if the patent's claims are not entitled to the 2018 priority date (e.g., if the PCT application's disclosure doesn't support the granted claims), Suslov could be prior art. This is fact-specific.

2. **Obviousness over Suslov + standard GRIN lens references:** Given that GRIN fiber lenses were well-known for mode field conversion between dissimilar SMFs (long before 2018), applying the same technique to SMF↔HCF would be obvious. This is a strong argument.

3. **Obviousness over prior art GRIN lens patents:** Corning/US Conec had GRIN lens connector patents since 2013 (US9022669B2, priority 2012). The Microsoft patent adds the specific application to HCF — which is an obvious use of an existing technique.

4. **Claim construction:** The term "joined to" may be narrowly construed to mean "permanently bonded or spliced" based on the specification (which only describes splices and fusion bonds). Under this construction, our air-gap connector does not infringe.

**Patent risk (for defensive publication):** Low. If we publish and don't sell, there's no damages exposure. Users of the design could be sued, but we provide them with invalidity arguments.

---

### Strategy D: Non-GRIN Waveguide Adapter

**Concept:** Use a different mode-field conversion mechanism that doesn't use GRIN fiber:
- **Thermally expanded core (TEC) fiber** — heat the SMF end to diffuse the core
- **Tapered fiber** — physically pull the fiber to create a core/waveguide taper
- **Photonic lantern** — transition from single-core to multi-core structure
- **Step-index MMF MMI** — use a short segment of standard step-index MMF (instead of GRIN MMF) to create MMI at a different optimal length

**How it avoids Claim 7 (GRIN-specific):**
- These approaches don't use GRIN fiber, so dependent claim 7 is clearly avoided.
- But independent claim 1 still applies if there's any "waveguiding core having a shape that changes" the mode field.

**Patent risk:** Medium. Claim 1 is broad enough to cover TEC and tapered fibers (the patent explicitly describes these in FIGS. 11-12 as alternative embodiments). But a non-waveguide approach (Strategy B) or a non-joined approach (Strategy A) would still be needed in combination.

---

## Recommended Development Path

### Phase 1: Validate Air-Gap Design (3 months, ~$500)

Build and measure the L/4 GRIN + air-gap connector:

1. **GRIN optimization:** Simulate the optimal gap distance for OM4 GRIN (NA=0.200) at L/4 (286 μm) to match 24 μm HCF MFD
2. **Fabrication:** Fusion-splice SMF-28 → OM4 GRIN, cleave GRIN at 286 μm, polish
3. **Measurement:** Couple to anti-resonant HCF (NANF, MFD≈24 μm) with variable air gap
4. **Target loss:** <0.2 dB (the Zhong et al. benchmark is 0.074 dB)

### Phase 2: Connector Prototype (3 months, ~$2,000)

- Design LC/APC ferrule with integrated GRIN and air-gap spacer
- Test with spaced HCF connector per US20240151904A1 methods (open art, royalty-free)
- Measure insertion loss, return loss, mechanical stability, temperature cycling

### Phase 3: Risk Mitigation

- If patent challenge is needed: retain prior art references (Suslov 2021, Zhong 2024, US9022669B2, Shi 2024)
- If air-gap approach has higher loss than acceptable: pivot to Strategy B (bulk GRIN rod lens)
- Open-source all designs and simulation code regardless of commercialization path

---

## Key Physical Parameters for Air-Gap Design

| Parameter | L/2 contact (our original) | L/4 + gap (recommended) |
|---|---|---|
| GRIN length | 572 μm | 286 μm |
| Gap distance | 0 μm | 50–200 μm (tuned) |
| Beam at GRIN output | Collimated (flat phase) | Focused (curved phase) |
| Beam MFD at HCF | 24 μm (MMI overlapped) | 24 μm (at waist) |
| Tolerance | ±77 μm on length | ±5 μm on gap |
| Est. loss | 0.003 dB (sim) | 0.074 dB (published) |
| Infringes Claim 1(c)? | **YES** (joined) | **NO** (air gap) |

---

## Summary

| Strategy | Infringement Risk | Technical Risk | Cost to Implement | Patent Challenge |
|---|---|---|---|---|
| A: Air-gap connector | **Low** | Low (validated by Zhong) | $500–2,000 | Not needed |
| B: Bulk GRIN rod lens | **Very low** | Medium (alignment) | $2,000–5,000 | Not needed |
| C: Open hardware | **None** | N/A (no product) | $0 (already done) | Strong invalidity arguments |
| D: Non-GRIN adapter | **Medium** | Medium | $1,000–3,000 | Weakens patent case |

**Go-to-market recommendation:** Strategy A (air-gap connector) + C (open-source publication). The air-gap approach has been experimentally validated by the Southampton group, avoids the "joined to" limitation with high confidence, and is implementable with standard connector hardware. Publish openly to establish prior art for any future patent attempts.
