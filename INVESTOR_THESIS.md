# 5G SSB Phase-Shift Observer

## Zero-Hardware Structural Health Monitoring for Telecom Towers

**Investment Thesis — 2 pages**

---

### The Problem

Telecom operators spend $4-6 billion annually on structural maintenance for 5 million towers worldwide. Current inspection methods are slow, expensive, and reactive:

| Method | Resolution | Frequency | Cost per tower/yr |
|---|---|---|---|
| Manual visual inspection | ~0.5° tilt | Every 3-5 years | $100-300 |
| Tilt sensor hardware | ~0.1° | Continuous | $500-1,000 |
| Drone survey | ~1 cm | Quarterly | $200-500/flight |

**Result:** Most towers are structurally invisible between inspections. A failure costs $200,000-500,000 per tower plus service disruption penalties. Damage accumulates silently until it's too late.

---

### The Solution

Every 5G tower already generates the data needed for structural health monitoring — the SSB phase correction log. When a tower deforms by fractions of a degree from wind or structural creep, the Baseband Unit applies a beam correction. That correction IS the measurement.

**The SSB Observer reads this existing log and extracts 15 structural health metrics — no sensors, no hardware, no tower climbs. Zero additional cost per tower.**

---

### Market

| Segment | Size | Our Beachhead |
|---|---|---|
| Global tower SHM market | $4-7B (2026), growing to $17-27B by 2033 (19% CAGR) | 5G-capable towers (~1.2M) |
| African tower market | ~200K towers, $120M SAM | Kenya (~8,000 towers), East Africa |
| Tower maintenance spend | $800-1,200/tower/year | Replace $500/yr tilt sensors with $0 software |

**Go-to-market:** Start with African tower operators (lower competition, urgent need, personal network). Expand to global via SaaS licensing.

---

### The Hardware We Read — Already Installed, Already Paid For

A typical 5G macro cell site costs **$85K–$290K** to build. The SSB Observer uses **zero additional hardware** — we read one log from equipment already on the tower.

**Tower-top equipment (30-100m height):**

| Component | Function | Cost |
|---|---|---|
| **AAU (Active Antenna Unit)** | 64T64R Massive MIMO array. Generates SSB beams. **This is our free sensor.** Phase correction log is a mandatory byproduct of beamforming. | $8K–20K |
| **GPS antenna** | PTP timing sync. Keeps telemetry and wind data on the same clock. | $200–800 |
| **Microwave dish** (optional) | Backhaul for sites without fiber. | $2K–10K |

**Ground-level equipment (equipment shelter):**

| Component | Function | Cost |
|---|---|---|
| **BBU (Baseband Unit)** | Digital signal processing. **This is our data source.** Logs every phase correction the AAU applies. Exposes via standard SNMP OID. | $5K–15K |
| **Switch / Router** | Aggregates traffic, connects backhaul. | $1K–5K |
| **Rectifier + Batteries** | -48V DC power + 4-8h backup. Keeps BBU logging during outages. | $3K–11K |
| **HVAC** | Shelter cooling. | $1K–4K |

**Passive infrastructure (the tower itself):**

| Component | Cost |
|---|---|
| Tower structure (monopole, lattice, or guyed, 30-100m) | $20K–100K |
| Concrete foundation + rebar | $10K–30K |
| Fence, gate, access road | $10K–55K |
| AC mains + transformer | $3K–15K |
| Earthing / lightning protection | $1K–5K |

**What matters to the SSB Observer:**

| Hardware | Our Interest |
|---|---|
| **AAU ($8K–20K)** | Free "sensor" — SSB phase correction is a mandatory byproduct |
| **BBU ($5K–15K)** | Data source — logs every correction, exposes via SNMP OID |
| **GPS antenna ($200–800)** | PTP timing — keeps telemetry and wind data synchronized |
| **Fiber backhaul** | Carries telemetry to OSS where we access it |
| **Battery backup** | Keeps BBU running during power cuts — data keeps flowing |
| **Everything else ($70K–240K)** | Not relevant — we don't touch, modify, or need any of it |

**$13K–35K of installed, powered, maintained equipment per site already does exactly what we need.** The operator has already sunk that CAPEX. Every BBU already logs every phase correction. We just read a log.

### How the Data Pipeline Works (Teaser)

The entire monitoring chain uses infrastructure the operator already runs — nothing new to install, configure, or maintain.

```
┌─────────────────────────────────────────────────────────────┐
│  TOWER — already happening, every 10-100ms                  │
│                                                             │
│  1. AAU beamforms SSB signal using 64-element array         │
│  2. Phase shifters adjust each element individually         │
│  3. BBU records phase correction angle per beam             │
│  4. BBU exposes this as a standard PM (Performance          │
│     Measurement) counter                                    │
│                                                             │
│  Vendor counter examples (actual OSS metric names):         │
│    Nokia:  "BeamPhaseOffset" in gNB PM XML feed             │
│    Ericsson: "pmRadioPhsClb" in ENM performance export      │
│    Huawei:  "gNBDUBeamPhsOffset" in iMaster MAE             │
│                                                             │
│  Granularity: 0.01-0.1° per sample                          │
│  Frequency:   Every 10-100ms (100-1,000 samples/second)     │
└──────────────────────┬──────────────────────────────────────┘
                       │ SNMP / OSS API / syslog
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  OSS (Operations Support System) — already running          │
│                                                             │
│  • NetAct (Nokia) / ENM (Ericsson) / iMaster MAE (Huawei)  │
│  • Aggregates PM counters from all towers in the network    │
│  • Exports as CSV, XML, or streaming API                    │
│  • Already polling this data for RF KPIs                    │
│                                                             │
│  We add ONE parsing step:                                   │
│    Extract "BeamPhaseOffset" column → feed to observer      │
└──────────────────────┬──────────────────────────────────────┘
                       │ CSV / API
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  SSB OBSERVER — the only new component                      │
│                                                             │
│  Input:  2 columns (phase correction + wind speed)          │
│  Output: 15-metric health vector, alert level               │
│  Runs on: Standard server, Raspberry Pi, or cloud VM        │
│  Cost:   $0 in additional hardware or licensing             │
└─────────────────────────────────────────────────────────────┘
```

**The only integration work required from the operator:** grant read-access to one PM counter they already collect. That's a configuration change, not a hardware deployment.

For operators without OSS export capability, the observer can ingest raw SNMP walk output directly from the BBU — no intermediate system required.

---

### Competitive Moat

1. **Zero hardware cost.** Competitors sell sensors. We use existing data — BBU phase corrections are already logged by every 5G base station as a standard RF beamforming metric. Wind data comes from tower anemometers (already installed) or free weather APIs. No sensors to buy, install, maintain, or power. Unbeatable on cost.
2. **Zero infrastructure change.** The data pipeline uses existing OSS/SNMP interfaces. BBU phase correction OIDs are standard across Nokia, Ericsson, and Huawei equipment. Operators already poll this data for RF performance — we extract structural information from the same stream.
3. **Data asset defensibility.** Per-tower calibration takes months. Once calibrated for a network, switching costs are high.
4. **Bitcoin-timestamped prior art.** Core method is publicly timestamped on blockchain. No competitor can patent-block us.
5. **Multi-metric detection.** 15 health indicators from one data stream. Competitors offer 1-3 metrics.
6. **First-mover advantage.** Using SSB phase corrections as a structural sensor is a novel technique.

---

### Business Model

| Tier | Price | What |
|---|---|---|
| Monitoring | $20-50/tower/month | Real-time dashboard, 15 metrics, alerts |
| Premium | $100-200/tower/month | Predictive ML, multi-tower correlation, API access |
| Enterprise | Custom | White-label, on-premise deployment, dedicated support |

**Margins:** >95% gross. Software-only. Zero hardware procurement.

---

### Traction & Timeline

| Milestone | Status |
|---|---|
| Working prototype with 15 metrics | ✅ Complete |
| Interactive demo dashboard | ✅ Complete |
| Technical whitepaper (public) | ✅ Published |
| Bitcoin-timestamped prior art | ✅ On-chain |
| Real tower data validation | ⚠️ Seeking tower operator partner |
| First paying customer | Target: Q3 2026 |
| SaaS product launch | Target: Q1 2027 |

---

### Team

**Washington Imae** — 17, self-taught developer, Kenya. Built the entire system solo over 8 weekends. Published whitepaper with on-chain prior art. Previously built: Bit Protocol (Bitcoin IP proof-of-existence), SACCO System (fintech automation), SolDegarde (solar panel optimization).

---

### Ask

**Seeking:** Tower operator partner for field validation. Access to anonymized BBU phase correction logs with known maintenance events. 3-6 month pilot.

**Contact:** washingtoneimae@gmail.com
**Whitepaper:** github.com/washingtoneimae-dot/5g-ssb-whitepaper
**Demo:** github.com/washingtoneimae-dot/5g-ssb-demo
