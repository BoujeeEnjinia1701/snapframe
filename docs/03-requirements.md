---
doc_id: SNF-REQ-001
title: SnapFrame requirements
project: SnapFrame
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept estimates
---

# SnapFrame requirements

These are first-pass requirements for the concept. Targets are proposals for review, not user-validated needs, and will be checked by calculation at TRL 3 and revised after co-design sessions. The status column compares each target with the first-order estimates in SNF-PRC-001; every status is an estimate until TRL 3. Three requirements are **not met** by the reference concept: R6 (wind), R10 (cost) and R13 (fire), and R7 (skin coverage) is only partly met.

| ID | Requirement | Target | Status (estimate) | Verification (TRL 3 or later) |
| --- | --- | --- | --- | --- |
| R1 | Give enough covered living space | Size M: 16 m² floor or more, which is 3.5 m² per person for four people (Sphere minimum) | Met: 4.0 x 4.0 m = 16 m² | Geometry |
| R2 | Give standing headroom | 2.0 m or more over at least 60 % of the floor | Met: 2.0 m or more over the central 3.0 m of the 4.0 m span (75 %) | Geometry |
| R3 | Cover several sizes from one design | At least three sizes (S about 9 m², M 16 m², L about 24 m²) generated from one parametric node model; M and L share every tube length | Partly met: M modeled; S and L defined by parameters only | Parametric model generating all three node sets |
| R4 | Go up without tools | Two adults with no tools and no prior training, using a picture guide, erect frame and skin of size M in 60 min or less | Estimate about 40 min; unverified | Time study in a later user trial (TRL 4 or later) |
| R5 | Ship flat | No member longer than 2.1 m; all members straight; kit in two packages, each 25 kg (55 lb) or less and 0.10 m³ or less | Met: longest member 2.06 m; tube bundle about 24 kg and 0.03 m³; bag about 21 kg and 0.08 m³ | Massing model, then weighing |
| R6 | Resist wind with the skin on | Every member stays elastic with a safety factor of 1.5 or more on yield in gusts of 20 m/s (72 km/h, 45 mph) | **Not met:** rafters about 1.26 with 3/4 in EMT; rating about 18 m/s (65 km/h, 41 mph) | Wind load calculation (CAL), then frame analysis |
| R7 | Fit standard relief tarpaulins | Two 4 x 6 m tarpaulins (48 m²) close the roof, both side walls and both gables | **Partly met:** full enclosure needs about 51 m² plus overlaps; two tarpaulins close the roof, both side walls and one gable | Cutting and folding plan |
| R8 | Anchor without a hammer | Every foot and guy anchored by hand; each anchor holds 1.0 kN uplift in firm soil | Unverified: estimated demand up to about 0.6 kN per foot anchor from wind, more with cable pretension | Anchor pull-out data for the chosen anchor and soils |
| R9 | Keep nodes strong in sun and cold | Nodes carry the socket forces from R6 with a factor of 2 after two years outdoors, from -10 to 70 °C surface temperature | Unverified; node material not chosen | Material data, then node load tests (TRL 4) |
| R10 | Stay within the concept budget | Complete size M kit $400 or less in prototype quantities | **Not met:** about $437 (9 % over); frame kit without tarpaulins about $387 | Priced BOM |
| R11 | Be carried by two people | Complete size M kit 50 kg (110 lb) or less | Met: about 45 kg | Massing model, then weighing |
| R12 | Be repairable in the field | Any member or node replaced by hand in 5 min or less; four tube types and three node types only | Met by design | Design review |
| R13 | Limit fire spread | Skin meets a recognized flame spread test for tents (for example CPAI-84) or the kit ships with a fire-retardant tarpaulin option | **Not met** with standard polyethylene relief tarpaulins, which are usually not flame retardant | Material data for the chosen tarpaulin |

## Assumptions

- Reference size M: 4.0 x 4.0 m floor, two 2.0 m bays, eave 1.8 m, ridge 2.6 m (roof pitch about 22°), three gable frames.
- Tube: 3/4 in EMT to ANSI C80.3 nominal dimensions (OD 23.4 mm, wall 1.24 mm), mass about 0.70 kg/m. Yield strength assumed 275 MPa (estimate, to be confirmed from supplier data).
- Wind: dynamic pressure q = ½ρv² with ρ = 1.225 kg/m³; windward wall coefficient +0.8; roof suction coefficient -0.7 (first-order values in the style of ASCE/SEI 7, not a code check). The tarpaulin panel is assumed to pass half its load to the frames and half to the eave and ridge tubes.
- Members are treated as simply supported between node centers; node fixity is ignored, which is conservative for bending.
- Snow is out of scope (SNF-PRB-001).
- Budget: $400 is the `budget_usd` in `project.yaml`, applied here to one complete size M kit including tarpaulins, anchors and bags. Whether tarpaulins belong in the budget is proposed, awaiting Amish.
