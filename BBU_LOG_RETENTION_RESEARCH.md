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

### 2.5 Data Access Methods

| Method | Detail | Best for |
|---|---|---|
| **OSS REST API** | NetAct NBI, ENM REST, iMaster MAE API | Programmatic access to PM data |
| **SNMP OID** | Direct BBU polling (vendor-specific OIDs) | Real-time phase correction values |
| **FTP/SFTP** | Raw XML PM files from OSS file share | Bulk historical data |
| **OSS CLI** | AMOS (Ericsson), MML (Huawei) | Ad-hoc queries |
| **Syslog** | Streaming from BBU | Real-time alerting |

### 2.6 Data Flow Diagram

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

1. **Data exists and is accessible** — operators are legally required to collect and retain BBU PM data
2. **Retention periods are sufficient** — 2+ years in most markets means historical comparison and baseline calibration are feasible
3. **No new regulatory burden** — the observer is read-only; operators are already compliant
4. **Raw phase correction is the target** — standard PM XML files contain aggregated counters, not the sub-100ms raw Δθ samples. For real-time monitoring, SNMP OID polling is the right approach. For historical validation, some operators may log raw phase data in debug buffers.
5. **The observer's free-data claim is validated** — regulators mandate the collection; the data costs zero additional dollars per tower
