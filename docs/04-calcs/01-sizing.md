---
doc_id: SNF-CAL-001
title: SnapFrame sizing calculations
project: SnapFrame
doc_type: Calculation
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First sizing note for TRL 3 (geometry, wind, bracing, anchors, joints, mass, packages, cost, skin, erection time)
---

# SnapFrame sizing calculations

With the decisions in SNF-DDR-001 (1 in EMT rafters, 3/4 in EMT elsewhere, tarpaulins from agency stock), the size M frame meets its floor, headroom, size-family and mass targets, but five of thirteen requirements are **not met**: wind (R6), packages (R5), skin (R7), cost (R10) and fire (R13). The main finding is that a first-principles load share puts more wind load on the ridge tubes and posts than the TRL 2 estimate did, so the 1 in rafters alone do not reach the 20 m/s target: the frame is rated at about **17.8 m/s** (64 km/h, 40 mph), governed by the 3/4 in ridge tubes. The frame kit costs about **$431** against the $400 budget, and the tube bundle weighs about **27.4 kg** against the 25 kg package limit.

Every number in this note is printed by `docs/04-calcs/sizing.py` (run from the repo root). Geometry, cut lengths and node volumes come from the parametric model `cad/src/model.py`, so the note, the model, drawing SNF-DWG-001 and `bom/bom.csv` agree. This is a first-order hand calculation, not a code check or a frame analysis.

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
| A2 | 1 in EMT | OD 29.54 mm (1.163 in), wall 1.448 mm (0.057 in) | As A1 |
| A3 | Steel yield strength | 275 MPa (40 ksi) | Assumed; C80.3 does not set a yield, so confirm from supplier data |
| A4 | Design gust, safety factor | 20 m/s, 1.5 on yield | R6 |
| A5 | Air density | 1.225 kg/m³ | Sea level, 15 °C |
| A6 | Pressure coefficients | Windward wall +0.8, leeward wall -0.5, roof -0.7 on both slopes, net of internal pressure for a closed shelter | First-order values in the style of ASCE/SEI 7; not a code check |
| A7 | Open gable sensitivity | Internal pressure +0.55 when the wind blows into the open gable | Partially enclosed building value in the style of ASCE/SEI 7 |
| A8 | Panel load share | 45° tributary lines from each panel corner: triangles on the short edges, trapezoids on the long edges | Usual two-way rule for a panel tied on four edges |
| A9 | Members | Simply supported between node centers; node fixity ignored | Conservative for bending |
| A10 | Bracing | Tension-only cables; the rear gable is the only braced frame across the span; the roof and side walls carry the rest to it | Concept bracing layout (SNF-PRC-001) |
| A11 | Wire rope | 4 mm 7x19 galvanized, minimum breaking load 8.0 kN | Typical catalog value, unverified |
| A12 | Printed nodes | Density 1,070 kg/m³, 55 % effective fill, filament $22/kg plus $1.00 machine time per node | ASA-class polymer, estimate; polymer not chosen |
| A13 | Tarpaulins | Two 4 x 6 m, 190 g/m², $25 each, from agency stock | Relief tarpaulin class; outside the kit budget (SNF-DDR-001 D1) |
| A14 | Tube prices | 3.05 m (10 ft) stick: 3/4 in $9.00, 1 in $14.00 | Indicative US retail, not quotes |

## 3. Geometry

The size M floor is 4.0 x 4.0 m (16.0 m²), room for 4.6 people at the Sphere minimum of 3.5 m² each. The roof pitch is 21.8°. Taking the underside of the 1 in rafter, the roof is 2.0 m or higher over the central 2.92 m of the 4.0 m span, which is **73 %** of the floor (R2 needs 60 %).

Table 2. Cut lengths from the model (node-center distance less 45 mm at each end).

| Size | Floor | Post | Rafter | Ridge and eave |
| --- | --- | --- | --- | --- |
| S | 3.0 x 3.0 m (9.0 m²) | 1.650 m | 1.526 m | 1.410 m |
| M | 4.0 x 4.0 m (16.0 m²) | 1.650 m | 2.064 m | 1.910 m |
| L | 4.0 x 6.0 m (24.0 m²) | 1.650 m | 2.064 m | 1.910 m |

The model generates the node set of each size (six printed variants per size) and exports each as STL, so R3 is met at model level. M and L share every tube length.

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
| Ridge tube | 3/4 in | 106.2 N·m | 232 MPa | **1.18** | **Below** |
| Post (windward) | 3/4 in | 86.0 N·m | 188 MPa | **1.46** | **Below** |
| Eave tube, windward side | 3/4 in | 68.0 N·m | 149 MPa | 1.85 | Meets |
| Eave tube, leeward side | 3/4 in | 80.9 N·m | 177 MPa | 1.55 | Meets |
| End rafter, wind on the rear gable | 1 in | 134.3 N·m | 157 MPa | 1.75 | Meets |

Stress scales with the square of wind speed, so the rating is the speed at which the weakest member reaches a factor of 1.5.

Table 5. Wind rating and sensitivity.

| Case | Rating at factor 1.5 | Governing member |
| --- | --- | --- |
| **As decided: 1 in rafters, 3/4 in elsewhere** | **17.8 m/s (64 km/h, 40 mph)** | Ridge tube, 1.18 at 20 m/s |
| TRL 2 concept, 3/4 in throughout | 15.4 m/s | Rafter, 0.89 at 20 m/s |
| 1 in rafters and ridge tubes | 19.7 m/s | Post, 1.46 at 20 m/s |
| 1 in rafters, ridge tubes and posts | 20.3 m/s | Eave tube (leeward), 1.55 at 20 m/s |
| As decided, open gable facing the wind (internal pressure +0.55) | 13.3 m/s | Ridge tube, 0.66 at 20 m/s |

For comparison, the TRL 2 method (half of each panel, uniform) gives 99 N·m and 218 MPa in a 3/4 in rafter, which matches SNF-PRC-001 v0.2; that method understated the midspan moment. The open gable case matters: with the door end facing the wind, internal pressure adds to the roof suction and the rating falls to about 13 m/s. Closing the front gable (R7, still open) or dropping the skin in strong wind removes this case.

Snow is out of scope (SNF-DDR-001 D7). As a check for the safety note, 0.5 kPa of snow on plan puts 356 N·m and 416 MPa into a middle 1 in rafter, well past yield.

## 6. Bracing, anchors and joints

Wind across the span puts 2,217 N on the two side walls; about 1,108 N reaches eave level. With the rear gable as the only braced frame across the span, its active X cable carries **1,209 N** and pulls up on its foot with 482 N. The roof acts as a cantilever from the rear gable; the resulting couple of 2,217 N·m puts 554 N into each side wall, 735 N into a side wall cable and another 482 N of uplift at its foot. Wind along the ridge on the closed rear gable (1,678 N) puts 556 N into a side wall cable. The highest cable tension is 1.2 kN, a factor of 6.6 on the assumed 8.0 kN breaking load of 4 mm wire rope; the hand tensioner rating is unknown.

Roof suction lifts the middle frame with 1,372 N against 110 N of its own weight, so each middle foot anchor sees **0.63 kN** and each end foot 0.32 kN. At a rear corner foot, the gable cable and the side wall cable both pull up as well: 0.32 + 0.48 + 0.48 = **1.28 kN** before cable pretension, above the 1.0 kN target in R8.

At that foot the hitch pin bears on the polymer socket at 16.0 MPa, or **32.0 MPa** with the factor of 2 in R9, and on the EMT wall at 64 MPa. The EMT shear-out capacity behind the pin hole is about 37.8 kN, so the steel is not the limit; the polymer socket is. A rafter end transfers 198 N of shear into its socket, a nominal bearing pressure of 0.10 MPa over 65 mm of engagement.

## 7. Nodes, mass, packages and cost

Table 6. Printed nodes, size M, from the model volumes.

| Node | Count | Solid volume | Printed mass | Cost each |
| --- | --- | --- | --- | --- |
| Foot | 6 | 717.3 cm³ | 422 g | $10.29 |
| Eave, corner (right and left hand) | 2 + 2 | 427.3 cm³ | 251 g | $6.53 |
| Eave, middle | 2 | 461.1 cm³ | 271 g | $6.97 |
| Ridge, end | 2 | 436.6 cm³ | 257 g | $6.65 |
| Ridge, middle | 1 | 463.4 cm³ | 273 g | $7.00 |

The 15 nodes weigh 4.87 kg and cost about $122. Corner eave nodes are handed, so a size M kit prints six node variants in three families.

Table 7. Mass and packages, size M.

| Item | Mass |
| --- | --- |
| Tubes (33.74 m) | 26.97 kg |
| Nodes | 4.87 kg |
| Brace cables (31.1 m node to node) and tensioners | 3.22 kg |
| Screw anchors | 3.60 kg |
| Guy lines | 0.28 kg |
| Buttons and hitch pins | 0.72 kg |
| Straps and bag | 1.00 kg |
| **Frame kit** | **40.6 kg (90 lb)** |
| Tarpaulins, agency stock | 9.1 kg |
| **With tarpaulins** | **49.8 kg** |

The tube bundle weighs **27.4 kg** and takes about 0.029 m³; the bag weighs 13.3 kg (22.4 kg with the tarpaulins) and holds about 0.055 m³ of parts before the tarpaulins. Splitting the tubes into two bundles (rafters and ridge tubes 15.2 kg; posts and eave tubes 12.1 kg) would keep every package under 25 kg but makes three packages.

Table 8. Cost, size M.

| Item | Cost |
| --- | --- |
| Tubes: 12 sticks of 3/4 in, 6 of 1 in | $192.00 |
| Nodes (15) | $122.09 |
| Brace cables (10) | $35.00 |
| Screw anchors (8) | $32.00 |
| Guy lines (2) | $6.00 |
| Buttons and hitch pins | $24.00 |
| Straps and bag | $20.00 |
| **Frame kit** | **$431.09, 7.8 % over $400** |
| Tarpaulins, agency stock | $50.00 |
| With tarpaulins | $481.09 |

The kit buys 54.9 m of tube and uses 33.7 m, a 39 % offcut.

## 8. Skin and erection time

Full enclosure needs about 51.4 m² (roof with 150 mm overhang 19.4 m², side walls 14.4 m², each gable 8.8 m²); roof, side walls and one gable need 42.6 m². Two 4 x 6 m tarpaulins give 48.0 m², so the front gable stays open.

Erection time is estimated at about **46 min** for two adults: 63 person-minutes of one-person tasks (36 snap joints at 20 s, 8 anchors at 2 min, 10 cables at 1.5 min, skin 20 min) shared by two, plus 14 min of two-person tasks (layout and raising three frames). This is an estimate only; R4 needs a timed trial.

## 9. Results against requirements

Table 9. Requirement status, size M. Not met items first.

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R5 | Ship flat | Longest member 2.064 m; tube bundle 27.4 kg, 0.029 m³; bag 22.4 kg with tarpaulins | 2.1 m or less; two packages, each 25 kg or less and 0.10 m³ or less | **Not met** (tube bundle 2.4 kg over) |
| R6 | Resist wind | Rating 17.8 m/s; ridge tube factor 1.18 and post 1.46 at 20 m/s | Factor 1.5 at 20 m/s | **Not met** |
| R7 | Fit standard tarpaulins | 48.0 m² closes roof, side walls and one gable (42.6 m²); full enclosure 51.4 m² | Both gables closed | **Not met** (front gable open; awaiting Amish) |
| R10 | Stay within budget | Frame kit $431 | $400 or less, frame kit without tarpaulins | **Not met** (7.8 % over) |
| R13 | Limit fire spread | Standard polyethylene tarpaulins | Flame spread test or fire-retardant option | **Not met** |
| R8 | Anchor without a hammer | Demand up to 1.28 kN at a rear corner foot, before pretension | Each anchor holds 1.0 kN | **At risk** (demand above target; capacity not verifiable at TRL 3) |
| R9 | Nodes strong in sun and cold | Pin bearing 32.0 MPa with the factor of 2 | Factor 2 after two years, -10 to 70 °C | **At risk** (polymer not chosen; close to typical printed ASA strength at room temperature, lower at 70 °C) |
| R12 | Repairable in the field | 4 tube types; 3 node families in 6 printed variants (handed corners) | 4 tube types and 3 node types | **At risk** |
| R4 | Go up without tools | About 46 min estimated | 60 min or less | Not verifiable at TRL 3 |
| R1 | Living space | 16.0 m² (4.6 people at 3.5 m²) | 16 m² or more | Met |
| R2 | Headroom | 73 % of floor at 2.0 m or more | 60 % or more | Met |
| R3 | Several sizes | S, M and L node sets generated and exported | Three sizes from one model | Met |
| R11 | Carried by two people | Frame kit 40.6 kg; 49.8 kg with tarpaulins | 50 kg or less | Met (0.2 kg margin with tarpaulins) |

Summary: 4 met, 5 not met, 3 at risk, 1 not verifiable at TRL 3.

## 10. Limitations

- Pressure coefficients are first-order, not taken from a code for this building shape and exposure. Gust factor, terrain and shelter from neighboring structures are not modeled.
- The frame is checked member by member. No frame analysis with pinned nodes and tension-only cables was run, so buckling of posts under combined axial load and bending, cable slack and second-order sway are not covered.
- Tarpaulin membrane forces that pull the edge members inward are ignored.
- EMT yield, anchor holding capacity, tensioner rating and printed polymer strength at 70 °C are assumed or unknown.
- Costs are indicative and exclude labor, shipping and tooling.
