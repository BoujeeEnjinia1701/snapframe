# SnapFrame

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Situational Field Hardware · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** $400 USD for the frame kit · **Difficulty:** 2 of 5

Frame kit of standard EMT conduit joined by printed or cast nodes, with parametric nodes generated for several shelter sizes.

![SnapFrame concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement (PDF)](cad/drawings/SNF-DWG-001.pdf) · [Calculations](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Problem

Emergency shelters need frames that ship flat and go up without tools. Relief agencies stock standard 4 x 6 m tarpaulins, but the frame is usually left to scarce local timber, and purpose-built flat-pack shelters are costly and tied to one supplier. Design with, not for: requirements must come from co-design sessions and field trials with the intended users through a local partner.

## Concept

Frame kit of standard EMT conduit joined by printed or cast nodes, with parametric nodes generated for several shelter sizes.

The reference size M is a 4.0 x 4.0 m (16 m²) gable frame with a 2.6 m ridge: 18 straight EMT tubes (1 in rafters, 3/4 in elsewhere), 15 printed nodes with spring-button sockets, cable bracing, hand-turned screw anchors, and two standard tarpaulins from agency stock. The TRL 3 calculation note puts the frame kit at about 40.6 kg and $431 (7.8 % over the $400 budget) and the wind rating at about 17.8 m/s, short of the 20 m/s target, with the 3/4 in ridge tubes governing. See the [review note](docs/REVIEW.md) for decisions and open items.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- EMT conduit in four cut lengths: 1 in rafters, 3/4 in posts, ridge and eave tubes
- Printed polymer nodes in three types, castable in aluminum later
- Spring snap buttons and hitch pins
- Wire-rope brace cables with hand tensioners
- Two 4 x 6 m relief tarpaulins (agency stock)
- Screw ground anchors and guy lines

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> **Safety:** SnapFrame is an emergency shelter frame, not a storm refuge. By calculation it stays elastic with a factor of 1.5 only up to gusts of about 17.8 m/s (64 km/h), less with wind blowing into the open gable, and it is not rated for snow. Leave the shelter in storms, clear snow and standing water, keep open flames outside (polyethylene tarpaulins burn), and rate the frame for local wind and snow before relying on it.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (SNF-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `SNF-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
