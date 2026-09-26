---
doc_id: SNF-DDR-002
title: SnapFrame recommendations accepted
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
  change: Recommendations accepted by Amish (DDR-002); record the newly decided items, what changed and the items still open
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted (items D8 and D9); items O1 to O8 remain proposed

## Context

The TRL 3 session (`docs/REVIEW.md`, "Session 2026-09-25: TRL 3") left five new items awaiting Amish, numbered 4 to 8 in that note, alongside the three open items O1 to O3 of SNF-DDR-001. On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item that carried a recommendation is therefore decided as recommended. Items without a recommendation stay "Proposed, awaiting Amish". TRL 4 remains on hold by Amish's instruction, and nothing here goes past TRL 3.

## Options considered

The options are in `docs/REVIEW.md` (TRL 3 session, "Still awaiting Amish") and in SNF-CAL-001 v0.1, Table 5. They are summarized with each item below.

## Decision

Table 1. Newly decided items.

| # | Item (REVIEW.md) | Options | Decision | What changed in the repo |
| --- | --- | --- | --- | --- |
| D8 | R6 wind (item 4) | (a) 1 in ridge tubes (+2 sticks of 1 in, about $10; 19.7 m/s); (b) 1 in ridge tubes and posts (about $40 more; 20.3 m/s); (c) keep 3/4 in ridge tubes and rate the kit at 17.5 m/s | Decided by Amish, 2026-09-25: go with recommendation. (a) 1 in EMT ridge tubes now; a frame analysis comes before any decision on 1 in posts | `TUBE_OF["ridge"]` set to 1 in in `cad/src/model.py`; ridge node ridge bores 24.0 to 30.1 mm; STEP and STL re-exported; BOM item 3 from 3/4 in at $9.00 to 1 in at $14.00; SNF-CAL-001 v0.2: rating 17.8 to 19.7 m/s, open-gable case 13.3 to 14.7 m/s, posts now govern (factor 1.46); SNF-DWG-001 Rev P1 to P2 |
| D9 | R12 node variants (item 7) | Use the four-socket middle eave node at the corners with one blank socket, removing the handed corner nodes | Decided by Amish, 2026-09-25: go with recommendation. One eave node variant at all six eave positions; the corner socket past the gable stays blank under a push-in cap | `node_variants()` returns four variants per size (foot, eave, ridge end, ridge middle) instead of six; the handed `eave-corner-L` and `eave-corner-R` STL files were removed; BOM items 6 and 12 updated (four caps added); R12 from at risk to met |

Consequences of D8 and D9 together, size M (SNF-CAL-001 v0.1 to v0.2):

- Frame kit cost $431.09 to $443.30 (7.8 % to 10.8 % over the $400 `budget_usd`); `budget_usd` stays 400 (SNF-DDR-001 D1).
- Frame kit mass 40.6 to 42.0 kg; with tarpaulins 49.8 to 51.1 kg, so **R11 changes from met to not met** (1.1 kg over the 50 kg carry limit).
- Tube bundle 27.4 to 28.6 kg (R5 still not met, now 3.6 kg over).
- Printed nodes 4.87 kg and $122.09 to 4.97 kg and $124.30.
- Requirement status: 4 met, 5 not met, 3 at risk, 1 not verifiable, to 4 met, 6 not met, 2 at risk, 1 not verifiable.

Documents revised: SNF-PRC-001 v0.4, SNF-REQ-001 v0.4, SNF-CAL-001 v0.2, SNF-DWG-001 Rev P2, `bom/bom.csv` and `bom/bom-notes.md`, `media/` regenerated. `pitch`, `problem` and `budget_usd` in `project.yaml` are unchanged, because no accepted recommendation touched them.

Table 2. Items that remain open.

| # | Item | Why it is open | Status |
| --- | --- | --- | --- |
| O1 | Tube offcuts (39 %) | The recommendation was to decide once the first region's tube source is known (SNF-DDR-001) | Proposed, awaiting Amish |
| O2 | First co-design partner and region | No recommendation was made | Proposed, awaiting Amish |
| O3 | Open front gable (R7) | No recommendation was made | Proposed, awaiting Amish |
| O4 | R10 cost ($443): bulk EMT pricing, a lighter foot plate, or raise `budget_usd` | Options only, no recommendation | Proposed, awaiting Amish |
| O5 | R5 tube bundle (28.6 kg) and, now, R11 carried mass (51.1 kg): two tube bundles (16.5 and 12.1 kg), or relax R5 to 30 kg for a two-person carry; R11 also needs a choice | Options only, no recommendation | Proposed, awaiting Amish |
| O6 | Node polymer (R9) | No recommendation was made | Proposed, awaiting Amish |
| O7 | R8 anchor target: 1.0 kN target against 1.28 kN calculated demand | No recommendation was made | Proposed, awaiting Amish |
| O8 | 1 in posts (R6 would reach 20.3 m/s by member check) | D8 puts this after a frame analysis, which has not been run yet | Proposed, awaiting Amish once the frame analysis is done |

## Consequences

- R6 remains not met at 19.7 m/s. The frame analysis named in D8 is TRL 3 paper work and is the next calculation step; it was not run in this session.
- R11 is newly not met because the 1 in ridge tubes add 1.2 kg. This is reported to Amish under O5 and is not decided here.
- No cross-repo action follows from these decisions.
- TRL 4 work (built frame, node and anchor load tests, timed erection, purchasing) remains on hold by Amish's instruction.
