---
doc_id: SNF-DEC-001
title: SnapFrame design decisions register
project: SnapFrame
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the build plan; open items from SNF-DDR-001 to SNF-DDR-003 and the review note; budget treated as a value-engineering target
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Amish approved the recommendations for all ten open decisions (SNF-DDR-003 accepted); moved to decisions made; To confirm items 4 and 6 and the value engineering note updated"
---

# SnapFrame design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | Snap buttons for 3/4 in and 1 in EMT: the spring reaches no more than 45 mm deeper than the button, and the button stands at least 3.5 mm above the tube surface | The spring must clear the hitch pin 15 mm from the tube end, and the button must stand proud in its finger recess | SNF-DDR-003, C1 and C2 |
| 2 | Snap hooks: the gate opens at least 14 mm, to pass the 12 mm wire of the anchor eye, and they fit the 6 mm ring | Every cable end clips to an anchor eye or a ring | SNF-DDR-003, C3 and C4 |
| 3 | Welded 6 mm ring of 32 mm bore: working load at least 2 kN; hand tensioner for 4 mm wire: working load at least 1.5 kN | The highest cable tension is 1.21 kN at 20 m/s; the tensioner rating has been unknown since TRL 3 | SNF-CAL-001, section 6 |
| 4 | Screw anchor: eye wire about 12 mm and eye about 56 mm across, so it straddles the 18 mm slot; holding capacity in the soils of the first site; a longer anchor of the same eye for the two rear corner feet | The eye clamps the foot plate; R8 needs 1.5 kN at the two rear corner feet and 1.0 kN at the others (decided 2026-10-02) | SNF-DDR-003, C5; R8 |
| 5 | EMT yield strength and dimensions from the supplier | The wind rating assumes 275 MPa yield | SNF-CAL-001, A3 |
| 6 | Print farm bed at least 230 mm, and that it can print glass- or carbon-filled PA12-class nylon (decided 2026-10-02) | The eave and middle ridge nodes are 220 mm across | SNF-DDR-003; decision of 2026-10-02 on the node polymer |

## Value engineering

Value-engineering target: USD 445 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 469.14 for the size M frame kit (USD 24.14 over the target). Tarpaulins are agency stock and costed separately (USD 50.00). Main cost drivers and savings worth trying:

- The largest lines are the tubes (USD 202.00 for 18 sticks, 39 % of the tube bought ends up as offcut), the 15 printed nodes (USD 119.74, of which the six foot nodes are USD 60.18), the brace cables (USD 42.00), the anchors (USD 32.00), the buttons, pins and caps (USD 24.00) and the cable bolt sets (USD 23.40).
- Making the design constructable added the cable bolt sets (USD 23.40) and a second snap hook on every cable (USD 7.00), and saved USD 4.56 of print; the frame kit rose from USD 443.30 to USD 469.14.
- Savings worth trying: bulk or 6 m metric tube, which also cuts the offcut (the 39 % offcut is accepted for the prototype; stock is chosen once the first region's tube source is known, decided 2026-10-02); a lighter foot plate, since the foot node is the most expensive print; lower infill on the low-stress ridge nodes in the chosen filled PA12-class nylon, once its coupons are tested; and stainless hardware bought by the hundred for the cable bolt sets.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D7: budget covers the frame kit, tarpaulins from agency stock; 1 in EMT rafters; print nodes, design for casting; spring buttons plus hitch pins at the 12 tension joints; gable with cable bracing; sizes S, M and L with M as reference; snow and cyclone out of scope | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | SNF-DDR-001 |
| 2026-09-25 | D8: 1 in EMT ridge tubes, frame analysis before any decision on posts. D9: one four-socket eave node at all six positions, the corner socket past the gable left blank and capped | Amish: "i accept all your recommendations, go with them across all repos." | SNF-DDR-002 |
| 2026-09-26 | Budget set to $445 to cover the priced frame kit (O4 closed) | Amish: "i approve all the budget items." | SNF-DDR-002 v0.2 |
| 2026-09-30 | Prototype build plan in the approved format; outstanding decisions kept out of the build plan and in this register | Amish: "this is the correct build plan ... this is a good quality document format. Extend this across all the other repos"; "don't log outstanding decisions in this build plan - that is not the place for it" | `.kit/STANDARDS.md` section 18 |
| 2026-09-30 | Fix the design where it cannot be built as drawn, keeping what it does | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | SNF-DDR-003 (the changes themselves are open decision 1) |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit; cost reported as over or under it | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens" | `.kit/STANDARDS.md` section 18 |
| 2026-10-02 | Design for construction accepted: the nine changes C1 to C9 as made (open item 1) | Amish: "i approve your recommendations for all 555 open decisions." | SNF-DDR-003, C1 to C9 |
| 2026-10-02 | Ridge tubes: the first prototype uses a folding step; guiding from the ground with a spare tube (option b) is timed in the TRL 4 user trial, and the step stays in the kit if ground guiding is slower or needs a third person (open item 2) | Amish: "i approve your recommendations for all 555 open decisions." | SNF-DDR-003, A1 |
| 2026-10-02 | Front gable closed with part of a third tarpaulin from agency stock, cut to include a door flap; the corner cable hem is settled in the same cutting plan; R7 restated to match (open item 3) | Amish: "i approve your recommendations for all 555 open decisions." | SNF-DDR-001, O3; SNF-DDR-003, A2; SNF-REQ-001 R7 |
| 2026-10-02 | Posts: the frame analysis is run now, as paper work at TRL 3; if it has not been run when the prototype tubes are bought, 1 in posts are fitted (open item 4) | Amish: "i approve your recommendations for all 555 open decisions." | SNF-DDR-002, O8 |
| 2026-10-02 | Packages: the tubes are split into two bundles (16.5 and 12.1 kg) and R5 restated as three packages of 25 kg or less; R11 is counted on the frame kit alone (43.3 kg against 50 kg), since the tarpaulins are issued separately from agency stock (open item 5) | Amish: "i approve your recommendations for all 555 open decisions." | SNF-DDR-002, O5; SNF-DDR-003 |
| 2026-10-02 | Node polymer: a glass- or carbon-filled nylon of the PA12 class, with printed coupons tested for pin bearing at 70 °C at TRL 4; PETG dropped (open item 6) | Amish: "i approve your recommendations for all 555 open decisions." | SNF-DDR-002, O6 |
| 2026-10-02 | Anchors: the target at the two rear corner feet is raised to 1.5 kN, with longer anchors there; 1.0 kN is kept at the other feet (open item 7) | Amish: "i approve your recommendations for all 555 open decisions." | SNF-DDR-002, O7 |
| 2026-10-02 | Tube offcut of 39 % accepted for the prototype on US 10 ft stock; the choice between 1.50 m posts and 6 m metric stock is made once the first region's tube source is known (open item 8) | Amish: "i approve your recommendations for all 555 open decisions." | SNF-DDR-001, O1 |
| 2026-10-02 | Partners: the IFRC Shelter Research Unit is the first candidate to approach for a technical review of the kit with standard relief tarpaulins, and Field Ready as the printing partner; the region is taken from the first warm-climate response the review points to (open item 9) | Amish: "i approve your recommendations for all 555 open decisions." | SNF-DDR-001, O2 |
| 2026-10-02 | Renders: the first three render choices accepted (tube split at the detail node, hero without guy lines, foot plate grip ribs and size mark as appearance only); the fourth (brace cable start at the detail node) withdrawn when the renders are redone (open item 10) | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26 render session, items 1 to 4 |
