---
doc_id: SNF-REQ-001
title: SnapFrame requirements
project: SnapFrame
doc_type: Requirements
version: "0.5"
status: Draft
date: '2026-09-26'
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
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Apply SNF-DDR-001 (R10 redefined as the frame kit; 1 in rafters); status from SNF-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish
---

# SnapFrame requirements

These are first-pass requirements for the concept. Targets are proposals for review, not user-validated needs, and will be revised after co-design sessions. The status column comes from the TRL 3 calculation note SNF-CAL-001 v0.3, for the size M frame with 1 in EMT rafters (SNF-DDR-001 D2) and ridge tubes (SNF-DDR-002 D8), 3/4 in EMT posts and eave tubes, and one eave node variant (SNF-DDR-002 D9). Five requirements are **not met**: R5 (packages), R6 (wind), R7 (skin), R11 (carried mass, newly failed by the heavier ridge tubes) and R13 (fire). Two are at risk: R8 (anchors) and R9 (nodes). R12 (part count) is met, and R10 (cost) is met since Amish approved a $445 budget on 2026-09-26.

| ID | Requirement | Target | Status (SNF-CAL-001) | Verification (TRL 3 or later) |
| --- | --- | --- | --- | --- |
| R1 | Give enough covered living space | Size M: 16 m² floor or more, which is 3.5 m² per person for four people (Sphere minimum) | Met: 4.0 x 4.0 m = 16.0 m² | Geometry |
| R2 | Give standing headroom | 2.0 m or more over at least 60 % of the floor | Met: 73 % of the floor, measured to the rafter underside | Geometry |
| R3 | Cover several sizes from one design | At least three sizes (S about 9 m², M 16 m², L about 24 m²) generated from one parametric node model; M and L share every tube length | Met: `cad/src/model.py` generates and exports the S, M and L node sets | Parametric model |
| R4 | Go up without tools | Two adults with no tools and no prior training, using a picture guide, erect frame and skin of size M in 60 min or less | Not verifiable at TRL 3: estimate about 46 min | Time study in a later user trial (TRL 4 or later) |
| R5 | Ship flat | No member longer than 2.1 m; all members straight; kit in two packages, each 25 kg (55 lb) or less and 0.10 m³ or less | **Not met:** longest member 2.064 m, but the tube bundle weighs about 28.6 kg; bag 22.5 kg with tarpaulins. Options are awaiting Amish | Massing model, then weighing |
| R6 | Resist wind with the skin on | Every member stays elastic with a safety factor of 1.5 or more on yield in gusts of 20 m/s (72 km/h, 45 mph) | **Not met:** rating about 19.7 m/s (71 km/h, 44 mph) with 1 in ridge tubes (SNF-DDR-002 D8); 3/4 in posts reach 1.46 at 20 m/s; 1 in rafters 1.66 and 1 in ridge tubes 2.22. Posts to be decided after a frame analysis | Wind load calculation (CAL), then frame analysis |
| R7 | Fit standard relief tarpaulins | Two 4 x 6 m tarpaulins (48 m²) close the roof, both side walls and both gables | **Not met:** full enclosure needs about 51.4 m²; two tarpaulins close the roof, both side walls and one gable. How to treat the open gable is proposed, awaiting Amish | Cutting and folding plan |
| R8 | Anchor without a hammer | Every foot and guy anchored by hand; each anchor holds 1.0 kN uplift in firm soil | **At risk:** estimated demand up to 1.28 kN at a rear corner foot before cable pretension; holding capacity not verifiable at TRL 3 | Anchor pull-out data for the chosen anchor and soils |
| R9 | Keep nodes strong in sun and cold | Nodes carry the socket forces from R6 with a factor of 2 after two years outdoors, from -10 to 70 °C surface temperature | **At risk:** hitch pin bearing on the socket about 32 MPa with the factor of 2; polymer not chosen | Material data, then node load tests (TRL 4) |
| R10 | Stay within the concept budget | Size M frame kit $445 or less in prototype quantities, excluding tarpaulins, which come from agency stock and are costed separately (SNF-DDR-001 D1; budget approved by Amish, 2026-09-26, SNF-DDR-002) | Met: frame kit about $443 ($1.70 under); tarpaulins about $50 extra | Priced BOM |
| R11 | Be carried by two people | Complete size M kit, including tarpaulins, 50 kg (110 lb) or less | **Not met:** frame kit about 42.0 kg; 51.1 kg with tarpaulins (1.1 kg over, from the 1 in ridge tubes) | Massing model, then weighing |
| R12 | Be repairable in the field | Any member or node replaced by hand in 5 min or less; four tube types and three node types only | Met: four tube types; three node types in four printed variants, none handed (one eave node with a blank capped socket at the corners, SNF-DDR-002 D9). Replacement time not verifiable at TRL 3 | Design review |
| R13 | Limit fire spread | Skin meets a recognized flame spread test for tents (for example CPAI-84) or the kit ships with a fire-retardant tarpaulin option | **Not met** with standard polyethylene relief tarpaulins, which are usually not flame retardant | Material data for the chosen tarpaulin |

## Assumptions

- Reference size M (SNF-DDR-001 D6): 4.0 x 4.0 m floor, two 2.0 m bays, eave 1.8 m, ridge 2.6 m (roof pitch 21.8°), three gable frames.
- Tube (SNF-DDR-001 D2, SNF-DDR-002 D8): 1 in EMT rafters and ridge tubes (OD 29.54 mm, wall 1.448 mm, 1.003 kg/m) and 3/4 in EMT posts and eave tubes (OD 23.42 mm, wall 1.245 mm, 0.681 kg/m), ANSI C80.3 nominal dimensions. Yield strength assumed 275 MPa, to be confirmed from supplier data.
- Wind: q = ½ρv² with ρ = 1.225 kg/m³; windward wall +0.8, leeward wall -0.5, roof suction -0.7 (first-order values in the style of ASCE/SEI 7, not a code check). Each tarpaulin panel shares its load between its four edge members by 45° tributary lines. See SNF-CAL-001 for the full list.
- Members are treated as simply supported between node centers; node fixity is ignored, which is conservative for bending.
- Snow and cyclone rating are out of scope for the first release (SNF-DDR-001 D7).
- Budget: $445 is the `budget_usd` in `project.yaml` (raised from $400 when Amish approved the budget on 2026-09-26), applied to one size M frame kit including anchors, cables and bags, and excluding tarpaulins (SNF-DDR-001 D1).
