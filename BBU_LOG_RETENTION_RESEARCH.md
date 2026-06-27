# BBU Log Retention & Format — Research Findings

## Summary

Telecom tower operators are **required** to collect and retain BBU (gNB) performance measurement logs under both 3GPP standards and national telecommunications regulations. The phase correction data the SSB Observer needs already exists in every operator's OSS and is retained for **6 months to 2+ years** depending on jurisdiction.

---

## Part 1: Regulatory Retention

### 1.1 3GPP Standards (Mandatory PM Collection)

| Standard | Scope |
|---|---|
| **TS 28.552** | Defines mandatory gNB performance measurements (PM counters) including beam/phase/RF metrics |
| **TS 32.404** | Defines measurement templates and standardised PM counter naming |
| **TS 32.435** | Defines XML file format for PM data collection and export |

- These PM counters are **collected automatically** by the OSS (NetAct for Nokia, ENM for Ericsson, iMaster MAE for Huawei)
- Operators **cannot disable** these collections without breaking network management and RF optimisation
- The phase correction data used by SSB Observer is a standard PM counter byproduct of beamforming

### 1.2 National Regulatory Retention Periods

| Country / Region | Retention Period | Source / Regulation |
|---|---|---|
| **India** | **2 years** | DoT license conditions — CDRs, UDRs, system logs mandatory |
| **Finland / EU** | **2 years** | Traficom — processing log data minimum 2 years |
| **United States** | **2 years** | 47 CFR §73.1840 — FCC broadcast/telecom logs |
| **China** | **Hot: 7 days in memory, Cold: variable** | YD/T 4688-2024 (NSA), YD/T 4689-2024 (SA) |
| **Australia** | Annual reporting | ACCC Record Keeping Rules |
| **Kenya / East Africa** | **6–24 months** (common practice for RF optimisation) | Not explicitly codified; operators retain PM data for network planning |

---

## Part 2: BBU PM Log Format

### 2.1 Standard Format (3GPP TS 32.435)

PM files use **XML format** defined by 3GPP TS 32.435. The schema (`measCollec.xsd`) defines a hierarchical structure:

```
measCollecFile
 ├── fileHeader
 │    ├── fileFormatVersion
 │    ├── dnPrefix
 │    └── fileSender (localDn, elementType)
 ├── measData (one or more)
 │    ├── managedElement (localDn, userLabel)
 │    ├── measInfo
 │    │    ├── job (jobId)
 │    │    ├── granPeriod (duration, endTime)
 │    │    ├── repPeriod (duration)
 │    │    ├── measType (p="1") — counter name
 │    │    ├── measType (p="2") — counter name
 │    │    ├── ...
 │    │    └── measValue (measObjLdn="...")
 │    │         ├── r p="1" — value
 │    │         ├── r p="2" — value
 │    │         └── ...
 │    └── measInfo ...
 └── fileFooter
      └── measCollec (endTime)
```

**Concrete example** (from 3GPP TS 32.435 Annex A):

```xml
<?xml version='1.0' encoding='UTF-8'?>
<measCollecFile xmlns="http://www.3gpp.org/ftp/specs/archive/32_series/32.435#measCollec">
  <fileHeader fileFormatVersion="32.435 V17.0" vendorName="VendorA" dnPrefix="VendorAPrefix">
    <measCollec beginTime="2021-12-06T15:45:00Z"/>
    <fileSender localDn="localDn" elementType="NF"/>
  </fileHeader>
  <measData>
    <managedElement localDn="ElementA" userLabel="ElementLabel"/>
    <measInfo>
      <job jobId="MetricJob"/>
      <granPeriod duration="PT15M" endTime="2021-12-06T16:00:04Z"/>
      <repPeriod duration="PT15M"/>
      <measType p="1">counter_requests</measType>
      <measType p="2">counter_attempts</measType>
      <measType p="3">counter_total</measType>
      <measValue measObjLdn="element=ElementA,logical-atribute-a=asd123">
        <r p="1">2</r>
        <r p="2">3</r>
        <r p="3">1</r>
      </measValue>
    </measInfo>
  </measData>
  <fileFooter>
    <measCollec endTime="2021-12-06T16:00:04Z"/>
  </fileFooter>
</measCollecFile>
```

### 2.2 Key Fields

| XML Element | Description |
|---|---|
| `measCollecFile` | Root element, namespaced to 3GPP TS 32.435 |
| `fileHeader/fileFormatVersion` | e.g. "32.435 V17.0" |
| `fileHeader/dnPrefix` | Distinguished Name prefix for the network |
| `measData/managedElement` | The managed element (e.g. gNB, NRBTS) |
| `measInfo/job/jobId` | Measurement job identifier |
| `measInfo/granPeriod` | Granularity period (e.g. PT15M = 15 minutes) |
| `measInfo/repPeriod` | Reporting period |
| `measInfo/measType` | Counter name/identifier (with positional attribute `p`) |
| `measValue/measObjLdn` | Local Distinguished Name of the measured object |
| `measValue/r` | Result value (attribute `p` matches `measType/p`) |
| `fileFooter/measCollec/endTime` | Collection end timestamp |

### 2.3 Vendor Counter Naming

#### Nokia (NetAct)

- Managed Objects: `MRBTS` (multi-RAN), `NRBTS` (gNB-level), `NRCEL` (cell-level)
- Counter IDs: `M55xxx` series for 5G NR (e.g. `M55360` for NR UL interference)
- 5G-NR category has ~14,500 counters across massive MIMO, beamforming, mobility, etc.
- Counters accessed via NetAct PM Browser, Reporting Suite, or NBI REST API:
  - `GET /performance/kpis?neDn=...&kpiGroup=...&granularity=PT15M&startTime=...&endTime=...`
- Granularity: 15-minute ROP (Report Output Period), 1-hour, or daily

#### Ericsson (ENM)

- Counter prefix: `pmRadio*`, `pmPdcp*`, `pmPrb*`, `pmFlex*` (flexible/dynamic counters)
- Examples: `pmPdcpVolDlDrb`, `pmRadioUeRepCqiDistr`, `pmPrbUtilDl`
- Flexible counters use dynamic naming: `pmFlexPdcpVolDlDrb_UeCat1To2Spid2`
- Raw PM files accessible via FTP: `/ericsson/pmic1/XML/` or `/ericsson/pmic2/XML/`
- Also accessible via ENM CLI, ENIQ Business Intelligence, DCGM, or AMOS (`pmr`/`pget` commands)
- Granularity: 15-minute ROP

#### Huawei (iMaster MAE)

- Counter prefix: `L.NR.*` pattern (e.g. `L.NB.Thrp.bits.DL.Phy`)
- Beam parameters configured via MOs: `NRDUCellTrpBeam`, `NRDUCellTrpCustBeam`
- Parameters include `CoverageScenario`, `Tilt`, `Azimuth`, `MaxSsbPwrOffset`, `ScenarioBeamAlgoSw`
- Beam count ranges from BEAM_0 to BEAM_7 (8 beams) for TDD 8:2 slot assignment

### 2.4 SSB Beam-Related PM Counters (TS 28.552)

| Section | Counter | Description |
|---|---|---|
| 5.1.1.21 | Intra-NRCell SSB Beam switch | Counts of requested/successful SSB beam switches within a cell |
| 5.1.1.28.1 | Number of UE related the SSB beam Index (mean) | Average UEs per SSB beam index |
| 5.1.1.28.2 | DL data transmission time per SSB | Time spent transmitting DL data per SSB beam |
| 5.1.1.28.3 | Number of UE related to the SSB beam Index (Maximum) | Max UEs per SSB beam index |
| 5.1.1.32.2 | SS-SINR distribution per SSB | Signal quality distribution per SSB beam |

**Note:** While these are the standardised counters, the **raw phase correction values** (Δθ) that the SSB Observer uses are BBU-internal beamforming weights, not aggregated PM counters. They exist in the BBU's internal phase lock loop logs and are exposed via vendor-specific SNMP OIDs or debug interfaces — not the standard PM XML files. The PM counters above are derived/aggregated metrics; the observer needs the raw per-sample values.

### 2.4.1 Precision & Resolution Gap

There are **two tiers of data** with very different resolution:

| Channel | Sample Interval | Resolution | Suitable for Observer? |
|---|---|---|---|
| **OSS PM XML** (standard) | 15 min / 1 hr | Aggregated counts | ❌ Too coarse |
| **BBU internal phase lock loop** | **10–100 ms** | **~0.01–0.02°** | ✅ Full resolution |

**Issue:** The raw sub-100ms Δθ samples are DSP-level beamforming weights internal to the AAU/BBU. They are:
- **Not exposed** in standard 3GPP PM XML exports
- **Not mandated** by regulators (who only require aggregated PM counters)
- **Accessible only** via vendor-specific SNMP OIDs, gNB trace (MDT/MLB per 3GPP TS 37.320), or BBU debug interfaces

**What this means for the SSB Observer:**
- The *capability* exists in hardware — every AAU computes phase corrections at 10-100ms with 0.01° resolution
- The *access* depends on vendor API support, not regulatory mandate
- Standard OSS PM feeds (15-min aggregates) are **insufficient** — the observer must tap into the real-time BBU data path
- A pilot would need the operator to enable the relevant SNMP OID or provide BBU debug trace access, not just standard PM exports

### 2.5 Data Access Methods

| Method | Detail | Best for |
|---|---|---|
| **OSS REST API** | NetAct NBI, ENM REST, iMaster MAE API | Programmatic access to PM data |
| **SNMP OID** | Direct BBU polling (vendor-specific OIDs) | Real-time phase correction values |
| **FTP/SFTP** | Raw XML PM files from OSS file share | Bulk historical data |
| **OSS CLI** | AMOS (Ericsson), MML (Huawei) | Ad-hoc queries |
| **Syslog** | Streaming from BBU | Real-time alerting |

### 2.5.1 Reality Check — Raw Phase Correction Data May Not Be Exposed

**Critical finding from vendor capability research:** There is no public evidence that Nokia AirScale, Ericsson RAN Compute, or Huawei gNBs expose **raw beamforming phase correction values (Δθ)** through any standard interface.

| What the whitepaper assumes | What actually exists |
|---|---|
| BBU logs Δθ at 10-100ms intervals | Internal DSP parameter — computed but never logged to an exportable interface |
| Exposed via vendor SNMP OIDs | No public documentation of OIDs for raw beamforming weights or phase corrections |
| Readable from standard PM logs | PM XML only contains aggregated counters (15-min ROP) like beam switch counts, UE per beam index, SS-SINR distribution |

**What IS actually available from real BBUs:**

1. **UE Measurement Reports (RRC/MAC CE)** — UEs report L1-RSRP (signal strength) per SSB beam index. The gNB gets beam quality, NOT phase correction. This is specified in TS 38.331 and TS 38.321.

2. **PM Counters (TS 28.552)** — Aggregated metrics:
   - `Number of SSB beam switches` (section 5.1.1.21)
   - `Number of UEs per SSB beam index` (section 5.1.1.28)
   - `DL data transmission time per SSB` (section 5.1.1.28.2)
   - `SS-SINR distribution per SSB` (section 5.1.1.32.2)
   - All are **15-minute aggregates**, not continuous samples

3. **gNB Trace / MDT** — 3GPP TS 37.320 defines trace capabilities, but these focus on RRC signaling and UE measurements, not internal DSP beamforming weights.

4. **External test equipment** — Rohde & Schwarz RTP/NRQ6 and Keysight VSE can measure MIMO phase externally via RF signal analysis (see R&S app note GFM343). This requires a signal analyzer connected to the antenna port — defeats the zero-hardware claim.

**Conclusion:** The whitepaper's core data assumption — that the BBU's internal phase correction (Δθ) is accessible at 10-100ms resolution — is **not supported by available vendor documentation**. The data exists inside the AAU's DSP but is not surfaced through any standard export mechanism.

**For the SSB Observer to work, one of these would be needed:**
- Vendor firmware update to expose beamforming weights as a PM counter or OID
- External RF phase measurement equipment per tower (defeats zero-hardware)
- Alternative approach using UE-reported L1-RSRP per beam (available, but measures signal strength, not phase/angle)

### 2.6 Data Flow Diagram (Revised)

```
BBU/AAU (every 10-100ms)
  │ Internal phase lock loop logs Δθ
  │
  ├──► SNMP OID (real-time phase correction values)
  │
  └──► OSS (NetAct / ENM / iMaster MAE)
        │ Collects PM counters including beam metrics
        │ Aggregates into 15-min ROP XML files
        │ Retains per regulatory requirements (6mo-2yr+)
        │ Exports as XML, CSV, or streaming API
        │
        ▼
     SSB Observer
        │ Reads: raw Δθ via SNMP OID (real-time)
        │   OR: phase correction column from OSS export (batch)
        └──► 15-metric health vector H(t)
```

---

## Part 3: Key Implications for SSB Observer

1. **Standard PM data is available but wrong granularity** — operators legally collect 15-min aggregated counters (beam switches, UE counts, SINR). These are **too coarse** for the observer's frequency-domain analysis (natural frequency tracking, damping, vortex shedding).

2. **Raw Δθ may not exist as accessible data** — extensive vendor research found **no evidence** that any BBU vendor exposes raw beamforming phase correction values at 10-100ms resolution through any standard interface (SNMP, PM XML, REST API). The whitepaper's core data assumption is unverified.

3. **UE-reported beam metrics are the closest available signal** — L1-RSRP per SSB beam index is real data that operators already collect. It measures signal strength per beam direction, not phase correction. Whether RSRP-per-beam correlates sufficiently with structural tilt is an open question requiring field validation.

4. **The zero-hardware claim is at risk** — without accessible Δθ data, the observer may require:
   - Vendor firmware changes (not zero-hardware, requires vendor partnership)
   - External RF measurement equipment (defeats the purpose)
   - A different algorithmic approach using existing UE RSRP reports

5. **The pilot's primary goal must change** — instead of "validate the observer against real Δθ data", the first pilot should be: **"determine what data the BBU actually exposes and whether any of it correlates with structural tilt."**
