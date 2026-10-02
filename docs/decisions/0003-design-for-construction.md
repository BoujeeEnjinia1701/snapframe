---
doc_id: SNF-DDR-003
title: SnapFrame design for construction
project: SnapFrame
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** Draft. Made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review. Items A1 and A2 in Table 3 are proposed, awaiting Amish.

## Context

On 2026-09-30 Amish asked for every repo's build plan to show how each component is made and how it fits the next, with pictures, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The concept model of SNF-DDR-002 shows what SnapFrame does, but checking it with build123d and walking through the build found nine places where it could not be made, fixed or put up as drawn (C1 to C9 below).

The changes keep what the frame does: the same size M gable, floor, heights, tube sizes and lengths, node family (three types in four printed variants, none handed), spring buttons at every tube end, hitch pins at the 12 tension joints, cable bracing layout, anchors and tarpaulins. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now also runs 203 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, parts that must stay apart are apart by at least the stated clearance, the button holes of every tube line up with its sockets, and every node fits a 256 mm print bed. All 203 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| C1 | Spring button 25 mm and hitch pin hole 50 mm from the tube end. The V spring of a snap button runs from about 5 mm nearer the end than its button to about 45 mm deeper (20 to 65 mm), so the 8 mm hitch pin would pass through the spring. | Button hole 40 mm and hitch pin hole 15 mm from the tube end (85 mm and 60 mm from the node centre). The spring now lies 35 to 80 mm from the end, 16 mm clear of the pin. | Keeps both locks of SNF-DDR-001 D4. The pin moves toward the tube end rather than the button toward it, so the spring never crosses the pin. The steel behind the pin still resists 9.0 kN of shear-out (was 37.8 kN), seven times the 1.28 kN worst foot load [SNF-CAL-001 section 6]. |
| C2 | A 6 mm button hole through a 5 mm socket wall: the button sits below the outer surface and a fingertip cannot press it, so the joint could not be undone by hand (R4, R12). The socket mouths had square edges for the button to catch on. | A 16 mm finger recess round every button hole, leaving 1.5 mm of wall, so the button stands about 2 mm proud of the recess floor; a 1.5 mm lead-in chamfer at every socket mouth. | The tent-pole arrangement: press the button with a fingertip and pull. The chamfer pushes the button in as the tube enters. |
| C3 | Brace cables were drawn from node centre to node centre, through the printed cores. The eave nodes had an 18 mm printed tab pointing outward and down, away from most of the cables it was meant to hold; at the 1.21 kN gable cable load it would carry about 46 MPa in bending, more than printed polymer can take with the factor of 2 of R9. The middle ridge node, which takes four roof cables, and the foot nodes had no fixing at all. | Every eave node and ridge node gets a cable bolt set through its core: a stainless M10 x 90 bolt with a 30 mm washer on a flat spot face, a 14 mm spacer carrying a welded 6 mm steel ring of 32 mm bore, a 24 mm washer under the head, and a washer and nyloc nut in a recess on the far side. On the eave nodes the bolt points inward and 35° down, between the post and rafter sockets; on the ridge nodes it points straight down. The cables have a snap hook at each end that clips into the ring. The printed tabs are removed. | A bolt through the core carries cable pulls from any direction; the ring swings to line up with them, and up to four snap hooks share it. The shank sees 171 MPa at the worst node (factor 2.6 on A4-70 stainless) and the polymer about 5.6 MPa in bearing. Nothing is loaded in printed bending. The nut sits below the surface, so nothing stands proud under the tarpaulins. |
| C4 | The lower ends of the cables had nowhere to attach at the feet. | The lower snap hook of each gable and side wall cable clips into the screw anchor eye at that foot. | The cable's uplift goes straight into the anchor, which is how SNF-CAL-001 already added up the worst foot load (1.28 kN). |
| C5 | The screw anchor eye stood 32 mm above the foot plate, so a foot could lift 32 mm before its anchor held it. | Each anchor is turned in until its eye sits down on the plate across the slot (eye centre about 45 mm above the ground). | The eye clamps the plate as soon as it is snug. Any turn of the eye except along the slot bears on both slot edges. |
| C6 | One anchor slot, straight out to the side. The rear gable cable leaves its anchor inward and up at about 23°, and from a slot straight out to the side it would pass 33 mm from the foot node's centre, through the 84 mm core. | Two slots in the plate, at 45° either side of straight out, each open to a plate corner and round-ended 62 mm from the centre. Rear feet use the slot that points backward, front feet the one that points forward, middle feet either. | The gable and side wall cables then pass 10 mm or more clear of the foot nodes, posts and sockets. The foot node stays one printed variant and is not handed (R12). |
| C7 | The concept put the anchors in first, dropped the frames into the anchored feet, then joined them with eave and ridge tubes. A 1,910 mm eave or ridge tube cannot be fitted between two fixed sockets whose mouths are 1,780 mm apart; it needs 65 mm of movement at one end. | Each gable frame is built flat with its feet on, stood on its marks unanchored, and the eave and ridge tubes go into the frame already standing. The next frame is stood 70 mm short of its marks and slid 65 mm on its feet onto the three tube ends. The anchors go in last, after the frame is squared. | No part changes; only the order. A frame of about 7 kg on two foot plates slides easily on the ground. |
| C8 | The guy lines were tied to printed tabs on the end ridge nodes, as in C3. | Each guy line ties to the ring on the end ridge node's cable bolt. | Same part as C3, no extra fixing. |
| C9 | The concept did not say where each tube's holes go. | The two button holes of every tube are on opposite sides of the tube, on one marked line; hitch pin holes in the posts go through on that line. This holds for all 18 members, so every tube of a type is the same and fits any position. | One drilling rule for every tube, checked in the model for each member. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| BOM | Line 5 to 7: node specs updated (finger recesses, chamfers, cable bolt holes, two anchor slots) and node prices from the new volumes. Line 8: cables now with a snap hook at each end, thimble and clips, eye-to-eye lengths, $4.20 each (was $3.50). Line 12: snap buttons sized for each tube. New line 14: nine cable bolt sets at $2.60. | Parts added and specified for construction. |
| Mass | Frame kit 42.0 to 43.3 kg; with tarpaulins 51.1 to 52.5 kg (R11 now 2.5 kg over, was 1.1 kg); bag 13.4 to 14.7 kg without tarpaulins. Printed nodes 4.97 to 4.76 kg. | The cable bolt sets add 1.17 kg and the second snap hooks about 0.5 kg; the removed tabs and the new recesses save 0.2 kg of print. |
| Cost | Frame kit $443.30 to $469.14 against the unchanged $445 value-engineering target (`budget_usd`): $24.14 over the target. | Cable bolt sets $23.40, second snap hooks $7.00, nodes $4.56 cheaper. |
| Cable lengths | Eye to eye: gable 4,230 mm, side wall 2,520 mm, roof 2,750 mm; 29.5 m of wire in all (31.1 m node to node in v0.3). | Measured between the real attachment points in the model. |
| Drawings | SNF-DWG-001 Rev P4; making sketches SNF-DWG-101 to 109 added. | Follows the model. |
| Documents | SNF-CAL-001 v0.4, SNF-REQ-001 v0.6, SNF-PRC-001 v0.6: mass, cost, cable, pin and erection-order figures updated; cost reported against the value-engineering target. No met requirement became not met; R10 is now reported against the value-engineering target. | Follows the model. |
| Wind, anchors, snow | Unchanged: tube sizes, node positions and cable layout are the same. | |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | Guiding the ridge tubes into their sockets at 2.6 m during the slide-on of C7. R4 asks for erection without tools; a person standing on the ground reaches about 2.2 m. | (a) a folding step in the kit (about 1.5 kg); (b) guide the ridge tube from the ground with a spare tube; (c) build the roof low and lift it onto the posts. | (b), and time it in the TRL 4 user trial before adding a step; the build plan uses a step for the first prototype. |
| A2 | Where the side wall tarpaulin's lower edge passes the cables at the corner anchors (the cables leave the anchor eyes just outside the wall line). | (a) tuck the hem inside the cable at each corner; (b) a short slit with an eyelet; (c) settle it in the cutting and folding plan of R7 (open item O3). | (c), since R7 already needs a tarpaulin plan. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan SNF-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status (SNF-CAL-001 v0.4): 4 met, 5 not met, 2 at risk, 1 not verifiable at TRL 3, and R10 reported against the value-engineering target, $24.14 over (in v0.3 R10 was counted as met within the $445 figure). R11 is further from its target: 2.5 kg over, was 1.1 kg.
- The photoreal renders (`media/render-*.png`), the storefront images and the appearance model `cad/src/product_model.py` still show the printed cable tabs, the old button and pin positions and the single anchor slot; they need updating on Amish's Mac, where Blender is.
- Bought parts to confirm before buying are listed in the design decisions register (SNF-DEC-001): snap button spring length and height, snap hook gate opening, ring and tensioner ratings, anchor eye fit on the plate.
