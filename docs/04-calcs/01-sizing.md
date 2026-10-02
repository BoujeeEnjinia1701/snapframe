---
doc_id: SNF-CAL-001
title: SnapFrame sizing calculations
project: SnapFrame
doc_type: Calculation
version: "0.5"
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
---

# SnapFrame sizing calculations

With the decisions in SNF-DDR-001 and SNF-DDR-002 (1 in EMT rafters and ridge tubes, 3/4 in EMT posts and eave tubes, one eave node variant, tarpaulins from agency stock), the size M frame meets its floor, headroom, size-family and part-count targets, but five of thirteen requirements were **not met** against the targets of v0.4: wind (R6), packages (R5), skin (R7), carried mass (R11) and fire (R13). On 2026-10-02 Amish restated R5 (three packages), R7 (a third tarpaulin for the front gable), R8 (1.5 kN at the rear corner feet) and R11 (frame kit alone) (SNF-DEC-001); against the restated targets only R6 and R13 are not met. A first-principles load share puts more wind load on the ridge tubes and posts than the TRL 2 estimate did. With the 1 in ridge tubes of SNF-DDR-002 the frame is rated at about **19.7 m/s** (71 km/h, 44 mph), up from 17.8 m/s in v0.1, and the 3/4 in posts now govern. The design for construction (SNF-DDR-003, version 0.4 of this note) adds cable bolt sets and second snap hooks: the frame kit is now about **$469**, **$24 over the $445 value-engineering target** (a control target, not a limit; Amish, 2026-10-01), the tube bundle stays at **28.6 kg** against the 25 kg package limit, and the complete kit with tarpaulins is **52.5 kg**, 2.5 kg over the 50 kg carry limit.

Every number in this note is printed by `docs/04-calcs/sizing.py` (run from the repo root). Geometry, cut lengths and node volumes come from the parametric model `cad/src/model.py`, so the note, the model, drawing SNF-DWG-001 and `bom/bom.csv` agree. This is a first-order hand calculation, not a code check or a frame analysis. Version 0.2 reruns the script after SNF-DDR-002; every changed number is noted with its v0.1 value. Version 0.3 changed only the budget, from $400 to $445 (SNF-DDR-002). Version 0.4 reruns the script on the constructable model of SNF-DDR-003: the hitch pin moves to 15 mm from the tube end, the cables run between their real attachment points (anchor eyes and cable bolt rings), the cable bolt is checked, and the masses and costs of the new parts are added. Every changed number gives its v0.3 value. The budget is reported as a value-engineering target, as Amish set out on 2026-10-01.

## 1. Method

1. Build the size M geometry from the model parameters: 4.0 x 4.0 m floor, two 2.0 m bays, eave nodes at 1.8 m, ridge nodes at 2.6 m, foot node centers 60 mm above ground.
2. Compute section properties of 3/4 in and 1 in EMT from the nominal ANSI C80.3 diameters and walls.
3. Apply a gust dynamic pressure to the skin, share each tarpaulin panel's load between its four edge members with 45° tributary lines, and check each member as simply supported between node centers.
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
| A9 | Members | Simply supported between node centers; node fixity ignored | Conservative for bending |
| A10 | Bracing | Tension-only cables; the rear gable is the only braced frame across the span; the roof and side walls carry the rest to it | Concept bracing layout (SNF-PRC-001) |
| A11 | Wire rope | 4 mm 7x19 galvanized, minimum breaking load 8.0 kN | Typical catalog value, unverified |
| A12 | Printed nodes | Density 1,070 kg/m³, 55 % effective fill, filament $22/kg plus $1.00 machine time per node | ASA-class polymer, estimate; glass- or carbon-filled PA12-class nylon chosen on 2026-10-02 (SNF-DEC-001), not yet re-estimated |
| A13 | Tarpaulins | Two 4 x 6 m, 190 g/m², $25 each, from agency stock | Relief tarpaulin class; outside the frame kit cost (SNF-DDR-001 D1) |
| A14 | Tube prices | 3.05 m (10 ft) stick: 3/4 in $9.00, 1 in $14.00 | Indicative US retail, not quotes |
| A15 | Corner eave nodes | The four-socket eave node with the socket past the gable left blank and capped | SNF-DDR-002 D9 |
| A16 | Cable bolt | M10 stainless A4-70 (yield 450 MPa), load applied at the ring 9.5 mm from the spot face, both cables of a rear corner eave node added at full value | SNF-DDR-003 C3; conservative upper bound |
| A17 | Cable bolt sets and second snap hooks | 0.13 kg and $2.60 a set; cable assembly $4.20 and 0.17 kg of fittings | Indicative catalog values |

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

Table 5. Wind rating and sensitivity.

| Case | Rating at factor 1.5 | Governing member |
| --- | --- | --- |
| **As decided: 1 in rafters and ridge tubes, 3/4 in posts and eave tubes (SNF-DDR-002 D8)** | **19.7 m/s (71 km/h, 44 mph)** | Post, 1.46 at 20 m/s |
| TRL 2 concept, 3/4 in throughout | 15.4 m/s | Rafter, 0.89 at 20 m/s |
| SNF-DDR-001 only: 1 in rafters, 3/4 in elsewhere (v0.1 baseline) | 17.8 m/s | Ridge tube, 1.18 at 20 m/s |
| 1 in rafters, ridge tubes and posts | 20.3 m/s | Eave tube (leeward), 1.55 at 20 m/s |
| As decided, open gable facing the wind (internal pressure +0.55) | 14.7 m/s (13.3 m/s in v0.1) | Eave tube (leeward), 0.81 at 20 m/s |

For comparison, the TRL 2 method (half of each panel, uniform) gives 99 N·m and 218 MPa in a 3/4 in rafter, which matches SNF-PRC-001 v0.2; that method understated the midspan moment. The open gable case matters: with the door end facing the wind, internal pressure adds to the roof suction and the wall suction, and the rating falls to about 14.7 m/s. Whether the posts also move to 1 in waits for a frame analysis (SNF-DDR-002 D8); on this member-by-member basis 1 in posts would give 20.3 m/s. Closing the front gable (R7, still open) or dropping the skin in strong wind removes this case.

Snow is out of scope (SNF-DDR-001 D7). As a check for the safety note, 0.5 kPa of snow on plan puts 356 N·m and 416 MPa into a middle 1 in rafter, well past yield.

## 6. Bracing, anchors and joints

Wind across the span puts 2,217 N on the two side walls; about 1,108 N reaches eave level. With the rear gable as the only braced frame across the span, its active X cable carries **1,209 N** and pulls up on its foot with 482 N. The roof acts as a cantilever from the rear gable; the resulting couple of 2,217 N·m puts 554 N into each side wall, 735 N into a side wall cable and another 482 N of uplift at its foot. Wind along the ridge on the closed rear gable (1,678 N) puts 556 N into a side wall cable. The highest cable tension is 1.2 kN, a factor of 6.6 on the assumed 8.0 kN breaking load of 4 mm wire rope; the hand tensioner rating is unknown.

Roof suction lifts the middle frame with 1,372 N against 116 N of its own weight, so each middle foot anchor sees **0.63 kN** and each end foot 0.31 kN. At a rear corner foot, the gable cable and the side wall cable both pull up as well: 0.31 + 0.48 + 0.48 = **1.28 kN** before cable pretension, above the 1.0 kN target in R8 and inside the 1.5 kN target set for the two rear corner feet on 2026-10-02 (SNF-DEC-001).

At that foot the hitch pin bears on the polymer socket at 16.0 MPa, or **32.0 MPa** with the factor of 2 in R9, and on the EMT wall at 64 MPa. With the pin hole now 15 mm from the tube end (SNF-DDR-003 C1), the EMT shear-out capacity behind it is about 9.0 kN (37.8 kN at 50 mm in v0.3), seven times the load, so the steel is still not the limit; the polymer socket is. A rafter end transfers 198 N of shear into its socket, a nominal bearing pressure of 0.10 MPa over 65 mm of engagement.

The cables now clip to an M10 cable bolt through each eave and ridge node (SNF-DDR-003 C3). The worst node is a rear corner eave node, which takes the gable cable and a roof cable; taking both at full value together (1,765 N, an upper bound) with the ring 9.5 mm from the spot face gives 16.8 N·m and **171 MPa** in the shank, a factor of **2.6** on A4-70 stainless, and about 5.6 MPa of bearing on the polymer (11.2 MPa with the factor of 2 in R9). The printed tab it replaces would have carried about 46 MPa in bending at the gable cable load alone.

## 7. Nodes, mass, packages and cost

Table 6. Printed nodes, size M, from the model volumes.

| Node | Count | Solid volume | Printed mass | Cost each |
| --- | --- | --- | --- | --- |
| Foot | 6 | 697.3 cm³ | 410 g | $10.03 |
| Eave (all six; corners with one blank socket) | 6 | 434.3 cm³ | 256 g | $6.62 |
| Ridge, end | 2 | 419.3 cm³ | 247 g | $6.43 |
| Ridge, middle | 1 | 461.3 cm³ | 271 g | $6.97 |

The 15 nodes weigh 4.76 kg and cost about $120 (v0.3: 4.97 kg, $124; the printed tabs are gone and the finger recesses, bolt holes and second anchor slot remove a little more). With one eave node variant (SNF-DDR-002 D9), a size M kit prints four node variants in three families, none of them handed; the ridge nodes grow slightly because their ridge sockets now take 1 in tube.

Table 7. Mass and packages, size M.

| Item | Mass |
| --- | --- |
| Tubes (33.74 m) | 28.20 kg |
| Nodes | 4.76 kg (v0.3: 4.97 kg) |
| Brace cables (29.5 m eye to eye), snap hooks and tensioners | 3.62 kg (v0.3: 3.22 kg) |
| Cable bolt sets (9) | 1.17 kg (new) |
| Screw anchors | 3.60 kg |
| Guy lines | 0.28 kg |
| Buttons and hitch pins | 0.72 kg |
| Straps and bag | 1.00 kg |
| **Frame kit** | **43.3 kg (96 lb)** (v0.3: 42.0 kg) |
| Tarpaulins, agency stock | 9.1 kg |
| **With tarpaulins** | **52.5 kg** (v0.3: 51.1 kg) |

The tube bundle weighs **28.6 kg** and takes about 0.030 m³; the bag weighs 14.7 kg (23.9 kg with the tarpaulins) and holds about 0.057 m³ of parts before the tarpaulins. Splitting the tubes into two bundles (rafters and ridge tubes 16.5 kg; posts and eave tubes 12.1 kg) would keep every package under 25 kg but makes three packages; Amish chose this on 2026-10-02 and restated R5 as three packages (SNF-DEC-001). The complete kit with tarpaulins is now 2.5 kg over the 50 kg carry limit of R11 (1.1 kg in v0.3); since 2026-10-02 R11 counts the frame kit alone (43.3 kg), because the tarpaulins are issued separately from agency stock (SNF-DEC-001).

Table 8. Cost, size M.

| Item | Cost |
| --- | --- |
| Tubes: 10 sticks of 3/4 in, 8 of 1 in | $202.00 |
| Nodes (15) | $119.74 (v0.3: $124.30) |
| Brace cables (10) | $42.00 (v0.3: $35.00) |
| Cable bolt sets (9) | $23.40 (new) |
| Screw anchors (8) | $32.00 |
| Guy lines (2) | $6.00 |
| Buttons and hitch pins | $24.00 |
| Straps and bag | $20.00 |
| **Frame kit** | **$469.14** (v0.3: $443.30) |
| Value-engineering target | $445 (a control target, not a limit): **$24.14 over** |
| Tarpaulins, agency stock | $50.00 |
| With tarpaulins | $519.14 |

The kit buys 54.9 m of tube and uses 33.7 m, a 39 % offcut.

## 8. Skin and erection time

Full enclosure needs about 51.4 m² (roof with 150 mm overhang 19.4 m², side walls 14.4 m², each gable 8.8 m²); roof, side walls and one gable need 42.6 m². Two 4 x 6 m tarpaulins give 48.0 m², so the front gable stays open with two. On 2026-10-02 Amish decided to close it with part of a third tarpaulin from agency stock, cut to include a door flap (72 m² in three; SNF-DEC-001).

Erection time is estimated at about **46 min** for two adults: 63 person-minutes of one-person tasks (36 snap joints at 20 s, 8 anchors at 2 min, 10 cables at 1.5 min, skin 20 min) shared by two, plus 14 min of two-person tasks (layout and raising three frames). This is an estimate only; R4 needs a timed trial. The erection order of SNF-DDR-003 C7 (frames slid onto the tube ends, anchors last) uses the same tasks, so the estimate is unchanged.

## 9. Results against requirements

Table 9. Requirement status, size M, against the targets as restated on 2026-10-02.

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R5 | Ship flat | Longest member 2.064 m; tube bundle 28.6 kg, 0.030 m³; bag 23.9 kg with tarpaulins | 2.1 m or less; three packages, each 25 kg or less and 0.10 m³ or less (restated 2026-10-02) | Met (bundles 16.5 and 12.1 kg, bag 14.7 kg without tarpaulins) |
| R6 | Resist wind | Rating 19.7 m/s; post factor 1.46 at 20 m/s | Factor 1.5 at 20 m/s | **Not met** (posts; frame analysis to be run now, 1 in posts if not run before the tubes are bought, decided 2026-10-02) |
| R7 | Fit standard tarpaulins | 48.0 m² closes roof, side walls and one gable (42.6 m²); full enclosure 51.4 m² | Both gables closed, with part of a third tarpaulin for the front gable (restated 2026-10-02) | Met by area (72 m² in three tarpaulins; cutting plan to be drawn) |
| R11 | Carried by two people | Frame kit 43.3 kg; 52.5 kg with tarpaulins | 50 kg or less, frame kit alone (restated 2026-10-02) | Met (43.3 kg) |
| R13 | Limit fire spread | Standard polyethylene tarpaulins | Flame spread test or fire-retardant option | **Not met** |
| R8 | Anchor without a hammer | Demand up to 1.28 kN at a rear corner foot, before pretension | Each anchor holds 1.0 kN; 1.5 kN at the two rear corner feet (raised 2026-10-02) | **At risk** (demand inside the raised target; capacity not verifiable at TRL 3) |
| R9 | Nodes strong in sun and cold | Pin bearing 32.0 MPa with the factor of 2 | Factor 2 after two years, -10 to 70 °C | **At risk** (filled PA12-class nylon chosen on 2026-10-02; coupons to be tested at 70 °C at TRL 4) |
| R4 | Go up without tools | About 46 min estimated | 60 min or less | Not verifiable at TRL 3 |
| R1 | Living space | 16.0 m² (4.6 people at 3.5 m²) | 16 m² or more | Met |
| R2 | Headroom | 73 % of floor at 2.0 m or more | 60 % or more | Met |
| R3 | Several sizes | S, M and L node sets generated and exported | Three sizes from one model | Met |
| R10 | Value-engineering target | Frame kit $469 | $445 value-engineering target, frame kit without tarpaulins | Over the value-engineering target by $24.14 (reported against the target, not as met or not met) |
| R12 | Repairable in the field | 4 tube types; 3 node types in 4 printed variants, none handed | 4 tube types and 3 node types | Met (at risk in v0.1) |

Summary against the targets restated on 2026-10-02: 7 met, 2 not met (R6, R13), 2 at risk, 1 not verifiable at TRL 3, and R10 reported against the value-engineering target; against the v0.4 targets: 4 met, 5 not met, 2 at risk, 1 not verifiable at TRL 3, and R10 reported against the value-engineering target, $24.14 over (v0.3: 5 met with R10 within the $445 budget; v0.2: 4 met, 6 not met, 2 at risk, 1 not verifiable; v0.1: 4 met, 5 not met, 3 at risk, 1 not verifiable).

## 10. Limitations

- Pressure coefficients are first-order, not taken from a code for this building shape and exposure. Gust factor, terrain and shelter from neighboring structures are not modeled.
- The frame is checked member by member. No frame analysis with pinned nodes and tension-only cables was run, so buckling of posts under combined axial load and bending, cable slack and second-order sway are not covered. That analysis is the next TRL 3 step under SNF-DDR-002 D8, before deciding on 1 in posts.
- Tarpaulin membrane forces that pull the edge members inward are ignored.
- EMT yield, anchor holding capacity, tensioner, ring and snap hook ratings and printed polymer strength at 70 °C are assumed or unknown.
- Costs are indicative and exclude labor, shipping and tooling.
