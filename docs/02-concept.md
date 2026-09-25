---
doc_id: SNF-PRC-001
title: SnapFrame design precis
project: SnapFrame
doc_type: Design precis
version: "0.2"
status: Draft
date: '2026-09-25'
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
---

# SnapFrame design precis

SnapFrame is a gable-roof shelter frame of straight 3/4 in EMT conduit joined by printed nodes. Each tube end carries a spring button that snaps into a hole in the node socket, so two adults can put the frame up by hand. The reference size M covers 4.0 x 4.0 m (16 m²) with a 2.6 m ridge, takes two standard 4 x 6 m relief tarpaulins as its skin, and packs into a 2.1 m tube bundle and one bag, about 45 kg in total. First-order numbers suggest the kit costs about $437 in prototype quantities (9 % over the $400 budget) and that 3/4 in rafters limit the wind rating to about 18 m/s, short of the 20 m/s target.

![Hero render](../media/hero.png)

*Figure 1. SnapFrame size M with a 1.75 m person for scale. The tarpaulin skin is shown on the rear bay only, so the frame, nodes and bracing stay visible. Massing model.*

## How it works

1. **Unpack.** The kit arrives as a strapped bundle of 18 straight tubes (four types, color-coded at the ends) and a bag with 15 nodes (three types), 10 brace cables, 8 screw anchors, 2 guy lines and 2 tarpaulins.
2. **Anchor the feet.** Six foot nodes are laid out on the ground with a knotted layout cord (4.0 x 4.0 m, diagonals equal). A screw anchor goes through each foot plate and is turned in by hand, using a spare tube through its eye as a lever.
3. **Build the frames.** Each of the three gable frames is two posts, two rafters, two eave nodes and one ridge node. The frame is assembled flat on the ground, then walked up and its posts dropped into the foot sockets. Every joint closes with a click as the spring button finds its hole.
4. **Tie the frames together.** Ridge and eave tubes connect the three frames. Brace cables with hand tensioners go into the rear gable, one bay of each side wall and one diagonal per bay in each roof plane, and are pulled snug. Guy lines run from the two end ridge nodes to anchors 1.5 m beyond each gable.
5. **Skin.** One tarpaulin goes over the ridge as the roof, with its long edges falling to the eaves; the second closes both side walls and the rear gable. Tarpaulins are tied through their eyelets to the tubes, never to the nodes.
6. **Strike and reuse.** Pressing each button releases its joint. Tubes and nodes go back in the bundle and bag, or the frame stays and carries better cladding later.

## Main components

Table 1. Main components. Numbers match `bom/bom.csv` and Figure 2.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Posts (6) | 3/4 in EMT, 1.65 m | One 3.05 m (10 ft) stick each; offcut 1.40 m |
| 2 | Rafters (6) | 3/4 in EMT, 2.06 m | Governs wind rating (see Table 3) |
| 3 | Ridge tubes (2) | 3/4 in EMT, 1.91 m | Same length as eave tubes; different end color only for the guide |
| 4 | Eave tubes (4) | 3/4 in EMT, 1.91 m | |
| 5 | Foot nodes (6) | Printed, socket plus 170 x 170 mm plate with anchor hole | Plate spreads load on soft ground |
| 6 | Eave nodes (6) | Printed, three or four sockets plus a cable tab | Corner and middle versions from one generator |
| 7 | Ridge nodes (3) | Printed, three or four sockets | End versions carry a guy tab |
| 8 | Brace cables (10) | 4 mm galvanized wire rope, loop ends, hand cam tensioner | About 31 m in total |
| 9 | Screw ground anchors (8) | 380 mm galvanized screw anchor with eye | Six at the feet, two for guys |
| 10 | Guy lines (2) | 6 mm polyester rope with slide tensioner | From end ridge nodes |
| 11 | Skin | Two 4 x 6 m reinforced polyethylene tarpaulins | Relief agency standard; may come from agency stock |
| 12 | Snap buttons and hitch pins | 36 spring buttons (one per tube end), 12 hitch pins on lanyards | Hitch pins back up the buttons at feet and eaves, where joints see tension |
| 13 | Bundle straps and bag | Two cam straps for the tube bundle; one duffel bag | |

### Node concept

A node is a spherical core (84 mm diameter) with one socket per member: 34 mm outside diameter, 24 mm bore, 110 mm long from the node center, so each tube engages about 65 mm. The socket axes are computed from the node positions, so a new width, length or pitch produces a new set of printable nodes; this is what makes the kit parametric. The tube end carries a stainless spring button (about 6 mm) in a hole drilled 25 mm from the end; it clicks into a matching hole in the socket. At joints that can go into tension (feet, eaves), a hitch pin on a lanyard passes through a second cross hole. The first release prints the nodes in a weather-resistant polymer; at scale, the same geometry becomes a pattern for sand-cast aluminum.

## Sizes

Table 2. Size family generated from the same parameters. Only M is modeled at TRL 2.

| Size | Floor | Bays | Eave and ridge | People at 3.5 m² each | Members | Nodes |
| --- | --- | --- | --- | --- | --- | --- |
| S | 3.0 x 3.0 m (9 m²) | 2 x 1.5 m | 1.8 m, 2.4 m | 2 | 18 | 15 (new angles) |
| M (reference) | 4.0 x 4.0 m (16 m²) | 2 x 2.0 m | 1.8 m, 2.6 m | 4 | 18 | 15 |
| L | 4.0 x 6.0 m (24 m²) | 3 x 2.0 m | 1.8 m, 2.6 m | 6 | 25 | 20 (same types as M) |

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3. Assumptions are listed in SNF-REQ-001: 3/4 in EMT (OD 23.4 mm, wall 1.24 mm, section modulus 457 mm³, about 0.70 kg/m), assumed yield 275 MPa, simply supported members between node centers, half of each tarpaulin panel's load to the frames.

Table 3. Geometry, mass, cost and wind.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Floor area | 16 m² | 4.0 x 4.0 m | R1 met |
| Headroom 2.0 m or more | 75 % of floor | Roof at 2.6 m falls 0.4 m per meter from the ridge | R2 met |
| Tube length in the kit | 33.7 m | 6 x 1.65 + 6 x 2.06 + 6 x 1.91 m | |
| Tube bought | 18 sticks of 3.05 m (54.9 m) | No two members fit one 10 ft stick | 39 % offcut; see design choices |
| Mass | about 45 kg (99 lb) | EMT 23.6, nodes 4.0, cables 2.5, anchors 3.6, tarpaulins 9.2, guys, pins and bags 2.1 kg | R11 met |
| Packages | Tube bundle 2.15 x 0.15 x 0.10 m, about 24 kg; bag about 0.08 m³, about 21 kg | Nodes, cables, anchors and tarpaulins in the bag | R5 met |
| Erection time | about 40 min for two adults | 36 snap joints at 20 s, 8 anchors at 2 min, 10 cables at 1.5 min, skin 20 min, shared by two people | R4, unverified |
| Skin area | about 51 m² for full enclosure | Roof with 150 mm eave overhang 19.3 m², side walls 14.4 m², gables 8.8 m² each | R7 partly met (48 m² available) |
| Parts cost | about $437 | Indicative prices, see `bom/bom.csv` | R10 **not met** (9 % over) |
| Frame kit without tarpaulins | about $387 | As above, less item 11 | Would meet $400 |
| Dynamic pressure at 20 m/s | 245 Pa | ½ x 1.225 x 20² | |
| Post bending at 20 m/s | 74 N·m, 162 MPa, factor 1.70 | Windward +0.8, 2.0 m bay, 1.74 m span | Meets 1.5 |
| Rafter bending at 20 m/s | 100 N·m, 218 MPa, factor 1.26 | Roof suction -0.7, 2.0 m bay, 2.15 m span | R6 **not met** |
| Wind rating with 3/4 in rafters | about 18 m/s (65 km/h, 41 mph) | Rafter stress 183 MPa at factor 1.5 | |
| Rafter with 1 in EMT at 20 m/s | 116 MPa, factor 2.4 | Section modulus 856 mm³ | Would meet R6 |
| Anchor uplift | up to about 0.6 kN per foot anchor, before cable pretension | Mean roof suction about 150 Pa on about 18.5 m², less kit weight, middle frame taking half | R8 target 1.0 kN |
| Snow | Not rated | 0.5 kPa of snow would put about 630 MPa in a 3/4 in rafter | Out of scope |

## Key design choices

All are proposed, awaiting Amish.

- **Tube size: 3/4 in EMT throughout, or 1 in EMT for the rafters.** 3/4 in keeps one socket bore for every node and is the most widely stocked size, but limits the rating to about 18 m/s. 1 in rafters meet the 20 m/s target at about $5 more per rafter ($30 per kit) and add a second socket bore. A third option is 1.33 m bays (four frames), which raises node and tube count. Recommendation: 1 in rafters, keeping 3/4 in elsewhere, and state the rating on the kit.
- **Pinned nodes with cable bracing, not rigid nodes.** Printed sockets cannot be relied on to resist bending at the joint, so the frame is treated as pinned and braced by cables. This keeps nodes small and printable, at the cost of 10 cables to tension. Recommendation: cable bracing.
- **Spring buttons plus hitch pins.** Buttons alone are fast and tool-free but carry little tension; hitch pins at feet and eaves back them up where wind lifts the frame. Recommendation: buttons everywhere, hitch pins at the 12 tension joints.
- **Printed nodes first, cast aluminum later.** Printed nodes can be made near the response in days; cast aluminum is stronger, UV-proof and cheaper in quantity, but needs a foundry. Recommendation: print for the first prototype and design every node to be castable from the printed pattern.
- **Gable roof, not a dome or barrel vault.** A gable uses four straight tube lengths, gives vertical walls for furniture and beds, and matches the rectangular tarpaulins. Domes use tube more efficiently in wind but need many node angles and cut the tarpaulin badly. Recommendation: gable.
- **Tube offcuts.** Members of 1.65 to 2.06 m leave a 0.98 to 1.40 m offcut from each 3.05 m stick (39 % of the tube bought). Options: accept it and use offcuts as anchor levers, tent pegs or a separate shade kit; shorten posts to 1.50 m so two come from one stick (eave 1.65 m, less headroom); or buy 6 m metric lengths where stocked. Recommendation: decide after the tube source for the first region is known.
- **Budget scope.** The complete kit is about $437; without tarpaulins, which relief agencies stock, it is about $387. Options: (a) define the budget as the frame kit and treat tarpaulins as agency stock; (b) cut cost (bulk EMT, cheaper filament); (c) raise `budget_usd` to about $450. Recommendation: (a), with the tarpaulin cost reported separately. `project.yaml` is unchanged.

![Exploded view](../media/exploded.png)

*Figure 2. Exploded view with BOM numbers. The skin (item 11) is left out so the frame parts stay visible; items 12 and 13 are not modeled.*

## Safety

> **Safety:** SnapFrame is an emergency shelter frame, not a storm refuge. With 3/4 in rafters it is estimated to stay elastic only up to gusts of about 18 m/s (65 km/h, 41 mph). Above that, or when a storm warning is issued, occupants should drop the skin, leave the shelter and follow local evacuation guidance. A collapsing steel frame can injure people inside.

> **Safety:** The frame is not rated for snow. Snow or ponding water on the roof can overload the rafters within hours. Clear the roof, or leave the shelter, whenever snow or standing water collects.

> **Safety:** Polyethylene tarpaulins burn quickly and drip. Keep cooking fires, candles, kerosene lamps and stoves outside the shelter or behind a non-combustible screen, keep at least 2 m between shelters where the site allows, and keep the doorway clear. A fire-retardant tarpaulin option is an open requirement (R13).

- **Erection.** Walking a frame up takes two people. Keep hands clear of sockets as tubes drop in (pinch points), and never erect or strike the frame in strong wind, when the tarpaulin acts as a sail.
- **Tube ends.** Cut EMT ends are sharp. Every tube is deburred during kit preparation, and ends sit inside sockets once assembled.
- **Guy lines and anchors.** Guy lines are a trip hazard at night; mark them with reflective tape. Screw anchors must be clear of buried cables and pipes.
- **Electrical.** The frame is conductive steel. Any lighting inside must be low-voltage DC (for example solar lanterns); mains cables must not be run on or near the frame.
- **Lightning.** A steel frame gives no reliable lightning protection. Leave it during thunderstorms where a solid building is available.

## Open questions for TRL 3

- Confirm EMT yield strength and dimensions from supplier data for the first region, and whether metric thin-wall tube of about 25 mm is stocked where EMT is not.
- Check the wind estimate with a proper load case (gusts, internal pressure through the open door, roof and wall coefficients for a small gable building) and a frame analysis with pinned nodes and cables.
- Node material: which printable polymer keeps its strength at 70 °C surface temperature under UV for two years, and what socket wall thickness is needed?
- Spring button and hitch pin loads, and whether the drilled hole in the thin EMT wall tears out under tension.
- Anchor holding capacity in sand, clay and gravel; alternatives such as sandbags or buried deadmen where screw anchors fail.
- A cutting and folding plan that makes two tarpaulins close both gables, or the case for a third tarpaulin.
- Fire-retardant tarpaulin sources and cost (R13).
- Picture-only erection guide: test with users who have not seen the kit.
- Validate floor area, headroom, erection time, wind exposure and price with users through a local partner.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
