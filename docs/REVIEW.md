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
4. **New, R6 wind.** Options: (a) 1 in ridge tubes as well (+2 sticks, about $10; rating 19.7 m/s, posts then govern); (b) 1 in ridge tubes and posts (about $40 more; 20.3 m/s); (c) keep D2 and rate the kit at 17.5 m/s. Recommendation: (a) now and a frame analysis before deciding on posts. Decided by Amish, 2026-09-25: go with recommendation (SNF-DDR-002 D8).
5. **New, R10 cost ($431).** Options: bulk EMT pricing, a lighter foot plate (foot nodes are $10.29 each), or raise `budget_usd`. No change was made. Decided by Amish, 2026-09-26: budget set to $445 (SNF-DDR-002 v0.2).
6. **New, R5 tube bundle (27.4 kg).** Options: two tube bundles (15.2 kg and 12.1 kg, three packages), or relax R5 to 30 kg for a two-person carry. Proposed, awaiting Amish.
7. **New, R12 node variants.** Using the four-socket middle eave node at the corners with one blank socket would remove the handed corner nodes. Decided by Amish, 2026-09-25: go with recommendation (SNF-DDR-002 D9).
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

## Session 2026-09-25: recommendations accepted

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item from the TRL 3 session that carried a recommendation is now "Decided by Amish, 2026-09-25: go with recommendation" and is recorded in `docs/decisions/0002-recommendations-accepted.md` (SNF-DDR-002 v0.1). Items without a recommendation stay "Proposed, awaiting Amish". The trl and trl_target stay at 3.

### Decisions applied and what changed

| # | Decision | Before | After |
| --- | --- | --- | --- |
| D8 (item 4, R6 wind) | Decided by Amish, 2026-09-25: go with recommendation. (a) 1 in EMT ridge tubes now; frame analysis before deciding on posts | 3/4 in ridge tubes; rating 17.8 m/s, ridge tube governs (factor 1.18); open-gable case 13.3 m/s | 1 in ridge tubes; rating 19.7 m/s, 3/4 in post governs (factor 1.46); ridge tube 2.22; open-gable case 14.7 m/s |
| D9 (item 7, R12 node variants) | Decided by Amish, 2026-09-25: go with recommendation. Four-socket eave node at the corners with one blank, capped socket | Six printed variants per size (handed corner eave nodes) | Four printed variants per size, none handed; R12 at risk to met |

Knock-on numbers, size M (SNF-CAL-001 v0.1 to v0.2): frame kit $431.09 to $443.30 (7.8 % to 10.8 % over the $400 budget); frame kit mass 40.6 to 42.0 kg; with tarpaulins 49.8 to 51.1 kg (R11 met to **not met**); tube bundle 27.4 to 28.6 kg; nodes 4.87 kg and $122.09 to 4.97 kg and $124.30. `budget_usd` stays 400 under SNF-DDR-001 D1; `pitch` and `problem` are unchanged because no accepted recommendation touched them.

Files changed: `cad/src/model.py` (1 in ridge tubes, single eave node), `cad/step/` and `cad/stl/` re-exported (the six `eave-corner-L/R` and three `eave-middle` STLs replaced by `snapframe-{S,M,L}-eave.stl`), `cad/src/sheets.py` and SNF-DWG-001 Rev P1 to P2, `docs/04-calcs/sizing.py` and SNF-CAL-001 v0.1 to v0.2, SNF-PRC-001 v0.3 to v0.4, SNF-REQ-001 v0.3 to v0.4, SNF-PRB-001 v0.3 to v0.4 (updated rating; MERO added to prior work), `bom/bom.csv` (items 3, 6, 7, 12) and `bom/bom-notes.md`, `cad/src/concept_media.py` and all of `media/`, `README.md` (numbers, and the new sections Concept rationale, Burning platform, Where it could be used and What sparked the idea), `project.yaml` (DDR-002 added to trl_evidence). All PDFs in `docs/pdf/`, the drawing and the concept media were regenerated so every footer shows designmolecule.com.

### Requirement status (SNF-CAL-001 v0.2, size M)

4 met, 6 not met, 2 at risk, 1 not verifiable at TRL 3 (was 4, 5, 3, 1).

| ID | Value | Target | Status |
| --- | --- | --- | --- |
| R5 | Tube bundle 28.6 kg | 25 kg per package | **Not met** |
| R6 | Rating 19.7 m/s; post 1.46 at 20 m/s | Factor 1.5 at 20 m/s | **Not met** (frame analysis pending) |
| R7 | One gable open (51.4 m² needed, 48 m² available) | Both gables closed | **Not met** |
| R10 | Frame kit $443 | $400, tarpaulins excluded | **Not met** (10.8 % over) |
| R11 | 51.1 kg with tarpaulins | 50 kg | **Not met** (new, from the 1 in ridge tubes) |
| R13 | Standard polyethylene tarpaulins | Fire-retardant option | **Not met** |
| R8 | Anchor demand up to 1.28 kN | 1.0 kN per anchor | At risk |
| R9 | Pin bearing on polymer 32 MPa with factor 2 | Factor 2 at 70 °C after two years | At risk |
| R4 | About 46 min estimated | 60 min | Not verifiable at TRL 3 |
| R1, R2, R3, R12 | 16.0 m²; 73 % headroom; S, M, L generated; four node variants, none handed | | Met |

### Still awaiting Amish

1. **O1 Tube offcuts** (39 %): decide once the first region's tube source is known.
2. **O2 First co-design partner and region**: no recommendation.
3. **O3 Open front gable (R7)**: no recommendation.
4. **O4 R10 cost ($443)**: bulk EMT pricing, a lighter foot plate, or raise `budget_usd`; no recommendation. Decided by Amish, 2026-09-26: budget set to $445 (SNF-DDR-002 v0.2).
5. **O5 R5 package and R11 carried mass**: two tube bundles (16.5 and 12.1 kg) or relax R5 to 30 kg; R11 is now 1.1 kg over and needs a choice too; no recommendation.
6. **O6 Node polymer (R9)** and **O7 R8 anchor target** (1.0 kN against 1.28 kN demand): no recommendation.
7. **O8 1 in posts**: per D8, after the frame analysis (20.3 m/s by member check, about $30 more).

### Cross-repo actions

None. No accepted recommendation for SnapFrame needs another repo to change.

### TRL 4

TRL 4 remains on hold by Amish's instruction. No build, test, purchasing or build-log material was created. The frame analysis that D8 calls for is TRL 3 paper work; it was not run in this session and is the recommended next step.

## Session 2026-09-26: sources strengthened

- **What sparked the idea (README):** the Wikipedia "Space frame" link (and the "first space truss system" claim it carried) was removed. The MERO account now rests on the company's own history page ([mero.de](https://mero.de/en/the-company/)), restated to what that page says (end of the 1930s, industrially prefabricated series elements), plus MERO Raumstruktur's patent [EP0475216B1](https://patents.google.com/patent/EP0475216B1/de) for the tubular rods and near-spherical node pieces.
- **`docs/01-problem.md` (SNF-PRB-001 v0.5):** the same MERO prior-work line now cites the patent for the tube and node description, since the MERO history page does not describe the nodes.
- `INSPIRATIONS.md`: the SnapFrame line now names the patent as a source. Country rows were already cited; no rows replaced. No budget change.

## Session 2026-09-26: budget approved

On 2026-09-26 Amish wrote: "i approve all the budget items." Open item O4 (R10 cost) is decided: budget set to $445 to cover the priced BOM, recorded in SNF-DDR-002 v0.2.

- `project.yaml`: `budget_usd` 400 to 445. The priced frame kit is $443.32 (tarpaulins excluded, SNF-DDR-001 D1), so the figure covers it.
- R10: **not met** (10.8 % over $400) to **met** ($1.70 under $445). Requirement status is now 5 met, 5 not met, 2 at risk and 1 not verifiable.
- `docs/04-calcs/sizing.py` now checks against $445 and was rerun; SNF-CAL-001 v0.3, SNF-REQ-001 v0.5, SNF-PRC-001 v0.5, SNF-PRB-001 v0.6, `README.md` and `bom/bom-notes.md` quote the new figure. The concept blueprint key figure now reads "budget $445", and `media/` was regenerated.
- Still awaiting Amish: O1 tube offcuts, O2 co-design partner, O3 open gable, O5 packages and carried mass, O6 node polymer, O7 anchor target, O8 1 in posts.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26. This session added `cad/src/product_model.py`, an appearance model of the size M frame for photoreal renders, and pointed the README hero image at `media/render-hero.png` with a link to `media/render-exploded.png`. The render files are produced later by the orchestrator.

What `product_model.py` adds:

- `product_parts()`: 144 parts in four groups (shell, internal, accessory, context), each with a colour, material, BOM line and exploded-view offset; `TITLE` and three `RENDER_VIEWS` (hero, exploded, detail).
- Galvanized EMT tubes with colour bands just outside each socket mouth, one colour per tube type (posts, rafters, ridge tubes, eave tubes), as the BOM's "color band at ends".
- The printed nodes from `model.node_variants()` in the kit teal, with fillets at the core-to-socket junctions, the socket mouths and the foot plate edges; grip ribs and a size mark on each foot plate.
- Stainless spring buttons showing in every tube socket hole, hitch pins with pull rings at the 12 tension joints, and ribbed push-in caps on the four blank corner eave sockets (item 12).
- Brace cables with hand cam tensioners and swaged sleeves, a snap hook on the front right corner eave node's cable tab, screw anchors at the feet, and guy lines with slide tensioners and reflective tape.
- Context: a compact soil plinth, one tarpaulin fitted over the rear bay with a hem and eyelets (agency stock, item 11, as in `concept_media.py`), and the shared clay mannequin standing beside the open front gable for scale.
- A "detail" view of one joint: the front right corner eave node and the ends of its post, rafter and eave tube, with buttons, hitch pin, cap and snap hook.

Places where the appearance model differs from `model.py`:

1. **Tube ends at the detail node.** The three tubes that meet the front right corner eave node are drawn as two pieces each, split 300 mm from the node centre, so the detail view can frame the joint alone. The joint between the two pieces is a flush butt that does not show in the renders; tube lengths and positions are unchanged. Proposed, awaiting Amish: keep the split as a render device. Recommendation: keep it; no document quotes it.
2. **Guy lines and guy anchors not in the hero.** They sit in the "accessory" group, so the hero shows the frame on a compact plinth; they appear in the exploded view. Proposed, awaiting Amish: accept the hero without guy lines, or add them and a wider plinth (the frame then fills less of the image). Recommendation: accept, with the hero caption saying guy lines are not shown.
3. **Appearance hardware not modeled in `model.py`.** Colour bands, spring buttons, hitch pins with rings, socket caps, cable tensioners, sleeves and snap hook, guy tensioners and foot plate ribs and marks are appearance additions with indicative sizes; the foot plate size mark and grip ribs are not in the BOM spec. Proposed, awaiting Amish: whether the foot plate ribs and size mark should become part of the node concept. Recommendation: keep them as appearance only until the node polymer (O6) is chosen.
4. **Brace cable at the detail node** starts 48 mm outside the node core rather than at the node centre, so it does not cross the snap hook in close-ups. Proposed, awaiting Amish. Recommendation: accept; the node-to-node cable length in SNF-CAL-001 is unchanged.

This is an appearance model only: no tolerances, no fabrication detail and no change to `model.py`, the BOM or the controlled documents. `trl` stays 3, and TRL 4 remains on hold.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-01: design for construction and illustrated build plan (BLD-001)

Kit 1.7.0 installed (`.kit/`, `.claude/commands/`, `CLAUDE.md`). Amish approved the build plan format on 2026-09-30 and asked for it across all repos, with outstanding decisions kept in a separate register; on 2026-10-01 he set `budget_usd` as a value-engineering target. This session made the SnapFrame design constructable, wrote the illustrated build plan and opened the design decisions register. No hardware was built; `trl` stays 3.

### What was done

- `cad/src/model.py`: constructable model with the bought hardware (snap buttons with their spring envelope, hitch pins, caps, cable bolt sets with rings, snap hooks, anchors turned down onto the plates) and 203 constructability checks (`python cad/src/model.py --check`): all 203 pass. STEP (`cad/step/`) and STL (`cad/stl/`) regenerated.
- `docs/decisions/0003-design-for-construction.md` (SNF-DDR-003 v0.1, Draft): every change, made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.
- `docs/05-build-plan.md` (SNF-BLD-001 v0.1): plain-English build plan, components in build order, 13 assembly steps, first checks, safety stops, tools; no open decisions.
- `docs/06-design-decisions.md` (SNF-DEC-001 v0.1): 10 open decisions, 6 items to confirm when parts are bought, a value-engineering section and the decisions made with Amish's words.
- `cad/src/build_plan_media.py`: overview, nine making sketches `cad/drawings/SNF-DWG-101` to `109`, six joint close-ups, 13 step pictures and a cable make-up picture in `docs/05-build-plan/`.
- `docs/04-calcs/sizing.py` and SNF-CAL-001 v0.4 (cable bolt check, pin shear-out, cable lengths, mass and cost); SNF-REQ-001 v0.6; SNF-PRC-001 v0.6; `bom/bom.csv` (lines 1 to 10 and 12 updated, new line 14) and `bom/bom-notes.md`; SNF-DWG-001 Rev P4 (`cad/src/sheets.py`); concept media regenerated (`cad/src/concept_media.py`).
- `project.yaml`: `design_state: constructable`; DDR-003, the build plan, the register, the overview picture and the picture script added to `trl_evidence`. `budget_usd` unchanged (445). `README.md`: links line, value-engineering target in the header line, and a "Building the prototype" section before "Safety".

### Design changes made for construction (SNF-DDR-003)

1. **C1** Spring button moved from 25 to 40 mm and hitch pin from 50 to 15 mm from the tube end: the button's spring ran through the pin.
2. **C2** A 16 mm finger recess round every button hole and a 1.5 mm chamfer at every socket mouth: the button can be pressed by hand and rides in.
3. **C3** Printed cable and guy tabs replaced by a through-bolted stainless M10 cable bolt with a spacer and a welded 6 mm ring on every eave and ridge node (171 MPa in the shank, factor 2.6).
4. **C4** Lower cable ends clip to the anchor eyes at the feet.
5. **C5** Anchor eyes turned down onto the foot plates (they stood 32 mm clear).
6. **C6** Two anchor slots at 45° in the foot plate, so the gable cable clears the foot node; still one foot node, not handed.
7. **C7** Erection order: frames stand unanchored and slide 65 mm onto the eave and ridge tubes; anchors go in last (a 1,910 mm tube cannot fit between fixed sockets 1,780 mm apart).
8. **C8** Guy lines tie to the end ridge node rings.
9. **C9** One drilling rule: the two button holes of every tube on opposite sides of one marked line.

### Key results and requirements

- Frame kit 43.3 kg (was 42.0); 52.5 kg with tarpaulins, so R11 is **not met** by 2.5 kg (was 1.1 kg).
- Frame kit cost $469.14 against the $445 value-engineering target: $24.14 over (was $443.30). R10 is reported against the target.
- Not met: R5, R6, R7, R11, R13. At risk: R8, R9. Not verifiable: R4. Met: R1, R2, R3, R12.
- Wind, anchor and snow figures are unchanged; EMT shear-out behind the pin falls to 9.0 kN, seven times the 1.28 kN worst foot load.

### Proposed, awaiting Amish (all in SNF-DEC-001)

1. Accept the design for construction changes C1 to C9 (recommended).
2. A1: guiding the ridge tubes at 2.6 m during the slide-on (R4). Recommendation: from the ground with a spare tube, timed at TRL 4; the first prototype uses a step.
3. A2: the side wall tarpaulin passing the cables at the corner anchors; settle in the R7 tarpaulin plan (O3).
4. Carried over: O1 offcuts, O2 partner and region, O3 open gable, O5 packages and carried mass, O6 node polymer, O7 anchor target, O8 1 in posts, and the four appearance-model choices of 2026-09-26.

### Pictures and checks

- Every build plan picture, making sketch and the general arrangement was looked at one by one; leaders that pointed at the wrong part, labels sitting on lines, a duplicated footer on SNF-DWG-109, the general arrangement's isometric view running under its revision table and its title block date were fixed and redrawn. `python3 .kit/drawing.py --check-text` finds no overlapping text.
- Known limit: the title block of SNF-DWG-109 (cable make-up, not to scale) reads "1:1"; the kit's title block has no "not to scale" entry. The picture itself is labelled "Not to scale".
- PDFs of every controlled document are in `docs/pdf/`.
- Concept media regenerated from the constructable model (`media/hero.png`, `media/exploded.png`, `media/concept-blueprint.*`, `media/model.glb`). The cable bolts and rings roughly double the viewer model, to about 19.9 MB (was 9.4 MB); worth a coarser export setting if the website load time matters.

### Stale, to regenerate on Amish's Mac

- `media/render-hero.png`, `media/render-exploded.png`, `media/render-detail.png` (not in this cloud copy) and `media/card.png`, `media/social-preview.png` show the printed cable tabs, the old button and pin positions and the single anchor slot.
- `cad/src/product_model.py` still draws the concept tabs and the snap hook on the eave node tab; update it to the cable bolt, ring, anchor slots and new hole positions before re-rendering.

### Safety concerns

- Raising and joining frames: a standing frame is unbraced until step 9; one person holds it until the next frame is joined, and nobody works in strong wind.
- Tensioning cables: stand out of line with a cable; hand tension only.
- Anchors: check for buried services before turning one in.
- Printing ASA-class polymer gives off fumes; print in a ventilated space.
- The shelter safety notes (wind rating, snow, fire, lightning) are unchanged.

### Recommended next step

Amish reviews SNF-DDR-003, the illustrated plan and the register, and decides open decisions 1 and 2. The renders and `product_model.py` can then be brought up to the constructable design on his Mac. Building to the plan is TRL 4 work and stays on hold.
