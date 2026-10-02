---
doc_id: SNF-DEC-001
title: SnapFrame design decisions register
project: SnapFrame
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the build plan; open items from SNF-DDR-001 to SNF-DDR-003 and the review note; budget treated as a value-engineering target
---

# SnapFrame design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design for construction: button 40 mm and hitch pin 15 mm from the tube end, finger recesses and mouth chamfers, through-bolted cable bolts with rings in place of printed tabs, cables clipped to the anchor eyes, anchor eyes down on the plate, two anchor slots, frames slid onto the tubes before anchoring, one drilling rule for every tube | Accept C1 to C9; change any of them | Accept all nine | Every node and tube, the cables and the erection order (build plan sections 3 and 4) | SNF-DDR-003, C1 to C9 |
| 2 | Guiding the ridge tubes at 2.6 m when a frame slides onto them (R4, no tools) | (a) folding step in the kit, about 1.5 kg; (b) guide from the ground with a spare tube; (c) build the roof low and lift it onto the posts | (b), timed in the TRL 4 user trial; the first prototype uses a step | Steps 5 to 7 of the build plan | SNF-DDR-003, A1 |
| 3 | Open front gable (R7): two tarpaulins close the roof, side walls and one gable only. Includes how the side wall tarpaulin passes the cables at the corner anchors | Cutting and folding plan; a third tarpaulin; accept one open gable as the doorway | None yet; for the corner cables, settle them in the same tarpaulin plan | Step 13 (tarpaulins) | SNF-DDR-001, O3; SNF-DDR-003, A2 |
| 4 | 1 in posts (R6): the 3/4 in posts reach a factor of 1.46 at 20 m/s; 1 in posts would give 20.3 m/s by member check, about $30 more | Decide after the frame analysis named in SNF-DDR-002 D8 | Run the frame analysis first | Posts, foot nodes and eave node post sockets | SNF-DDR-002, O8 |
| 5 | Packages and carried mass (R5, R11): tube bundle 28.6 kg against 25 kg; complete kit with tarpaulins 52.5 kg against 50 kg | Two tube bundles (16.5 and 12.1 kg); relax R5 to 30 kg for a two-person carry; and a choice for R11 | None yet | Packing only; not the prototype build | SNF-DDR-002, O5; SNF-DDR-003 |
| 6 | Node polymer (R9): printed sockets at 70 °C carrying 32 MPa of pin bearing with the factor of 2 | ASA, PETG, nylon blends; later cast aluminium | None yet | Printing of every node (section 3 of the build plan assumes ASA class) | SNF-DDR-002, O6 |
| 7 | Anchor target (R8): 1.0 kN target against 1.28 kN calculated demand at a rear corner foot | Raise the target; longer anchors at the rear corners; more pretension in the guys | None yet | Anchor choice | SNF-DDR-002, O7 |
| 8 | Tube offcuts: 39 % of the tube bought is offcut | Accept; shorten posts to 1.50 m; buy 6 m metric stock | Decide once the first region's tube source is known | Tube cutting list | SNF-DDR-001, O1 |
| 9 | First co-design partner and region | Not yet listed | None yet | None in the prototype build | SNF-DDR-001, O2 |
| 10 | Appearance model choices from the render session: tube split at the detail node as a render device; hero without guy lines; foot plate grip ribs and size mark as appearance only; brace cable start at the detail node | Accept each, or change the renders | Accept the first three; the fourth is overtaken by the cable bolt (SNF-DDR-003, C3) and is withdrawn when the renders are redone | Photoreal renders only | `docs/REVIEW.md`, 2026-09-26 render session, items 1 to 4 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | Snap buttons for 3/4 in and 1 in EMT: the spring reaches no more than 45 mm deeper than the button, and the button stands at least 3.5 mm above the tube surface | The spring must clear the hitch pin 15 mm from the tube end, and the button must stand proud in its finger recess | SNF-DDR-003, C1 and C2 |
| 2 | Snap hooks: the gate opens at least 14 mm, to pass the 12 mm wire of the anchor eye, and they fit the 6 mm ring | Every cable end clips to an anchor eye or a ring | SNF-DDR-003, C3 and C4 |
| 3 | Welded 6 mm ring of 32 mm bore: working load at least 2 kN; hand tensioner for 4 mm wire: working load at least 1.5 kN | The highest cable tension is 1.21 kN at 20 m/s; the tensioner rating has been unknown since TRL 3 | SNF-CAL-001, section 6 |
| 4 | Screw anchor: eye wire about 12 mm and eye about 56 mm across, so it straddles the 18 mm slot; holding capacity in the soils of the first site | The eye clamps the foot plate; R8 needs 1.0 kN per anchor | SNF-DDR-003, C5; R8 |
| 5 | EMT yield strength and dimensions from the supplier | The wind rating assumes 275 MPa yield | SNF-CAL-001, A3 |
| 6 | Print farm bed at least 230 mm, and the polymer it can print | The eave and middle ridge nodes are 220 mm across | SNF-DDR-003; open decision 6 |

## Value engineering

Value-engineering target: USD 445 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 469.14 for the size M frame kit (USD 24.14 over the target). Tarpaulins are agency stock and costed separately (USD 50.00). Main cost drivers and savings worth trying:

- The largest lines are the tubes (USD 202.00 for 18 sticks, 39 % of the tube bought ends up as offcut), the 15 printed nodes (USD 119.74, of which the six foot nodes are USD 60.18), the brace cables (USD 42.00), the anchors (USD 32.00), the buttons, pins and caps (USD 24.00) and the cable bolt sets (USD 23.40).
- Making the design constructable added the cable bolt sets (USD 23.40) and a second snap hook on every cable (USD 7.00), and saved USD 4.56 of print; the frame kit rose from USD 443.30 to USD 469.14.
- Savings worth trying: bulk or 6 m metric tube, which also cuts the offcut (open decision 8); a lighter foot plate, since the foot node is the most expensive print; lower infill on the low-stress ridge nodes once the polymer is chosen (open decision 6); and stainless hardware bought by the hundred for the cable bolt sets.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D7: budget covers the frame kit, tarpaulins from agency stock; 1 in EMT rafters; print nodes, design for casting; spring buttons plus hitch pins at the 12 tension joints; gable with cable bracing; sizes S, M and L with M as reference; snow and cyclone out of scope | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | SNF-DDR-001 |
| 2026-09-25 | D8: 1 in EMT ridge tubes, frame analysis before any decision on posts. D9: one four-socket eave node at all six positions, the corner socket past the gable left blank and capped | Amish: "i accept all your recommendations, go with them across all repos." | SNF-DDR-002 |
| 2026-09-26 | Budget set to $445 to cover the priced frame kit (O4 closed) | Amish: "i approve all the budget items." | SNF-DDR-002 v0.2 |
| 2026-09-30 | Prototype build plan in the approved format; outstanding decisions kept out of the build plan and in this register | Amish: "this is the correct build plan ... this is a good quality document format. Extend this across all the other repos"; "don't log outstanding decisions in this build plan - that is not the place for it" | `.kit/STANDARDS.md` section 18 |
| 2026-09-30 | Fix the design where it cannot be built as drawn, keeping what it does | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | SNF-DDR-003 (the changes themselves are open decision 1) |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit; cost reported as over or under it | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens" | `.kit/STANDARDS.md` section 18 |
