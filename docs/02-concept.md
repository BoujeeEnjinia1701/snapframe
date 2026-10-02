---
doc_id: SNF-PRC-001
title: SnapFrame design precis
project: SnapFrame
doc_type: Design precis
version: "0.6"
status: Draft
date: '2026-10-01'
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
  change: Populate to TRL 2 (architecture, sizes, first-order numbers, design choices, safety, media)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Apply SNF-DDR-001 (1 in rafters, frame kit budget, decided design choices); numbers from SNF-CAL-001; parametric model and SNF-DWG-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish ($445, SNF-DDR-002); cost figure restated against it
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: Design for construction (SNF-DDR-003, Draft) applied; erection order, joints and cable fixings updated; cost against the value-engineering target
---

# SnapFrame design precis

SnapFrame is a gable-roof shelter frame of straight EMT conduit joined by printed nodes: 1 in EMT rafters and ridge tubes, and 3/4 in EMT posts and eave tubes. Each tube end carries a spring button that snaps into a hole in the node socket, so two adults can put the frame up by hand. The reference size M covers 4.0 x 4.0 m (16 m²) with a 2.6 m ridge and takes two standard 4 x 6 m relief tarpaulins from agency stock as its skin. The TRL 3 calculation note SNF-CAL-001 v0.4 puts the constructable frame kit (SNF-DDR-003) at about 43.3 kg and $469, $24 over the $445 value-engineering target, and rates the frame at about 19.7 m/s (71 km/h, 44 mph), just short of the 20 m/s target, with the 3/4 in posts governing.

![Hero render](../media/hero.png)

*Figure 1. SnapFrame size M with a 1.75 m person for scale. The tarpaulin skin is shown on the rear bay only, so the frame, nodes and bracing stay visible. Generated from the parametric model `cad/src/model.py`.*

## How it works

1. **Unpack.** The frame kit arrives as a strapped bundle of 18 straight tubes (four types, color-coded at the ends, snap buttons fitted) and a bag with 15 nodes (three families, four printed variants, cable bolts fitted to the eave and ridge nodes), 10 brace cables, 8 screw anchors, 2 guy lines, hitch pins and caps. Two tarpaulins come from agency stock.
2. **Mark out.** Six pegs mark the feet with a knotted layout cord (4.0 x 4.0 m, diagonals equal).
3. **Build the frames.** Each of the three gable frames is two posts, two rafters, two eave nodes, one ridge node and two foot nodes, assembled flat on the ground. Every joint closes with a click as the spring button finds its hole; hitch pins go in at the feet and the eave post sockets.
4. **Stand and join the frames.** The rear frame is walked up and stood on its marks. The ridge and eave tubes go into it, and the middle frame, stood 70 mm short of its marks, slides 65 mm on its feet onto the three tube ends; the front bay follows the same way (SNF-DDR-003 C7). Then the frame is squared, and a screw anchor is turned in by hand through a slot in each foot plate, using a spare tube through its eye as a lever, until the eye sits down on the plate.
5. **Brace.** Brace cables with hand tensioners go into the rear gable, one bay of each side wall and one diagonal per bay in each roof plane. Their snap hooks clip to the anchor eyes at the feet and to the steel ring on each eave and ridge node's cable bolt, and they are pulled snug. Guy lines run from the rings of the two end ridge nodes to anchors 1.5 m beyond each gable.
6. **Skin.** One tarpaulin goes over the ridge as the roof; the second closes both side walls and the rear gable. The front gable stays open (R7, awaiting Amish). The blank socket on each corner eave node takes a push-in cap. Tarpaulins are tied through their eyelets to the tubes, never to the nodes.
7. **Strike and reuse.** Pressing each button in its finger recess releases its joint. Tubes and nodes go back in the bundle and bag, or the frame stays and carries better cladding later.

## Main components

Table 1. Main components. Numbers match `bom/bom.csv`, Figure 2 and drawing SNF-DWG-001.

| # | Component | Choice | Notes |
| --- | --- | --- | --- |
| 1 | Posts (6) | 3/4 in EMT, 1.650 m | One 3.05 m (10 ft) stick each |
| 2 | Rafters (6) | 1 in EMT, 2.064 m | SNF-DDR-001 D2; second socket bore on eave and ridge nodes |
| 3 | Ridge tubes (2) | 1 in EMT, 1.910 m | SNF-DDR-002 D8 (were 3/4 in and governed the wind rating) |
| 4 | Eave tubes (4) | 3/4 in EMT, 1.910 m | Same length as item 3, smaller tube; different end color for the guide |
| 5 | Foot nodes (6) | Printed, one socket, 170 x 170 x 12 mm plate with two anchor slots at 45° | About 410 g each |
| 6 | Eave nodes (6) | Printed, four sockets and a cable bolt hole, one variant | At the corners the socket past the gable stays blank and capped (SNF-DDR-002 D9); about 256 g |
| 7 | Ridge nodes (3) | Printed, three or four sockets, all 30.1 mm bore, and a cable bolt hole | About 247 to 271 g |
| 8 | Brace cables (10) | 4 mm galvanized wire rope, thimble loop, hand tensioner, snap hook at each end | 29.5 m eye to eye |
| 9 | Screw ground anchors (8) | 380 mm galvanized screw anchor with eye | Six at the feet, two for guys |
| 10 | Guy lines (2) | 6 mm polyester rope with slide tensioner | From end ridge nodes |
| 11 | Skin | Two 4 x 6 m reinforced polyethylene tarpaulins | Agency stock, outside the kit budget (SNF-DDR-001 D1) |
| 12 | Snap buttons, hitch pins and caps | 36 spring buttons (one per tube end), 12 hitch pins on lanyards, 4 socket caps | Hitch pins at the 12 tension joints (SNF-DDR-001 D4) |
| 13 | Bundle straps and bag | Two cam straps for the tube bundle; one duffel bag | |
| 14 | Cable bolt sets (9) | Stainless M10 bolt through each eave and ridge node, with spacer, washers, nyloc nut and a welded 6 mm ring | The cables and guy lines clip to the ring (SNF-DDR-003 C3) |

### Node concept

A node is a spherical core (84 mm diameter) with one socket per member. Each socket is 110 mm long from the node center; the tube end stops 45 mm from the center, so it engages 65 mm. The bore is the tube outside diameter plus 0.6 mm (24.0 mm for 3/4 in, 30.1 mm for 1 in) and the socket wall is 5 mm. One eave node serves all six eave positions; it is symmetric about its own frame line, so it is not handed, and at the corners its outward socket stays empty under a cap. A 6 mm spring button hole sits 40 mm from the tube end, in a 16 mm finger recess so the button can be pressed by hand; at the feet and eave post sockets an 8 mm hitch pin hole sits 15 mm from the tube end, clear of the button's spring inside the tube (SNF-DDR-003 C1, C2). Each socket mouth has a lead-in chamfer. Each eave and ridge node carries a through-bolted M10 cable bolt with a steel ring, and the foot plate has two anchor slots, so the cables never load the print in bending (SNF-DDR-003 C3 to C6). Socket axes are computed from the node positions, so a new width, length or pitch produces a new set of printable nodes. The prototype prints the nodes, and the printed node is intended to become a pattern for sand-cast aluminum later (SNF-DDR-001 D3); castability is not checked at TRL 3.

## Sizes

Table 2. Size family generated from the same parameters (SNF-DDR-001 D6). The model exports the node set of every size.

| Size | Floor | Bays | Eave and ridge | People at 3.5 m² each | Members | Nodes |
| --- | --- | --- | --- | --- | --- | --- |
| S | 3.0 x 3.0 m (9 m²) | 2 x 1.5 m | 1.8 m, 2.4 m | 2 | 18 | 15 (new angles) |
| M (reference) | 4.0 x 4.0 m (16 m²) | 2 x 2.0 m | 1.8 m, 2.6 m | 4 | 18 | 15 |
| L | 4.0 x 6.0 m (24 m²) | 3 x 2.0 m | 1.8 m, 2.6 m | 6 | 25 | 20 (same types as M) |

## Key numbers

All values are from SNF-CAL-001, which lists its assumptions. They are calculations on paper, not measurements.

Table 3. Geometry, mass, cost and wind, size M.

| Quantity | Value | Requirement |
| --- | --- | --- |
| Floor area | 16.0 m² | R1 met |
| Headroom 2.0 m or more | 73 % of floor | R2 met |
| Tube length in the kit | 33.7 m (54.9 m bought, 39 % offcut) | |
| Frame kit mass | 43.3 kg (96 lb); 52.5 kg with tarpaulins | R11 **not met** (2.5 kg over) |
| Packages | Tube bundle 28.6 kg, 0.030 m³; bag 23.9 kg with tarpaulins | R5 **not met** |
| Erection time | About 46 min for two adults (estimate) | R4 not verifiable at TRL 3 |
| Skin area | 51.4 m² for full enclosure; 42.6 m² with one gable open | R7 **not met** (48 m² available) |
| Frame kit cost | About $469; value-engineering target $445 | R10: $24 over the value-engineering target |
| Dynamic pressure at 20 m/s | 245 Pa | |
| Rafter (1 in) at 20 m/s | 142 N·m, 166 MPa, factor 1.66 | Meets 1.5 |
| Ridge tube (1 in) at 20 m/s | 106 N·m, 124 MPa, factor 2.22 | Meets 1.5 (1.18 with 3/4 in) |
| Post (3/4 in) at 20 m/s | 86 N·m, 188 MPa, factor 1.46 | R6 **not met** |
| Wind rating | 19.7 m/s (71 km/h, 44 mph); 14.7 m/s with the open gable facing the wind | R6 **not met** (posts govern) |
| Worst foot anchor uplift | 1.28 kN at a rear corner, before pretension | R8 at risk (1.0 kN target) |
| Snow | Not rated; 0.5 kPa would put 416 MPa in a 1 in rafter | Out of scope |

The TRL 2 estimates (factor 1.70 for posts, 1.26 for 3/4 in rafters, about 18 m/s) spread half of each panel uniformly over the frames. SNF-CAL-001 uses 45° tributary lines, which peak at midspan and give higher moments. On that basis, a 3/4 in rafter would reach only 0.89.

![Exploded view](../media/exploded.png)

*Figure 2. Exploded view with BOM numbers. The skin (item 11) is left out so the frame parts stay visible; items 12 and 13 are not modeled.*

## Design choices

Decided by Amish on 2026-09-25 (SNF-DDR-001):

- **Tube size (D2).** 1 in EMT rafters, with the wind rating stated on the kit.
- **Budget scope (D1).** The budget covers the frame kit; Amish set it at $445 on 2026-09-26 (SNF-DDR-002) and on 2026-10-01 made it a value-engineering target, not a limit. Tarpaulins come from agency stock and are costed separately.
- **Node process (D3).** Print for the first prototype, design every node to be castable from the printed pattern.
- **Joint locking (D4).** Spring buttons at every tube end, hitch pins at the 12 tension joints.
- **Frame form (D5).** Gable roof with pinned nodes and cable bracing, not a dome, barrel vault or rigid nodes.
- **Sizes (D6)** S, M and L, with M as the reference, and **scope (D7)** without snow or cyclone rating in the first release.

Decided by Amish on 2026-09-25, going with the recommendations (SNF-DDR-002):

- **Ridge tubes (D8).** 1 in EMT ridge tubes as well, which lifts the rating from 17.8 to 19.7 m/s. Whether the posts also move to 1 in (20.3 m/s, about $30 more) waits for a frame analysis.
- **One eave node (D9).** The four-socket eave node is used at the corners with one blank, capped socket, so there are no handed nodes and R12 is met.
- **Wind rating on the kit (D2 with D8).** Until R6 is met the kit label states 19.7 m/s (71 km/h) and about 14.7 m/s with wind into the open gable.

Still proposed, awaiting Amish (all listed in the design decisions register, SNF-DEC-001): the design for construction changes of SNF-DDR-003, tube offcuts (accept 39 %, shorten posts to 1.50 m, or buy 6 m metric stock, to decide once the first region's tube source is known), the first co-design partner and region, how to treat the open front gable (R7), whether the posts move to 1 in after the frame analysis (R6), the package and carry mass (R5, R11), and the node polymer and anchor target (R9, R8). Cost is followed against the value-engineering target in the register rather than as a decision.

## Safety

> **Safety:** SnapFrame is an emergency shelter frame, not a storm refuge. By calculation (SNF-CAL-001) it stays elastic with a factor of 1.5 only up to gusts of about 19.7 m/s (71 km/h, 44 mph), and about 14.7 m/s (53 km/h) when wind blows into the open gable. Above that, or when a storm warning is issued, occupants should drop the skin, leave the shelter and follow local evacuation guidance. A collapsing steel frame can injure people inside.

> **Safety:** The frame is not rated for snow. Snow or ponding water on the roof can overload the rafters within hours. Clear the roof, or leave the shelter, whenever snow or standing water collects.

> **Safety:** Polyethylene tarpaulins burn quickly and drip. Keep cooking fires, candles, kerosene lamps and stoves outside the shelter or behind a non-combustible screen, keep at least 2 m between shelters where the site allows, and keep the doorway clear. A fire-retardant tarpaulin option is an open requirement (R13).

- **Erection.** Walking a frame up takes two people. Keep hands clear of sockets as tubes drop in (pinch points), and never erect or strike the frame in strong wind, when the tarpaulin acts as a sail.
- **Tube ends.** Cut EMT ends are sharp. Every tube is deburred during kit preparation, and ends sit inside sockets once assembled.
- **Guy lines and anchors.** Guy lines are a trip hazard at night; mark them with reflective tape. Screw anchors must be clear of buried cables and pipes.
- **Electrical.** The frame is conductive steel. Any lighting inside must be low-voltage DC (for example solar lanterns); mains cables must not be run on or near the frame.
- **Lightning.** A steel frame gives no reliable lightning protection. Leave it during thunderstorms where a solid building is available.

## Open questions

- R6: with 1 in ridge tubes the 3/4 in posts (factor 1.46) still fall short at 20 m/s. A frame analysis with pinned nodes and tension-only cables, including post buckling, cable slack and sway, comes before the decision on 1 in posts (SNF-DDR-002 D8).
- R5 and R11: the tube bundle (28.6 kg) and the complete kit with tarpaulins (51.1 kg) are over their limits; options are in `docs/REVIEW.md`.
- Confirm EMT yield strength and dimensions from supplier data for the first region, and whether metric thin-wall tube of about 25 mm is stocked where EMT is not.
- Node polymer: which printable polymer keeps its strength at 70 °C surface temperature under UV for two years (R9).
- Anchor holding capacity in sand, clay and gravel, and the rating of the hand cable tensioners (R8).
- A cutting and folding plan that closes both gables, or the case for a third tarpaulin (R7).
- Fire-retardant tarpaulin sources and cost (R13).
- Picture-only erection guide: test with users who have not seen the kit.
- Validate floor area, headroom, erection time, wind exposure and price with users through a local partner.

Drawings and media: [prototype build plan SNF-BLD-001](05-build-plan.md), [design decisions register SNF-DEC-001](06-design-decisions.md), [general arrangement SNF-DWG-001](../cad/drawings/SNF-DWG-001.pdf), [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
