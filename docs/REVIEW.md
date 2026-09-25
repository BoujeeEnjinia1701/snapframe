# Review note: SnapFrame

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (SNF-PRB-001 v0.2): problem, users (displaced households, agency shelter teams, local fabricators, transitional shelter, public buildings), constraints, out of scope, prior work with sources, open questions; co-design checklist added in the portfolio's standard form (the scaffold had none).
- `docs/03-requirements.md` (SNF-REQ-001 v0.2): 13 measurable requirements (R1 to R13) with targets, estimated status and assumptions.
- `docs/02-concept.md` (SNF-PRC-001 v0.2): how it works, numbered components, node concept, size family (S, M, L), first-order numbers (geometry, mass, cost, wind, anchors, snow), design choices, safety, open questions.
- `cad/src/concept_media.py`: massing model of size M (18 EMT members, 15 nodes, 10 brace cables, 8 screw anchors, 2 guy lines, tarpaulin skin on the rear bay), each part carrying its BOM number. Hero uses a ground patch and a 1.75 m person as context parts so the below-ground anchors do not shift the figure's floor.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `exploded.png` with callouts 1 to 10, `model.glb` and `viewer.html`. Temporary `_views` folders deleted.
- `bom/bom.csv`: 13 lines with indicative prices, numbered to match the exploded view; `bom/bom-notes.md` updated with totals.
- `README.md`: hero image and links line before "## Problem"; problem, concept, key components and safety brought in line with the concept.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Floor, size M | 4.0 x 4.0 m, 16 m² (four people at 3.5 m²) | R1 met |
| Headroom 2.0 m or more | 75 % of floor | R2 met |
| Members, nodes | 18 tubes (4 types), 15 nodes (3 types) | R12 met |
| Longest member, packages | 2.06 m; tube bundle about 24 kg, bag about 21 kg | R5 met |
| Kit mass | about 45 kg | R11 met |
| Erection time, two adults | about 40 min | R4 unverified |
| Rafter safety factor at 20 m/s gusts, 3/4 in EMT | about 1.26 (218 MPa against assumed 275 MPa yield) | **R6 not met** |
| Wind rating with 3/4 in rafters | about 18 m/s (65 km/h, 41 mph) | |
| Rafter safety factor at 20 m/s, 1 in EMT | about 2.4 | Would meet R6 |
| Skin area for full enclosure | about 51 m² against 48 m² from two tarpaulins | **R7 partly met** |
| Parts cost, complete kit | about $437 | **R10 not met, 9 % over** |
| Frame kit without tarpaulins | about $387 | Would meet R10 |
| Tube offcut | 39 % of 18 sticks bought | |
| Anchor uplift | up to about 0.6 kN per foot anchor, before pretension | R8 unverified (1.0 kN target) |

Requirements not met or at risk:

- **R6 (wind) not met:** 3/4 in rafters reach a factor of about 1.26 at 20 m/s; rating about 18 m/s.
- **R10 (cost) not met:** about $437 against $400.
- **R13 (fire) not met:** standard polyethylene relief tarpaulins are usually not flame retardant.
- **R7 (skin) partly met:** two tarpaulins close the roof, both side walls and one gable only.
- **R3 (sizes) partly met:** only size M is modeled; S and L are defined by parameters.
- **R4, R8, R9 unverified:** erection time, anchor holding and node material need data or trials.

### Proposed, awaiting Amish

1. **Budget (R10).** Options: (a) define the $400 as the frame kit and treat tarpaulins as agency stock (about $387, meets); (b) cut cost with bulk EMT or cheaper filament; (c) raise `budget_usd` to about $450. Recommendation: (a), reporting tarpaulin cost separately. `project.yaml` budget is unchanged.
2. **Rafter tube size (R6).** Options: 3/4 in everywhere with an 18 m/s rating; 1 in EMT rafters (about $30 more per kit, second socket bore); four frames at 1.33 m spacing. Recommendation: 1 in rafters.
3. **Node material and process.** Printed polymer first, cast aluminum from printed patterns later. Recommendation: print for the prototype, design for casting.
4. **Joint locking.** Spring buttons everywhere plus hitch pins at the 12 tension joints. Recommendation as stated.
5. **Frame form.** Gable with cable bracing, rather than a dome, barrel vault or rigid nodes. Recommendation: gable.
6. **Tube offcuts.** Accept 39 % offcut, shorten posts to 1.50 m (eave 1.65 m), or use 6 m metric stock. Recommendation: decide once the first region's tube source is known.
7. **Reference size and size family** (S 9 m², M 16 m², L 24 m²), with M as reference.
8. **Out of scope:** snow and cyclone rating in the first release.
9. **First partner and region** for co-design.

No change was made to `pitch` or `problem` in `project.yaml`; the numbers found do not contradict them.

### Safety concerns

- Frame collapse in wind above about 18 m/s, or under snow or ponded water; the frame is an emergency shelter, not a storm refuge.
- Fire: polyethylene tarpaulins burn and drip; cooking and open flames must stay outside.
- Pinch points while dropping tubes into sockets, sharp cut tube ends, trip hazards from guy lines, and buried services when turning in anchors.
- A conductive steel frame near mains cables, and no lightning protection.

### Problems and notes

- **Sources not re-verified this session.** Web search had reached its session limit and page fetches were blocked, so the citations in SNF-PRB-001 (IFRC, UNHCR, Sphere, Better Shelter, Desert Domes, ASCE) and the EMT dimensions and prices come from prior knowledge. Several links point to an organization's home page rather than the exact document. Check each figure and deep link before release.
- No cutaway: at shelter scale the section shows nothing that the hero and exploded views do not. The node interior matters, but belongs in a TRL 3 node drawing.
- No flow diagram: the concept does not move energy or material. A wind load path diagram could be added as a suggestion at TRL 3.
- The exploded view leaves out the skin (item 11) because it hid the frame; it is rendered with a kit helper called after `render_all`. Items 12 and 13 are not modeled.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).

### Recommended next step

Review this note and the media, then decide items 1 and 2. If approved, run `/advance-trl3` to verify EMT properties and sources, do the wind and anchor calculation note, model the parametric nodes for S, M and L with STEP export, and produce the drawing sheet.

## Session 2026-09-25: TRL 3

Amish approved the TRL 2 review on 2026-09-25 ("proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them."). This session advanced SnapFrame to TRL 3 and stopped there.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (SNF-DDR-001 v0.1): decisions D1 to D7 recorded as "Decided by Amish, 2026-09-25: go with recommendation"; items O1 to O3 left open.
- `docs/04-calcs/01-sizing.md` (SNF-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: geometry, EMT sections, wind with 45° tributary load share, bracing, anchors, joints, node mass and cost, mass, packages, cost, skin and erection time, with a results table for R1 to R13. The script imports the CAD model and prints every number the note quotes.
- `cad/src/model.py`: parametric build123d model (sizes S, M, L; tube, node and anchor parameters). Exports `cad/step/snapframe-M-assembly.step`, `cad/step/snapframe-{S,M,L}-nodes.step` and 18 node STLs in `cad/stl/` (six variants per size).
- `cad/src/sheets.py` and `cad/drawings/SNF-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, 1:50, with node details and key dimensions; marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". The concept sheet keeps SNF-DWG-010, so DWG-001 was free.
- `bom/bom.csv` and `bom/bom-notes.md`: all 13 lines priced with supplier types; node prices from the model volumes.
- `cad/src/concept_media.py`: now built from `model.py`; `media/hero.png`, `exploded.png`, `concept-blueprint.*`, `model.glb` and `viewer.html` regenerated and checked. Temporary `_views` folders deleted.
- `docs/01-problem.md`, `docs/02-concept.md`, `docs/03-requirements.md` moved to v0.3; `README.md` and `project.yaml` (trl 3, trl_target 3, evidence list) updated. `pitch`, `problem` and `budget_usd` (400) are unchanged, as the TRL 2 review recommended.

### Requirements (SNF-CAL-001, size M)

4 met, 5 not met, 3 at risk, 1 not verifiable at TRL 3.

| ID | Value | Target | Status |
| --- | --- | --- | --- |
| R5 | Tube bundle 27.4 kg | 25 kg per package | **Not met** |
| R6 | Rating 17.8 m/s; ridge tube 1.18, post 1.46 at 20 m/s | Factor 1.5 at 20 m/s | **Not met** |
| R7 | One gable open (51.4 m² needed, 48 m² available) | Both gables closed | **Not met** (open item O3) |
| R10 | Frame kit $431 | $400, tarpaulins excluded | **Not met** (7.8 % over) |
| R13 | Standard polyethylene tarpaulins | Fire-retardant option | **Not met** |
| R8 | Anchor demand up to 1.28 kN | 1.0 kN per anchor | At risk |
| R9 | Pin bearing on polymer 32 MPa with factor 2 | Factor 2 at 70 °C after two years | At risk |
| R12 | Six printed node variants (handed corners) | Three node types | At risk |
| R4 | About 46 min estimated | 60 min | Not verifiable at TRL 3 |
| R1, R2, R3, R11 | 16.0 m²; 73 % headroom; S, M, L generated; 40.6 kg (49.8 kg with tarpaulins) | | Met |

Key finding: the TRL 2 wind estimate spread half of each tarpaulin panel uniformly over the frames. The 45° tributary rule used here peaks at midspan, so the 3/4 in ridge tubes (not the rafters) now govern, and 1 in rafters alone do not reach 20 m/s. With the open gable facing the wind, the rating falls to about 13.3 m/s. The TRL 2 figures in SNF-PRC-001 v0.2 (post factor 1.70, 18 m/s, $437 complete, 45 kg, 0.6 kN anchors) were replaced with the CAL values.

### Decisions recorded (SNF-DDR-001)

Decided by Amish, 2026-09-25, going with the recommendation: D1 budget covers the frame kit, tarpaulins are agency stock; D2 1 in EMT rafters; D3 print nodes, design for casting; D4 buttons plus hitch pins at 12 tension joints; D5 gable with cable bracing; D6 S, M, L with M as reference; D7 snow and cyclone out of scope.

### Still awaiting Amish

1. **O1 Tube offcuts** (39 %): the recommendation was to decide once the first region's tube source is known, so it stays open.
2. **O2 First co-design partner and region**: no recommendation.
3. **O3 Open gable (R7)**: no recommendation; the open gable also sets the 13.3 m/s open-door wind case.
4. **New, R6 wind.** Options: (a) 1 in ridge tubes as well (+2 sticks, about $10; rating 19.7 m/s, posts then govern); (b) 1 in ridge tubes and posts (about $40 more; 20.3 m/s); (c) keep D2 and rate the kit at 17.5 m/s. Recommendation: (a) now and a frame analysis before deciding on posts. Proposed, awaiting Amish.
5. **New, R10 cost ($431).** Options: bulk EMT pricing, a lighter foot plate (foot nodes are $10.29 each), or raise `budget_usd`. No change was made. Proposed, awaiting Amish.
6. **New, R5 tube bundle (27.4 kg).** Options: two tube bundles (15.2 kg and 12.1 kg, three packages), or relax R5 to 30 kg for a two-person carry. Proposed, awaiting Amish.
7. **New, R12 node variants.** Using the four-socket middle eave node at the corners with one blank socket would remove the handed corner nodes. Proposed, awaiting Amish.
8. **New, node polymer (R9)** and **R8 anchor target**: the 1.0 kN target is below the 1.28 kN calculated demand. Proposed, awaiting Amish.

### Safety concerns

- Frame collapse above about 17.8 m/s, or about 13 m/s with wind into the open gable; not a storm refuge. Snow at 0.5 kPa would yield a 1 in rafter.
- Fire: polyethylene tarpaulins burn and drip (R13 not met).
- Anchor pull-out at the rear corner feet under combined suction and cable forces (R8).
- Printed sockets at 70 °C in sun may lose strength at the hitch pins (R9).
- Pinch points, sharp tube ends, guy line trip hazards, buried services, a conductive frame near mains and no lightning protection, as before.

### Citations

Checked this session with web search and fetch: IFRC and ICRC shelter kit (two 4 x 6 m tarpaulins), UNHCR family tent (16 m² plus vestibules), Better Shelter RHU (17.5 m²; panel and frame life), Zurich 2015 fire concerns (Humanosphere), UNHCR shelter standards citing Sphere (3.5 m² per person), and EMT OD and ID (Engineering ToolBox). Links in SNF-PRB-001 now point to those pages. Not verified: the Domerama strut-flattening page (found by search, not fetched), the ASCE link (home page only), the 275 MPa EMT yield, the 8.0 kN wire rope rating and all prices.

### Problems and notes

- No TRL 4 material exists in the repo (`build-log/` holds only its README and `.gitkeep`).
- The model uses hollow tubes and bored sockets, so `concept_media.py` takes about 8 min to run.
- The exploded view leaves out the skin; items 12 and 13 are not modeled.

### Recommended next step

TRL 4 is on hold by Amish's instruction; do not start it. Next, Amish decides items 4 to 8 above, and SNF-CAL-001 is revised to v0.2 if the tube sizes change. For reference only, TRL 4 would need: a built frame kit and printed nodes, node and anchor load tests with a test report (TST, `environment: lab`), a timed erection with users, and build log entries.
