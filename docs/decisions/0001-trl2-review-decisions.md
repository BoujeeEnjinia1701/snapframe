---
doc_id: SNF-DDR-001
title: SnapFrame TRL 2 review decisions
project: SnapFrame
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's decisions on the TRL 2 review items and the items that remain open
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted (items D1 to D7); items O1 to O3 remain proposed

## Context

The TRL 2 review note (`docs/REVIEW.md`, session "/populate to a strong TRL 2") listed nine items as "Proposed, awaiting Amish", and the requirements left the open-gable skin question (R7) without a recommendation. On 2026-09-25 Amish wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." Every item that carried a recommendation is therefore decided as recommended. Items without a recommendation stay open.

## Options considered

The options for each item are in the TRL 2 review note and in SNF-PRC-001 v0.2, "Key design choices". They are summarized with each decision below.

## Decision

Table 1. Decided items.

| # | Item | Options | Decision |
| --- | --- | --- | --- |
| D1 | Budget scope (R10) | (a) $400 covers the frame kit and tarpaulins come from agency stock; (b) cut cost; (c) raise `budget_usd` to about $450 | Decided by Amish, 2026-09-25: go with recommendation. (a): the $400 `budget_usd` covers the size M frame kit; tarpaulins are agency stock, costed and reported separately. `budget_usd` stays at 400. |
| D2 | Rafter tube size (R6) | 3/4 in throughout (about 18 m/s at TRL 2); 1 in EMT rafters; four frames at 1.33 m | Decided by Amish, 2026-09-25: go with recommendation. 1 in EMT rafters, 3/4 in EMT elsewhere, and the wind rating is stated on the kit. |
| D3 | Node material and process | Printed polymer; cast aluminum | Decided by Amish, 2026-09-25: go with recommendation. Print nodes for the prototype and design every node to be castable from the printed pattern. The polymer itself is not chosen. |
| D4 | Joint locking | Spring buttons only; buttons plus hitch pins | Decided by Amish, 2026-09-25: go with recommendation. Spring buttons at every tube end plus hitch pins at the 12 tension joints (6 feet, 6 eave post sockets). |
| D5 | Frame form | Gable with cable bracing; dome; barrel vault; rigid nodes | Decided by Amish, 2026-09-25: go with recommendation. Gable frame with pinned nodes and cable bracing. |
| D6 | Reference size and family | S 9 m², M 16 m², L 24 m² | Decided by Amish, 2026-09-25: go with recommendation. Size family S, M and L, with M as the reference size. |
| D7 | Out of scope | Snow and cyclone rating in the first release | Decided by Amish, 2026-09-25: go with recommendation. Snow and cyclone rating are out of scope for the first release. |

Table 2. Items that remain open.

| # | Item | Why it is open | Status |
| --- | --- | --- | --- |
| O1 | Tube offcuts: accept 39 %, shorten posts to 1.50 m, or buy 6 m metric stock | The recommendation was to decide once the first region's tube source is known, so going with it leaves the choice open | Proposed, awaiting Amish |
| O2 | First co-design partner and region | No recommendation was made | Proposed, awaiting Amish |
| O3 | Open gable (R7): two tarpaulins close the roof, both side walls and one gable only; options include a cutting and folding plan, a third tarpaulin, or accepting one open gable as the doorway | No recommendation was made | Proposed, awaiting Amish |

## Consequences

- SNF-REQ-001 v0.3 redefines R10 as the frame kit without tarpaulins. R6 keeps its 20 m/s target.
- SNF-PRC-001 v0.3 and the parametric model use 1 in rafters, which need a second socket bore (30.1 mm) on the eave and ridge nodes.
- SNF-CAL-001 shows that D2 alone does not meet R6: with a first-principles load share, the 3/4 in ridge tubes govern and the rating is about 17.8 m/s. It also shows the frame kit at about $431 (R10 not met) and the tube bundle at about 27.4 kg (R5 not met). These findings are reported in `docs/REVIEW.md` as new items awaiting Amish; this record does not decide them.
- TRL 4 work is on hold by Amish's instruction.
