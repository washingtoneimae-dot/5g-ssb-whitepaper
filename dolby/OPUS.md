# Dolby's Opus Patent Enforcement

## Background

Opus is an audio codec standardized by the IETF in 2012 (RFC 6716). It was
**explicitly designed to be royalty-free**, developed by Skype (now Microsoft),
Mozilla, and the Xiph.Org Foundation. These developers committed to licensing
their relevant patents royalty-free.

**Dolby and Fraunhofer were not part of the Opus standardization process.**

Despite this, in 2023 they launched the **Vectis IP Opus patent pool**,
demanding **€0.15/unit** ($0.16) for hardware devices implementing Opus,
with an annual cap of €15M.

## The Pool

| Detail | Value |
|--------|-------|
| Pool operator | Vectis IP (UK) |
| Participants | Dolby, Fraunhofer IIS |
| Patents declared | 300+ |
| Royalty rate | €0.15/unit (€0.10 early adopter) |
| Annual cap | €15M (€10M early adopter) |
| Scope | Hardware devices only (phones, tablets, PCs, TVs, speakers, consoles) |
| Excluded | Open source software, apps, content |

## Enforcement

As of 2026, Dolby has won a **four-country Opus injunction** via the UPC
(Dusseldorf Local Division) — the UPC's third FRAND ruling. Targets include
hardware manufacturers.

## Why This Is Controversial

1. **Dolby wasn't at the standard body** — They didn't contribute to Opus.
   The standard was set by Skype/Microsoft, Mozilla, and Xiph.

2. **Royalty-free promise subverted** — The IETF process required participants
   to disclose patents and commit to royalty-free licensing. Dolby wasn't a
   participant and made no such commitment.

3. **They sell products using Opus** — Dolby products implement Opus, which
   means they rely on the royalty-free licenses from the original developers.
   Some commentators argue this creates estoppel.

4. **Hardware-only targeting** — The pool explicitly excludes software to
   avoid backlash from the open-source community while still extracting rent
   from hardware vendors.

## Weaknesses

- **Prior art search:** Many of these patents likely cover general audio
  coding techniques that predate Opus (2012). Old patents on CELP, SILK,
  and CELT (the building blocks of Opus) may read on the standard but be
  obvious or anticipated.
- **Estoppel:** If Dolby's products use Opus under the original royalty-free
  license, they may be estopped from asserting patents against others.
- **FRAND compliance:** For a standard that was explicitly royalty-free, what
  constitutes FRAND? The argument that €0.15/unit is FRAND is weak when the
  standard was designed to cost $0.

## Next Steps

1. Get the list of 300+ Opus-declared patents from Vectis
2. Identify the earliest priority dates and compare to Opus RFC 6716 (2012)
3. Check for prior art on SILK, CELT, and CELP coding techniques
4. Search for patents that predate Opus but read on it — these are the
   most vulnerable to obviousness challenges
5. Check if Dolby has made inconsistent statements about Opus licensing
