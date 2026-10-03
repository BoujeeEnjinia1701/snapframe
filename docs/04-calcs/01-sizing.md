---
doc_id: SNF-CAL-001
title: SnapFrame sizing calculations
project: SnapFrame
doc_type: Calculation
version: "0.6"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First sizing note for TRL 3 (geometry, wind, bracing, anchors, joints, mass, packages, cost, skin, erection time)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). 1 in ridge tubes and one eave node variant; results rerun
- version: "0.3"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish ($400 to $445, SNF-DDR-002); script rerun; R10 not met to met
- version: "0.4"
  date: '2026-10-01'
  author: Amish Chadha
  change: Design for construction (SNF-DDR-003, Draft) rerun; cable bolt check added; cost reported against the value-engineering target
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Status against the targets restated by Amish on 2026-10-02 (R5, R7, R8, R11) and the node polymer choice; no figures changed"
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Approved decisions of 2026-10-02 carried into the numbers: frame analysis run (SNF-DDR-002 D8; rating 19.7 to 19.5 m/s), nodes re-estimated for filled PA12-class nylon, folding step, long rear anchors, two sets of straps, two tube bundles, three tarpaulins with the cutting plan; frame kit $469.14 to $700.56"
---

# SnapFrame sizing calculations

With the decisions in SNF-DDR-001 to SNF-DDR-003 and those of 2026-10-02 (SNF-DEC-001), the size M frame meets its floor, headroom, size-family, packages, skin, carried mass and part-count targets. Two requirements are **not met**: wind (R6) and fire (R13). Two are at risk: anchors (R8) and nodes (R9). The frame analysis named in SNF-DDR-002 D8, run for this version, adds axial force to the bending of the member check and puts the weakest member, the windward 3/4 in post, at a factor of 1.43 on yield at 20 m/s (1.46 by the member check). The frame is rated at about **19.5 m/s** (70 km/h, 44 mph), down from 19.7 m/s; with rigid knees and ridge, which the sockets do not guarantee and which are not credited, it would reach 20.3 m/s. The posts stay 3/4 in, because the analysis has been run (the 1 in fallback applied only if it had not been); 1 in posts remain an option at about $30 and 20.3 m/s. The frame kit is now about **$701**, **$256 over the $445 value-engineering target** (a control target, not a limit; Amish, 2026-10-01): the nodes in filled PA12-class nylon cost $316 against $120 in ASA, and the folding step, long rear anchors and second straps add $35. The frame kit weighs **46.2 kg** (limit 50 kg) in three packages of 16.7, 12.3 and 17.2 kg; the three tarpaulins add 13.7 kg from agency stock.

Every number in this note is printed by `docs/04-calcs/sizing.py` (run from the repo root). Geometry, cut lengths and node volumes come from the parametric model `cad/src/model.py`, so the note, the model, drawing SNF-DWG-001 and `bom/bom.csv` agree. This is a first-order hand calculation with a two-dimensional frame analysis of the middle frame (section 5), not a code check. Version 0.2 reruns the script after SNF-DDR-002; every changed number is noted with its v0.1 value. Version 0.3 changed only the budget, from $400 to $445 (SNF-DDR-002). Version 0.4 reruns the script on the constructable model of SNF-DDR-003: the hitch pin moves to 15 mm from the tube end, the cables run between their real attachment points (anchor eyes and cable bolt rings), the cable bolt is checked, and the masses and costs of the new parts are added. Every changed number gives its v0.3 value. The budget is reported as a value-engineering target, as Amish set out on 2026-10-01. Version 0.6 carries the decisions of 2026-10-02 into the numbers: the frame analysis, filled nylon nodes, the folding step, long rear anchors, second straps, two tube bundles and the cutting plan for three tarpaulins; every changed number gives its v0.5 value.

## 1. Method

1. Build the size M geometry from the model parameters: 4.0 x 4.0 m floor, two 2.0 m bays, eave nodes at 1.8 m, ridge nodes at 2.6 m, foot node centers 60 mm above ground.
2. Compute section properties of 3/4 in and 1 in EMT from the nominal ANSI C80.3 diameters and walls.
3. Apply a gust dynamic pressure to the skin, share each tarpaulin panel's load between its four edge members with 45° tributary lines, check each member as simply supported between node centers, and run a plane frame analysis of the middle frame with the same loads (axial force added to bending).
4. Follow the loads into the cable bracing, the foot anchors and the pinned joints.
5. Add up mass, package size and cost from the model and the BOM prices, and check the skin area and erection time.

## 2. Assumptions

Table 1. Assumptions. Each is used only where stated.

| # | Assumption | Value | Basis |
| --- | --- | --- | --- |
| A1 | 3/4 in EMT | OD 23.42 mm (0.922 in), wall 1.245 mm (0.049 in) | ANSI C80.3 nominal; OD and ID checked against [Engineering ToolBox](https://www.engineeringtoolbox.com/conduit-size-d_1738.html) |
| A2 | 1 in EMT | OD 29.54 mm (1.163 in), wall 1.448 mm (0.057 in); rafters (SNF-DDR-001 D2) and ridge tubes (SNF-DDR-002 D8) | As A1 |
| A3 | Steel yield strength | 275 MPa (40 ksi) | Assumed; C80.3 does not set a yield, so confirm from supplier data |
| A4 | Design gust, safety factor | 20 m/s, 1.5 on yield | R6 |
| A5 | Air density | 1.225 kg/m³ | Sea level, 15 °C |
| A6 | Pressure coefficients | Windward wall +0.8, leeward wall -0.5, roof -0.7 on both slopes, net of internal pressure for a closed shelter | First-order values in the style of ASCE/SEI 7; not a code check |
| A7 | Open gable sensitivity | Internal pressure +0.55 when the wind blows into the open gable | Partially enclosed building value in the style of ASCE/SEI 7 |
| A8 | Panel load share | 45° tributary lines from each panel corner: triangles on the short edges, trapezoids on the long edges | Usual two-way rule for a panel tied on four edges |
| A9 | Members | Simply supported between node centers in the member check; in the frame analysis the knees and ridge are pinned (design basis) and, as a bound only, rigid | Conservative for bending; a socket with 0.3 mm clearance does not guarantee fixity |
| A10 | Bracing | Tension-only cables; the rear gable is the only braced frame across the span; the roof and side walls carry the rest to it | Concept bracing layout (SNF-PRC-001) |
| A11 | Wire rope | 4 mm 7x19 galvanized, minimum breaking load 8.0 kN | Typical catalog value, unverified |
| A12 | Printed nodes | Density 1,200 kg/m³, 55 % effective fill, filament $55/kg plus $1.50 machine time and hardened nozzle wear per node | Glass- or carbon-filled PA12-class nylon, chosen on 2026-10-02 (SNF-DEC-001); indicative filament price and a density between carbon-filled (about 1,100) and glass-filled (about 1,300); v0.5 used ASA at 1,070 kg/m³ and $22/kg plus $1.00 |
| A13 | Tarpaulins | Three 4 x 6 m, 190 g/m², $25 each, from agency stock | Relief tarpaulin class; outside the frame kit cost (SNF-DDR-001 D1); third added 2026-10-02 |
| A14 | Tube prices | 3.05 m (10 ft) stick: 3/4 in $9.00, 1 in $14.00 | Indicative US retail, not quotes |
| A15 | Corner eave nodes | The four-socket eave node with the socket past the gable left blank and capped | SNF-DDR-002 D9 |
| A16 | Cable bolt | M10 stainless A4-70 (yield 450 MPa), load applied at the ring 9.5 mm from the spot face, both cables of a rear corner eave node added at full value | SNF-DDR-003 C3; conservative upper bound |
| A17 | Cable bolt sets and second snap hooks | 0.13 kg and $2.60 a set; cable assembly $4.20 and 0.17 kg of fittings | Indicative catalog values |
| A18 | Folding step | 1.5 kg, $25; top tread 500 mm, folded 0.50 x 0.45 x 0.08 m; a person standing reaches 2.2 m | Indicative retail price of a light two-step folding step; reach from SNF-DDR-003 A1 |
| A19 | Long screw anchor | 560 mm, 0.66 kg, $6.00, rated 1.5 kN | Item 9 scaled by length (560/380); rating to be confirmed when bought |
| A20 | Bundle straps | Four 25 mm cam straps, 0.2 kg and $3.00 each; duffel 0.6 kg and about $14 | Indicative; two straps on each tube bundle |

## 3. Geometry

The size M floor is 4.0 x 4.0 m (16.0 m²), room for 4.6 people at the Sphere minimum of 3.5 m² each. The roof pitch is 21.8°. Taking the underside of the 1 in rafter, the roof is 2.0 m or higher over the central 2.92 m of the 4.0 m span, which is **73 %** of the floor (R2 needs 60 %).

Table 2. Cut lengths from the model (node-center distance less 45 mm at each end).

| Size | Floor | Post | Rafter | Ridge and eave |
| --- | --- | --- | --- | --- |
| S | 3.0 x 3.0 m (9.0 m²) | 1.650 m | 1.526 m | 1.410 m |
| M | 4.0 x 4.0 m (16.0 m²) | 1.650 m | 2.064 m | 1.910 m |
| L | 4.0 x 6.0 m (24.0 m²) | 1.650 m | 2.064 m | 1.910 m |

The model generates the node set of each size (four printed variants per size: foot, eave, ridge end and ridge middle, none handed) and exports each as STL, so R3 is met at model level. M and L share every tube length.

## 4. Tube sections

Table 3. Section properties.

| Tube | Area | Second moment | Section modulus | Mass |
| --- | --- | --- | --- | --- |
| 3/4 in EMT | 86.7 mm² | 5,348 mm⁴ | 457 mm³ | 0.681 kg/m |
| 1 in EMT | 127.8 mm² | 12,639 mm⁴ | 856 mm³ | 1.003 kg/m |

## 5. Wind

At 20 m/s the dynamic pressure is q = ½ x 1.225 x 20² = **245 Pa**, giving 171.5 Pa of roof suction and 196.0 Pa on the windward wall.

A roof panel is 2.00 m (between frames) by 2.154 m (eave to ridge). With 45° tributary lines, each rafter edge takes a trapezoid of 1.154 m² (26.8 % of the panel) and the ridge and eave edges each take a triangle of 1.000 m². A wall panel is 2.00 m by 1.740 m; each post edge takes a triangle of 0.757 m² and the eave and ground edges trapezoids of 0.983 m². The TRL 2 estimate spread half of each panel uniformly onto the frames; the tributary rule gives a similar total but peaks at midspan, which raises the midspan moment by about 40 %.

Table 4. Member check at 20 m/s, middle frame unless stated.

| Member | Tube | Moment | Stress | Factor on yield | Against 1.5 |
| --- | --- | --- | --- | --- | --- |
| Rafter | 1 in | 141.8 N·m | 166 MPa | 1.66 | Meets |
| Ridge tube | 1 in | 106.2 N·m | 124 MPa | 2.22 | Meets (1.18 with 3/4 in in v0.1) |
| Post (windward) | 3/4 in | 86.0 N·m | 188 MPa | **1.46** | **Below** |
| Eave tube, windward side | 3/4 in | 68.0 N·m | 149 MPa | 1.85 | Meets |
| Eave tube, leeward side | 3/4 in | 80.9 N·m | 177 MPa | 1.55 | Meets |
| End rafter, wind on the rear gable | 1 in | 134.3 N·m | 157 MPa | 1.75 | Meets |

Stress scales with the square of wind speed, so the rating is the speed at which the weakest member reaches a factor of 1.5.

**Frame analysis (SNF-DDR-002 D8, run in this version).** The middle frame is modelled as a plane frame of its two posts and two rafters, 16 beam elements a member, with the feet pinned, the eave nodes held across the span by the braced roof and rear gable (section 6), and the same panel loads as Table 4. Axial force is added to bending, stress = M/S + N/A. The analysis reproduces the member check (post 85.7 N·m against 86.0, rafter 141.8 N·m against 141.8) and adds the axial force, 369 N in the post and 496 N in the rafter.

Table 4a. Frame analysis of the middle frame at 20 m/s, three joint assumptions.

| Joints | Windward post (3/4 in) | Rafter (1 in) | Leeward post | Rating | Governing member |
| --- | --- | --- | --- | --- | --- |
| **Pinned knees and ridge (design basis)** | 85.7 N·m, 369 N, 192 MPa, **1.43** | 141.8 N·m, 496 N, 170 MPa, 1.62 | 2.26 | **19.5 m/s (70 km/h, 44 mph)** | Windward post |
| Rigid knees, pinned ridge (bound) | 82.2 N·m, 347 N, 184 MPa, 1.49 | 145.3 N·m, 447 N, 173 MPa, 1.59 | 1.56 | 20.0 m/s | Windward post |
| Rigid knees and ridge (upper bound) | 71.5 N·m, 347 N, 161 MPa, 1.71 | 125.4 N·m, 617 N, 151 MPa, 1.82 | 2.13 | 20.3 m/s | Eave tube (leeward), 1.55 |
| 1 in posts, pinned joints | not governing | 1.62 | not governing | 20.3 m/s | Eave tube (leeward), 1.55 |

The sockets give an unknown knee stiffness (0.3 mm of clearance, then polymer bearing), so no fixity is credited and the pinned case is the design basis. The finding is that the posts still govern, at 1.43 once the axial force is added, so the rating moves from 19.7 to 19.5 m/s; the eave tubes and ridge tubes keep their member-check factors. Whether a real knee gives the fixity of the bounds is a TRL 4 test (knee rotation under load). The 1 in post option remains open at about $30 more (6 sticks, $5 each) and 20.3 m/s. Because the analysis has been run, the 1 in posts that SNF-DEC-001 called for if it had not been run when the tubes are bought are not fitted; the model, nodes and BOM keep 3/4 in posts.

Table 5. Wind rating and sensitivity.

| Case | Rating at factor 1.5 | Governing member |
| --- | --- | --- |
| **As decided: 1 in rafters and ridge tubes, 3/4 in posts and eave tubes (SNF-DDR-002 D8), frame analysis with axial force** | **19.5 m/s (70 km/h, 44 mph)** (19.7 m/s by the member check, bending only) | Post, 1.43 at 20 m/s (1.46 bending only) |
| TRL 2 concept, 3/4 in throughout | 15.4 m/s | Rafter, 0.89 at 20 m/s |
| SNF-DDR-001 only: 1 in rafters, 3/4 in elsewhere (v0.1 baseline) | 17.8 m/s | Ridge tube, 1.18 at 20 m/s |
| 1 in rafters, ridge tubes and posts | 20.3 m/s (same by the frame analysis) | Eave tube (leeward), 1.55 at 20 m/s |
| As decided, door flap open and wind into it (internal pressure +0.55) | 14.7 m/s (13.3 m/s in v0.1) | Eave tube (leeward), 0.81 at 20 m/s |

For comparison, the TRL 2 method (half of each panel, uniform) gives 99 N·m and 218 MPa in a 3/4 in rafter, which matches SNF-PRC-001 v0.2; that method understated the midspan moment. The open door case matters: with the door flap open and the wind blowing into it, the opening (1.7 m² of a 8.8 m² gable) makes the shelter partially enclosed, internal pressure adds to the roof suction and the wall suction, and the rating falls to about 14.7 m/s. The front gable is now closed by the third tarpaulin (R7, decided 2026-10-02), so this case applies only while the flap is open; tying the flap shut in strong wind removes it. The frame analysis above gives the same 20.3 m/s for 1 in posts as the member check.

Snow is out of scope (SNF-DDR-001 D7). As a check for the safety note, 0.5 kPa of snow on plan puts 356 N·m and 416 MPa into a middle 1 in rafter, well past yield.

## 6. Bracing, anchors and joints

Wind across the span puts 2,217 N on the two side walls; about 1,108 N reaches eave level. With the rear gable as the only braced frame across the span, its active X cable carries **1,209 N** and pulls up on its foot with 482 N. The roof acts as a cantilever from the rear gable; the resulting couple of 2,217 N·m puts 554 N into each side wall, 735 N into a side wall cable and another 482 N of uplift at its foot. Wind along the ridge on the closed rear gable (1,678 N) puts 556 N into a side wall cable. The highest cable tension is 1.2 kN, a factor of 6.6 on the assumed 8.0 kN breaking load of 4 mm wire rope; the hand tensioner rating is unknown.

Roof suction lifts the middle frame with 1,372 N against 116 N of its own weight, so each middle foot anchor sees **0.63 kN** and each end foot 0.31 kN. At a rear corner foot, the gable cable and the side wall cable both pull up as well: 0.31 + 0.48 + 0.48 = **1.28 kN** before cable pretension, above the 1.0 kN target in R8 and inside the 1.5 kN target set for the two rear corner feet on 2026-10-02 (SNF-DEC-001), where the kit now has two longer anchors, 560 mm against 380 mm (BOM item 16, rated 1.5 kN).

At that foot the hitch pin bears on the polymer socket at 16.0 MPa, or **32.0 MPa** with the factor of 2 in R9, and on the EMT wall at 64 MPa. With the pin hole now 15 mm from the tube end (SNF-DDR-003 C1), the EMT shear-out capacity behind it is about 9.0 kN (37.8 kN at 50 mm in v0.3), seven times the load, so the steel is still not the limit; the polymer socket is. A rafter end transfers 198 N of shear into its socket, a nominal bearing pressure of 0.10 MPa over 65 mm of engagement.

The cables now clip to an M10 cable bolt through each eave and ridge node (SNF-DDR-003 C3). The worst node is a rear corner eave node, which takes the gable cable and a roof cable; taking both at full value together (1,765 N, an upper bound) with the ring 9.5 mm from the spot face gives 16.8 N·m and **171 MPa** in the shank, a factor of **2.6** on A4-70 stainless, and about 5.6 MPa of bearing on the polymer (11.2 MPa with the factor of 2 in R9). The printed tab it replaces would have carried about 46 MPa in bending at the gable cable load alone.

## 7. Nodes, mass, packages and cost

Table 6. Printed nodes, size M, from the model volumes, in filled PA12-class nylon (A12).

| Node | Count | Solid volume | Printed mass | Cost each |
| --- | --- | --- | --- | --- |
| Foot | 6 | 697.3 cm³ | 460 g (v0.5, ASA: 410 g) | $26.81 ($10.03) |
| Eave (all six; corners with one blank socket) | 6 | 434.3 cm³ | 287 g (256 g) | $17.27 ($6.62) |
| Ridge, end | 2 | 419.3 cm³ | 277 g (247 g) | $16.72 ($6.43) |
| Ridge, middle | 1 | 461.3 cm³ | 304 g (271 g) | $18.25 ($6.97) |

The 15 nodes weigh 5.34 kg and cost about $316 (v0.5: 4.76 kg, $120). The model volumes are unchanged; the polymer is 12 % denser and the filament 2.5 times the price, and each node carries $0.50 more machine time. The prices are indicative: a print farm quote for filled nylon, a lower infill on the low-stress ridge nodes after coupon tests, or casting the nodes in aluminum are the ways to bring this line down (SNF-DEC-001, value engineering). With one eave node variant (SNF-DDR-002 D9), a size M kit prints four node variants in three families, none of them handed.

Table 7. Mass and packages, size M.

| Item | Mass |
| --- | --- |
| Tubes (33.74 m) | 28.20 kg |
| Nodes | 5.34 kg (v0.5: 4.76 kg) |
| Brace cables (29.5 m eye to eye), snap hooks and tensioners | 3.62 kg |
| Cable bolt sets (9) | 1.17 kg |
| Screw anchors (6 standard, 2 long) | 4.03 kg (v0.5: 3.60 kg) |
| Folding step | 1.50 kg (new) |
| Guy lines | 0.28 kg |
| Buttons and hitch pins | 0.72 kg |
| Straps (four) and bag | 1.40 kg (v0.5: 1.00 kg) |
| **Frame kit** | **46.2 kg (102 lb)** (v0.5: 43.3 kg) |
| Three tarpaulins, agency stock | 13.7 kg (two: 9.1 kg) |
| **With tarpaulins** | **59.9 kg** (v0.5: 52.5 kg) |

The tubes go in two bundles, as Amish decided on 2026-10-02 (SNF-DEC-001): bundle A holds the six rafters and two ridge tubes, **16.7 kg** and 0.017 m³ with two cam straps; bundle B holds the six posts and four eave tubes, **12.3 kg** and 0.013 m³ with two cam straps. The bag weighs **17.2 kg** (30.9 kg with the three tarpaulins) and holds about 0.075 m³ of parts, the folded step among them, in a duffel of about 0.08 m³. Every package is under the 25 kg and 0.10 m³ of R5 as restated. Since 2026-10-02 R11 counts the frame kit alone (46.2 kg against 50 kg, 3.8 kg of margin); the tarpaulins are issued separately from agency stock (SNF-DEC-001).

Table 8. Cost, size M.

| Item | Cost |
| --- | --- |
| Tubes: 10 sticks of 3/4 in, 8 of 1 in | $202.00 |
| Nodes (15), filled PA12-class nylon | $316.16 (v0.5: $119.74) |
| Brace cables (10) | $42.00 |
| Cable bolt sets (9) | $23.40 |
| Screw anchors (6 standard) | $24.00 (v0.5: 8 at $4.00, $32.00) |
| Long screw anchors (2, rear corner feet) | $12.00 (new) |
| Folding step (1) | $25.00 (new) |
| Guy lines (2) | $6.00 |
| Buttons and hitch pins | $24.00 |
| Straps (four) and bag | $26.00 (v0.5: $20.00) |
| **Frame kit** | **$700.56** (v0.5: $469.14) |
| Value-engineering target | $445 (a control target, not a limit): **$255.56 over** |
| Three tarpaulins, agency stock | $75.00 (two: $50.00) |
| With tarpaulins | $775.56 |

Value-engineering target: USD 445. Estimated cost of the constructable design: USD 700.56 (USD 255.56 over the target). The nodes account for $196 of the $231 rise; the folding step ($25), the two long anchors in place of two standard ones (+$4) and the second straps (+$6) for the other $35. `bom/bom.csv` sums to $700.57, a cent more, because it rounds each node price to the cent.

The kit buys 54.9 m of tube and uses 33.7 m, a 39 % offcut.

## 8. Skin and erection time

Full enclosure needs about 51.4 m² (roof with 150 mm overhang 19.4 m², side walls 14.4 m², each gable 8.8 m²). Three 4 x 6 m tarpaulins give 72.0 m², and the cutting plan (Figure 18 of the build plan, `cad/src/skin_plan.py`, 19 checks) uses 59.6 m² of it:

Table 9a. Cutting plan for three tarpaulins, size M.

| Tarpaulin | Pieces | Used | Spare |
| --- | --- | --- | --- |
| 1 | Roof sheet, whole: 6.0 m across the slopes (4.31 m of rafters and 0.85 m of eave skirt each side), 4.0 m along the ridge | 24.0 m² | none |
| 2 | Three strips 4.0 x 2.0 m: left and right side walls (1.8 m wall and 0.2 m to tuck under the roof sheet) and the lower part of the rear gable | 24.0 m² | none |
| 3 | Front gable lower strip 4.0 x 2.0 m with a door flap of 1.0 x 1.7 m (two slits from the ground edge, hinged at the top, rolled up and tied); two gable tops, base 4.0 m and height 0.9 m, interlocked in a 6.0 x 0.9 m strip | 11.6 m² | 12.4 m² |

The corner cable hem settles the question left in SNF-DDR-003 A2: each strip's two ground corners carry a cut-out of 0.40 x 0.20 m, edges folded and taped, which the model shows is enough for the gable and side wall cables to leave the anchor eyes (every one is 0.20 m up after a run of at most 0.31 m, inside 0.40 m). This closes R7 on paper with the front gable, and the spare 12.4 m² covers patches and repairs.

Erection time is estimated at about **46 min** for two adults: 63 person-minutes of one-person tasks (36 snap joints at 20 s, 8 anchors at 2 min, 10 cables at 1.5 min, skin 20 min) shared by two, plus 14 min of two-person tasks (layout and raising three frames). This is an estimate only; R4 needs a timed trial. The erection order of SNF-DDR-003 C7 (frames slid onto the tube ends, anchors last) uses the same tasks, so the estimate is unchanged.

## 9. Results against requirements

Table 9. Requirement status, size M, against the targets as restated on 2026-10-02.

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R5 | Ship flat | Longest member 2.064 m; bundles 16.7 and 12.3 kg (0.017 and 0.013 m³); bag 17.2 kg, 0.075 m³ | 2.1 m or less; three packages, each 25 kg or less and 0.10 m³ or less (restated 2026-10-02) | Met (tarpaulins are issued separately; 30.9 kg with three) |
| R6 | Resist wind | Rating 19.5 m/s; post factor 1.43 at 20 m/s (frame analysis, v0.5: 19.7 m/s and 1.46) | Factor 1.5 at 20 m/s | **Not met** (posts; frame analysis run, posts stay 3/4 in; 1 in posts would give 20.3 m/s for about $30) |
| R7 | Fit standard tarpaulins | Cutting plan drawn: 59.6 m² of 72.0 m² in three tarpaulins; full enclosure 51.4 m²; door flap 1.0 x 1.7 m; corner cable hems 0.40 x 0.20 m | Both gables closed, with part of a third tarpaulin for the front gable (restated 2026-10-02) | Met (cutting plan drawn and checked) |
| R11 | Carried by two people | Frame kit 46.2 kg; 59.9 kg with three tarpaulins | 50 kg or less, frame kit alone (restated 2026-10-02) | Met (46.2 kg, 3.8 kg of margin) |
| R13 | Limit fire spread | Standard polyethylene tarpaulins | Flame spread test or fire-retardant option | **Not met** |
| R8 | Anchor without a hammer | Demand up to 1.28 kN at a rear corner foot, before pretension; two long anchors (item 16) fitted there | Each anchor holds 1.0 kN; 1.5 kN at the two rear corner feet (raised 2026-10-02) | **At risk** (demand inside the raised target; capacity not verifiable at TRL 3) |
| R9 | Nodes strong in sun and cold | Pin bearing 32.0 MPa with the factor of 2 | Factor 2 after two years, -10 to 70 °C | **At risk** (filled PA12-class nylon chosen on 2026-10-02; coupons to be tested at 70 °C at TRL 4) |
| R4 | Go up without tools | About 46 min estimated | 60 min or less | Not verifiable at TRL 3 |
| R1 | Living space | 16.0 m² (4.6 people at 3.5 m²) | 16 m² or more | Met |
| R2 | Headroom | 73 % of floor at 2.0 m or more | 60 % or more | Met |
| R3 | Several sizes | S, M and L node sets generated and exported | Three sizes from one model | Met |
| R10 | Value-engineering target | Frame kit $700.56 | $445 value-engineering target, frame kit without tarpaulins | Over the value-engineering target by $255.56 (reported against the target, not as met or not met) |
| R12 | Repairable in the field | 4 tube types; 3 node types in 4 printed variants, none handed | 4 tube types and 3 node types | Met (at risk in v0.1) |

Summary against the targets restated on 2026-10-02: 7 met (R1, R2, R3, R5, R7, R11, R12), 2 not met (R6, R13), 2 at risk (R8, R9), 1 not verifiable at TRL 3 (R4), and R10 reported against the value-engineering target, $255.56 over. The statuses are the same as in v0.5; R6 moved from 19.7 to 19.5 m/s, R7 from "met by area" to "met, cutting plan drawn", and R10 from $24.14 to $255.56 over (v0.5; v0.4 against the targets before 2026-10-02: 4 met, 5 not met, 2 at risk, 1 not verifiable).

## 10. Limitations

- Pressure coefficients are first-order, not taken from a code for this building shape and exposure. Gust factor, terrain and shelter from neighboring structures are not modeled.
- The frame analysis (section 5) is plane, first order and linear: it covers the middle frame with its eave nodes held across the span, and not tension-only cables, cable slack, second-order sway or the joint stiffness of real sockets. The 1 in post decision is left with the TRL 3 result above; a knee rotation test is TRL 4 work.
- Tarpaulin membrane forces that pull the edge members inward are ignored.
- EMT yield, anchor holding capacity (and the 1.5 kN rating of the long anchors), tensioner, ring and snap hook ratings, the filled nylon price and density, and printed polymer strength at 70 °C are assumed or unknown.
- Costs are indicative and exclude labor, shipping and tooling.
