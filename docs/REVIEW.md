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
