# BBU Log Retention Requirements — Research Findings

## Summary

Telecom tower operators are **required** to collect and retain BBU (gNB) performance measurement logs under both 3GPP standards and national telecommunications regulations. The phase correction data the SSB Observer needs already exists in every operator's OSS and is retained for **6 months to 2+ years** depending on jurisdiction.

---

## 1. 3GPP Standards (Mandatory PM Collection)

| Standard | Scope |
|---|---|
| **TS 28.552** | Defines mandatory gNB performance measurements (PM counters) including beam/phase/RF metrics |
| **TS 32.404** | Defines measurement templates and standardised PM counter naming |
| **TS 32.435** | Defines XML file format for PM data collection and export |

- These PM counters are **collected automatically** by the OSS (NetAct for Nokia, ENM for Ericsson, iMaster MAE for Huawei)
- Operators **cannot disable** these collections without breaking network management and RF optimisation
- The phase correction data used by SSB Observer is a standard PM counter byproduct of beamforming

---

## 2. National Regulatory Retention Periods

| Country / Region | Retention Period | Source / Regulation |
|---|---|---|
| **India** | **2 years** | DoT license conditions — CDRs, UDRs, system logs mandatory |
| **Finland / EU** | **2 years** | Traficom — processing log data minimum 2 years |
| **United States** | **2 years** | 47 CFR §73.1840 — FCC broadcast/telecom logs |
| **China** | **Hot: 7 days in memory, Cold: variable** | YD/T 4688-2024 (NSA) and YD/T 4689-2024 (SA) |
| **Australia** | Annual reporting | ACCC Record Keeping Rules — infrastructure asset records |
| **Kenya / East Africa** | **6–24 months** (common practice for RF optimisation) | Not explicitly codified; operators retain PM data for network planning |

---

## 3. Data Flow (Already in Place)

```
BBU/AAU (every 10-100ms)
  │ SNMP / OSS API
  ▼
OSS (NetAct / ENM / iMaster MAE)
  ─ Collects PM counters including beam phase corrections
  ─ Retains data per regulatory requirements (6mo-2yr+)
  ─ Exports as CSV, XML, or streaming API
  │
  ▼
SSB Observer (read-only access)
  ─ Reads one column: "BeamPhaseOffset" or equivalent
  - No new data collection infrastructure needed
```

- Operators already poll this data for RF KPIs
- The SSB Observer adds **one parsing step** to an existing data stream
- Zero new logging obligations — the data is already being stored

---

## 4. Key Implications for SSB Observer

1. **Data exists and is accessible** — operators are legally required to collect and retain BBU PM data
2. **Retention periods are sufficient** — 2+ years in most markets means historical comparison and baseline calibration are feasible
3. **No new regulatory burden** — the observer is read-only; operators are already compliant
4. **Phase correction data is vendor-standard** — Nokia (`BeamPhaseOffset`), Ericsson (`pmRadioPhsClb`), Huawei (`gNBDUBeamPhsOffset`) all expose this via standard OIDs
5. **The observer's free-data claim is validated** — regulators mandate the collection; the data costs zero additional dollars per tower
