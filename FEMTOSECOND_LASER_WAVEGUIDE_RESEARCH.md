# Femtosecond Laser Direct Writing — Can It Solve Fiber's Unsolved Problems?

## Summary

Companies like **Femtoprint** (Switzerland) and formerly **OptoScribe** (UK, now POET Technologies) use focused femtosecond laser pulses to write 3D waveguides inside bulk glass, modifying the refractive index at the focus point. This creates optical paths that can route, split, and mode-convert light without discrete components.

---

## 1. Commercial Players & Current Specs

### Femtoprint (femtoprint.ch)
| Parameter | Spec |
|---|---|
| Propagation loss | **<0.2 dB/cm** |
| Min bend radius | **20-25 mm** (at 1000-1550nm) |
| Refractive index change | **10⁻² to 10⁻³** |
| Wavelength range | 650-1550nm |
| Min mode field diameter | 6-8μm |
| Materials | Fused silica, Borofloat 33, Eagle XG |
| Max substrate | 200×200mm, up to 32mm thick |
| Accuracy | <1μm positioning |
| Surface roughness | <10nm Ra |
| Also does | Glass fiber ferrules (sub-micron holes/V-grooves), monolithic integration of waveguides + micro-optics + alignment structures |

Femtoprint has a **commercial platform** — not just lab research. They sell a laser microfabrication system and also offer contract manufacturing at wafer scale. Actively working on **detachable low-loss fiber connectors** (Optica GAMA 2026 panel).

### OptoScribe / POET Technologies
- Was UK-based, acquired by POET Technologies (publicly traded)
- Focus: glass interposers for co-packaged optics
- Less public detail on current specs post-acquisition
- Published work on 3D mode-field converters and fan-in/fan-out devices

---

## 2. State of the Art (Academic/Research, 2024-2026)

| Metric | Record | Source |
|---|---|---|
| **Propagation loss** | **0.07 dB/cm** | Fused silica, 1550nm — multiple groups (arxiv 2408.06688, Opt. Lett. 2025) |
| **Coupling loss to SMF** | **0.045 dB/facet** | OCMS method — Light: Sci & Appl 2024 |
| **Total insertion loss** | **<0.29 dB** for a waveguide | Light: Sci & Appl 2024 (OCMS) |
| **Bend loss** | **0.01 dB/cm** at R>6mm | Ion-exchanged glass waveguides — OFC 2026 |
| **MCF fan-in/out (4-core)** | **<0.5 dB** avg insertion loss | OFC 2026, writing speed >30 mm/s |
| **90° tight bend** | **1.028 dB/cm** at 10mm radius | Opt. Lett. 50(5) 2025 |
| **Mode overlap with SMF** | **98.8%** | arxiv 2408.06688 |
| **Writing speed** | **>30 mm/s** | OFC 2026 (mass-producible target) |

---

## 3. Application to Fiber's Biggest Problems

### 3.1 Hollow-Core Fiber to SMF Adapter

**The problem:** HCF mode field diameter (~24μm) vs SMF (~10μm). Direct splicing gives high loss. Current solutions: GRIN lens or tapered fiber — bulk, alignment-sensitive.

**Laser-written solution:** Write a **3D GRIN taper** inside a glass chip — gradually transition from 24μm mode to 10μm mode over a few mm. The refractive index profile can be precisely controlled by varying laser exposure parameters along the length.

**Status:** Mode-field converters for SMF-to-large-mode-area fiber demonstrated in research (OCMS method, Light 2024). **No commercial product for HCF specifically.** Needed: writing long (>5mm) tapers at production speed.

### 3.2 Multi-Core Fiber Fan-In/Fan-Out

**The problem:** MCF cores are tightly packed (19-50μm pitch). Connecting each core to a separate SMF requires complex 3D routing.

**Laser-written solution:** This is the **most mature application.** A laser-written glass chip routes each MCF core to a separate SMF pitch (127μm or 250μm) using 3D waveguide curves.

**Status:** **Production-ready.** 4-core achieved at <0.5 dB insertion loss with writing speed >30 mm/s (OFC 2026). Scaling to 7-core and 19-core in progress. Femtoprint offers this commercially.

### 3.3 Bend-Loss Elimination in Tight Spaces

**The problem:** Tight fiber bends (<10mm radius) in FTTH, data centers, and patch panels cause macrobending loss.

**Laser-written solution:** A glass interposer with laser-written waveguides can route light at sharp angles with **0.01 dB/cm bend loss** (vs >1 dB for a tight fiber bend). The glass chip becomes the "bend" — light stays inside the glass block, never sees a tight radius.

**Status:** Demonstrated in labs. Not yet commercialized as a drop-in connector replacement. Femtoprint is working toward this (detachable connector panel, GAMA 2026).

### 3.4 Polarization-Maintaining / Mode-Selective Couplers

**The problem:** Mode-division multiplexing needs precise LP01/LP11 conversion. Current photonic lanterns are complex.

**Laser-written solution:** 3D waveguide mode-selective couplers demonstrated with **>99.5% coupling ratio**, >25 dB extinction ratio, broadband (1500-1610nm) — Light: Sci & Appl 2024.

---

## 4. Fundamental Limits & Open Challenges

| Challenge | Detail |
|---|---|
| **Propagation loss vs SMF** | 0.07 dB/cm is **350× worse** than SMF (0.2 dB/km). For <1cm on-chip, fine. For >1m interconnects, loss adds up. |
| **Writing speed** | 30 mm/s → 3 seconds for a 10cm waveguide. Femtosecond laser writing is inherently serial. Parallel-beam or burst-mode could scale, but not yet. |
| **Material uniformity** | Borosilicate glass has better write properties than fused silica but worse thermal stability. |
| **Reliability/qualification** | No ITU or Telcordia standard for laser-written glass waveguides. Telcos need GR-20, GR-326 qualification. Femtoprint/POET are working toward this but not there yet. |
| **HCF-specific taper** | Writing a precise 24μm→10μm taper needs long, adiabatic structures. Writing speed becomes a bottleneck for production. |
| **Cost per unit** | Laser time + glass substrate + polishing. For datacom at scale, needs to compete with molded plastic or etched silicon photonics. Promising for low-to-mid volume, not mass market yet. |

---

## 5. Verdict

| Problem | Can laser writing solve it? | Readiness |
|---|---|---|
| **MCF fan-in/out** | ✅ Yes, already working | **Near production** (<0.5 dB, >30 mm/s) |
| **HCF-to-SMF adapter** | ⚠️ Technically possible, not built | **Lab demonstration needed** |
| **Sharp bend elimination** | ✅ Yes, proven at 0.01 dB/cm | **Productization needed** |
| **Fiber connector replacement** | ⚠️ Femtoprint working on it | **In development** |
| **Replacing SMF entirely** | ❌ Propagation loss 350× worse | **Not viable for long-haul** |

**Where it could be a genuine breakthrough for fiber's unsolved problems:**

The **HCF-to-SMF adapter** is the most valuable single application. If a laser-written glass chip could splice HCF to SMF at <0.5 dB loss for production cost under $50, it removes the biggest barrier to hollow-core fiber deployment — its incompatibility with the existing fiber plant. That's worth watching.
