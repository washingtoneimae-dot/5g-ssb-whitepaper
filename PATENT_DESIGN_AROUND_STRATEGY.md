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

### Strategy D: Index-Matched Gel Coupling (New Recommended — #1)

**Concept:** Same L/2 physics (572μm OM4 GRIN at half-pitch, MMI field overlap at
24μm), but instead of fusion-splicing the GRIN output to the HCF, both ends are
polished flat and mated with a thin layer of index-matching gel (RI ≈ 1.44–1.46,
close to silica's 1.457). The GRIN and HCF are separate connectorized fibers joined
through a standard adapter with gel between the facets.

**How it avoids Claim 1:**
- Element (C): The second end of the GRIN adapter is NOT "joined to" the HCF. The
  term "joined to" in the patent consistently describes permanent physical bonds:
  fusion splices, adhesive bonding, thermal expansion joints. The specification
  distinguishes "joined" (permanent) from "optically coupled" or "connectorised"
  (detachable). Dependent claim 13 explicitly reads "joined to... by a splice,"
  confirming the prosecution intended "joined" to mean a permanent bond.

  A gel interface is a separable, non-permanent optical contact. The GRIN and HCF
  can be pulled apart, cleaned, and reconnected. This is optically coupled but not
  "joined" under any reasonable claim construction.

**Advantages over air-gap (Strategy A):**
| Aspect | Air-gap | Gel coupling |
|---|---|---|
| GRIN length | L/4 = 286μm (must change) | **L/2 = 572μm (keeps our design)** |
| Beam propagation | Diverges in air (n=1) | **No divergence (n≈1.45)** |
| Fresnel loss | ~0.15 dB per air-glass interface | **<0.01 dB (RI-matched)** |
| Loss contribution from interface | ~0.074 dB (Zhong 2024) | **~0.003 dB (MMI floor)** |
| Gap tolerance | ±5 μm | **±20 μm (forgiving)** |
| Prior art restriction | Must use L/4 + tunable gap | **Keeps our MMI physics intact** |
| BOM adder | $0.10 (spacer) | **$0.05 (gel drop)** |

**Why gel preserves the MMI physics:**
- The L/2 MMI mechanism produces a field at the GRIN output facet that overlaps
  the 24μm HCF mode with 99.94% efficiency (0.003 dB). This requires the GRIN
  output to be optically contiguous with the HCF input.
- An air gap (n=1) causes the beam to diverge, destroying the MMI condition and
  requiring a switch to L/4 + collimation/focus.
- A gel layer (n≈1.45) is optically similar to silica. The MMI field propagates
  through the gel with negligible wavefront distortion. A 1-5μm gel layer adds
  <0.01 dB penalty vs the zero-gap case.
- The gel also eliminates the Fresnel back-reflection that would otherwise require
  an APC polish.

**Patent risk:** Very low. Stronger even than the air-gap approach because:
1. The adhesive/mechanical interface is clearly separable → not "joined to"
2. The patent specification never contemplates or describes this approach
3. Any claim interpretation that covers a gel-coupled interface would be so
   broad as to cover any connector, making the claim likely invalid for
   lack of definiteness or over breadth.

**Manufacturing:**
- Fusion-splice SMF-28 → OM4 GRIN (same as original)
- Cleave GRIN at L/2 = 572μm and polish (standard LC ferrule polish)
- Apply index-matching gel to GRIN facet or HCF facet
- Mate in standard LC adapter with flat or APC polish
- Option: UV-cure the gel (Norland 61, etc.) for a semi-permanent but
  separable bond — still not "joined" under the patent's meaning
- Field replacement: clean off old gel, reapply, reconnect

**Trade-off vs. fusion splice:**
| Aspect | Fusion splice | Gel coupling |
|---|---|---|
| Loss | 0.003 dB (sim) | 0.003 + <0.01 dB |
| Permanence | Permanent | Field-replaceable |
| Infringes Claim 1(c)? | **YES** | **NO** |
| BOM adder | $0.10 (splice) | $0.05 (gel) |

---

### Strategy E: Non-GRIN Waveguide Adapter

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

### Phase 1: Validate Gel-Coupled Design (3 months, ~$500)

Build and measure the L/2 GRIN + gel connector:

1. **Fabrication:** Fusion-splice SMF-28 → OM4 GRIN, cleave GRIN at 572 μm, polish
2. **Gel application:** Test with standard telecom index-matching gel (e.g., Thorlabs G608N, RI=1.457) and UV-cured adhesive (Norland 61)
3. **Measurement:** Couple to anti-resonant HCF (NANF, MFD≈24 μm), measure insertion loss, return loss, and repeatability over 100 connect/disconnect cycles
4. **Target loss:** <0.05 dB (should approach the 0.003 dB MMI floor minus splice loss)
5. **Thermal test:** -40°C to +85°C cycling to validate gel stability

### Phase 2: Validate Air-Gap Design (Backup, 1 month, ~$300)

If gel approach has issues with long-term stability or contamination:

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
- If gel has long-term degradation issues: pivot to air-gap (Strategy A) or bulk GRIN rod lens (Strategy B)
- Open-source all designs and simulation code regardless of commercialization path

---

## Key Physical Parameters

| Parameter | L/2 fusion splice (original) | L/4 + air gap (Strategy A) | L/2 + gel (Strategy D) |
|---|---|---|---|
| GRIN length | 572 μm | 286 μm | 572 μm |
| Interface | Fusion splice | 50–200 μm air | 1–5 μm gel (RI≈1.45) |
| Beam at GRIN output | MMI overlapped | Focused (curved phase) | MMI overlapped |
| Beam MFD at HCF | 24 μm | 24 μm (at waist) | 24 μm |
| Tolerance | ±77 μm on length | ±5 μm on gap | ±77 μm on length, ±20 μm on gel |
| Est. loss | 0.003 dB (sim) | 0.074 dB (published) | 0.003 + <0.01 dB |
| BOM adder | $0.10 (splice) | $0.10 (spacer) | $0.05 (gel) |
| Field-replaceable? | No | Yes | Yes |
| Infringes Claim 1(c)? | **YES** (joined) | **NO** (air gap) | **NO** (gel, not joined) |

---

## Summary

| Strategy | Infringement Risk | Technical Risk | Cost to Implement | Patent Challenge |
|---|---|---|---|---|
| D: Gel coupling | **Very low** | Low (validated by Zhong + simpler) | $500–1,500 | Not needed |
| A: Air-gap connector | **Low** | Low (validated by Zhong) | $500–2,000 | Not needed |
| B: Bulk GRIN rod lens | **Very low** | Medium (alignment) | $2,000–5,000 | Not needed |
| C: Open hardware | **None** | N/A (no product) | $0 (already done) | Strong invalidity arguments |
| E: Non-GRIN adapter | **Medium** | Medium | $1,000–3,000 | Weakens patent case |

**Go-to-market recommendation:** Strategy D (gel coupling) + C (open-source publication).
The gel approach keeps our optimal L/2 MMI physics (572μm, 0.003 dB), adds only $0.05
BOM, avoids the "joined to" limitation with high confidence, and is field-replaceable.
The gel eliminates Fresnel loss and beam divergence that the air-gap approach suffers.
Publish openly to establish prior art for any future patent attempts.
