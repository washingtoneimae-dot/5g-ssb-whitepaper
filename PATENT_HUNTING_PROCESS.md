# Patent Hunting: Systematic Process

A repeatable workflow for finding patents that big companies use to block
smaller competition, analyzing their validity, and publishing design-arounds.

---

## Phase 1: Target Selection

### 1A. Identify Emerging Technology Domains

Big companies file blocking patents before a technology becomes mainstream.
Look where R&D spending is growing but products aren't yet commoditized.

**Signals:**
- NSF/DOG/EU grant awards in specific topics
- Startup activity (Crunchbase, Y Combinator, TechCrunch)
- Standards body discussions (ITU, IEEE, IETF, 3GPP working groups)
- Conference proceedings (OFC, ECOC, CLEO for optics)
- Big company R&D blog posts / whitepapers
- arXiv preprints from corporate labs

**Our domain (fiber optics) examples:**
- Hollow-core fiber deployment infrastructure
- Space-division multiplexing ( multicore fiber, few-mode fiber)
- Silicon photonics packaging
- Coherent optics in access networks
- AI/machine learning for optical network optimization

### 1B. Find the Blocking Patents

**Search queries (USPTO / Google Patents):**

Basic:
```
assignee:"Microsoft" AND "hollow core" AND "mode field"
assignee:"Google" AND "optical fiber" AND "connector"
assignee:"Corning" AND "GRIN" AND "mode"
```

Broad:
```
"GRIN fiber" AND "mode" AND ("converter" OR "adapter" OR "coupler")
"hollow core" AND "connector" AND ("mode field" OR "mode matching")
"mode field adapter" AND "fiber"
```

By known inventors (track individuals from big company R&D):
```
inventor:"Poletti" AND "hollow core"
inventor:"Slavik" AND "GRIN"
```

**Tools:**
| Tool | Use |
|---|---|
| Google Patents | Best for search, claim trees, family trees |
| USPTO Public PAIR | Prosecution history (what examiner saw) |
| USPTO Patent Center | Filed/granted status |
| PatentsReview (patents-review.com) | Clean claim summaries |
| Espacenet (European Patent Office) | Global family search |
| JustPatents (justpatents.com) | AI-assisted claim charts |

### 1C. Prioritize

Score each target patent on:

| Factor | Weight | Score (1-5) |
|---|---|---|
| Would this block a small player from entering the market? | High | |
| Is the claim broad enough to cover real products? | High | |
| Does prior art likely exist (old tech, well-known principles)? | High | |
| Is the assignee likely to enforce it? | Medium | |
| Would a design-around be cheap to implement? | Medium | |

**Priority tiers:**
- **Tier 1** (score 20-25): Full analysis — prior art search, claim chart,
  design-around, publication
- **Tier 2** (score 15-19): Quick analysis — surface prior art, note strategy
- **Tier 3** (score <15): Archive — low impact or hard to work around

---

## Phase 2: Claim Analysis

### 2A. Extract the Independent Claims

Independent claims are the broadest — if they fall, the whole patent falls.
Focus on claim 1 and any other independent claims.

**Template:**
```
Claim 1:
Limitation A: [element + function]
Limitation B: [element + function]
Limitation C: [element + function]
...
```

### 2B. Identify Key Limiting Elements

What specific things does the claim REQUIRE?
- A specific material? (silica, polymer, GRIN, etc.)
- A specific geometry? (length, diameter, pitch, angle)
- A specific connection method? (spliced, joined, coupled, connectorized)
- A specific operating condition? (wavelength, power, bandwidth)
- A specific structure? (core, cladding, capillary, void)

**These are your escape hatches.** Every claim element you can avoid is a
non-infringement path.

### 2C. Check the Prosecution History

The patent file wrapper may contain:
- **Admitted prior art** — the patentee admitted certain things were known
- **Claim amendments** — narrowed claims to get allowance
- **Arguments made to the examiner** — creates prosecution estoppel
  (they can't argue a broad interpretation later)

**Where to find it:**
- USPTO Patent Center → "Image File Wrapper" tab
- Google Patents → "Discussions" tab
- Look for "Office Action" documents — the examiner's rejections and the
  applicant's responses

---

## Phase 3: Prior Art Search

### 3A. Search by Time Period

For any granted patent, search for prior art BEFORE its earliest priority date.

**Layers of prior art (by age/strength):**
1. **Patents in same classification** (USPC/CPC) — 5-20 years before
2. **Academic papers** — look for university research, conference proceedings
3. **Product documentation** — old datasheets, application notes, standards
4. **Textbooks** — well-known principles can't be patented
5. **Older patents from different domains** — analogous art if the
   application is obvious

### 3B. Search Queries

**For GRIN fiber / mode converter type patents:**
```
"GRIN fiber" AND "mode" AND ("convert" OR "adapt" OR "coupl")
"graded index" AND "mode field" AND ("fiber" OR "waveguide")
"multimode interference" AND "mode field" AND ("adapt" OR "convert")
"self-imaging" AND "fiber" AND "mode"
```

**By classification (USPTO search):**
```
CPC/G02B6/14  (mode converters)
CPC/G02B6/255  (splicing light guides)
CPC/G02B6/32  (lens systems in light guides)
CPC/G02B6/02328  (hollow core fibers)
```

### 3C. Build the Timeline

Map every prior art reference on a timeline before the patent's priority date.
Include the specific claim elements each reference teaches.

**Killer find:** A single prior art reference that teaches EVERY limitation
of the independent claim = anticipation (§ 102 — patent invalid).

**Good find:** Multiple references that together teach every limitation =
obviousness (§ 103 — patent likely invalid).

### 3D. Check What the Examiner Missed

The examiner had limited time and a limited search budget. Common misses:

| Missed Type | Why | Our Advantage |
|---|---|---|
| Non-patent literature | Examiners focus on patent databases | We search academic papers, theses, conference proceedings |
| Foreign patents | Examiner may not search JP, CN, KR databases | We search globally |
| Old patents | Examiner searches last 10-20 years | We search back 50+ years |
| Different classification | Patent may be classified differently | We search by concept, not just class |

---

## Phase 4: Design-Around Development

### 4A. Identify Workarounds for Each Limitation

For each limitation in the independent claim, list ways to avoid it:

| Limitation | Avoid by |
|---|---|
| "joined to" | Use separable interface (gel, air gap, connector) |
| "waveguiding core" | Use bulk optic (GRIN rod lens, ball lens) |
| "GRIN fiber" | Use step-index MMF, TEC fiber, tapered fiber |
| "hollow core fiber" | Target solid-core large-mode-area fiber instead |
| "fusion spliced" | Use mechanical splice, adhesive, gel |
| "single mode" | Design for few-mode or multimode instead |
| "length L" | Use a different length outside claim range |
| "silica" | Use polymer, chalcogenide, or other materials |

### 4B. Assess Trade-offs

For each workaround, estimate:

| Factor | How |
|---|---|
| Performance penalty | Loss in dB, bandwidth reduction, etc. |
| Cost impact | BOM change, manufacturing complexity |
| Implementation difficulty | Time + skill required |
| Legal certainty | How sure are we it avoids the claim? |

### 4C. Validate with Physics (When Relevant)

If the patent is in a technical domain you understand:
- Build a quick simulation (Python, MATLAB, COMSOL)
- Do back-of-envelope calculations
- Check if the workaround actually works physically

---

## Phase 5: Publication

### 5A. What to Publish

| Document | Contents |
|---|---|
| Claim analysis | Patent number, independent claims, key limitations |
| Prior art timeline | All references found, with dates and relevance |
| Invalidity analysis | Which claims are anticipated/obvious, with rationale |
| Design-around strategies | Specific workarounds with trade-offs |
| Open-source implementation | Code, CAD files, test results where applicable |

### 5B. Where to Publish

- GitHub repo (dedicated or organized by domain)
- Each patent gets its own directory or markdown file
- Include all referenced prior art (links, DOIs, PDFs if not copyrighted)

### 5C. License

Use a public license that maximizes freedom:
- **Documentation:** CC-BY-4.0
- **Code:** MIT or Apache 2.0
- **Hardware designs:** CERN-OHL-S or similar

---

## Repeatable Toolkit

### Essential Bookmarks

```
Google Patents:     https://patents.google.com
USPTO Patent Center: https://patentcenter.uspto.gov
USPTO PAIR:         https://portal.uspto.gov/pair
Espacenet:          https://worldwide.espacenet.com
JustPatents:        https://www.justpatents.com
Google Scholar:     https://scholar.google.com
arXiv:             https://arxiv.org
IEEE Xplore:       https://ieeexplore.ieee.org
OSA/Optica:        https://opg.optica.org
```

### Search Templates

**Find all patents by an assignee in a specific CPC class:**
```
assignee:"Microsoft" AND CPC/G02B6/14
```

**Find all patents mentioning a concept before a date:**
```
"hollow core fiber" AND "connector" AND priorityDate:2000-01-01 TO 2018-12-31
```

**Find non-patent literature (Google Scholar):**
```
"graded index" "mode field" "hollow core"
```

---

## Example: The Workflow Applied (Our Case)

| Phase | What We Did |
|---|---|
| 1. Target | Found US12517303B2 (Microsoft + Lumenisity) — blocks SMF↔HCF adapters |
| 2. Claim analysis | Claim 1 requires: SMF, HCF, adapter with "shape that changes mode field," "joined to" both ends |
| 3. Prior art | Found Reed 2002 (16 years older), Mafi 2011 (7 years older) — both teach identical GRIN mode converters |
| 4. Design-around | Gel coupling avoids "joined to"; GRIN rod lens avoids "waveguiding core" |
| 5. Publication | All pushed to GitHub with MIT license |

---

## Suggested Pipeline

| Frequency | Task |
|---|---|
| Weekly | Scan new patents from big assignees in target domains |
| Monthly | Deep-dive on one high-priority patent |
| Quarterly | Publish a batch of analyses |
| Per trigger | If a patent is asserted against a small player, rapid response within 2 weeks |

**Next domains to explore:**
- Hollow core fiber connectors (Corning, OFS, Prysmian)
- Silicon photonics edge couplers (Intel, Cisco, IBM)
- Multimode fiber transmission systems
- AI/ML for optical network monitoring
- Quantum key distribution fiber infrastructure
