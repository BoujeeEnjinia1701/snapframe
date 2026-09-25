# SnapFrame

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Situational Field Hardware · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $400 USD · **Difficulty:** 2 of 5

Frame kit of standard EMT conduit joined by printed or cast nodes, with parametric nodes generated for several shelter sizes.

![SnapFrame concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Problem

Emergency shelters need frames that ship flat and go up without tools. Relief agencies stock standard 4 x 6 m tarpaulins, but the frame is usually left to scarce local timber, and purpose-built flat-pack shelters are costly and tied to one supplier. Design with, not for: requirements must come from co-design sessions and field trials with the intended users through a local partner.

## Concept

Frame kit of standard EMT conduit joined by printed or cast nodes, with parametric nodes generated for several shelter sizes.

The reference size M is a 4.0 x 4.0 m (16 m²) gable frame with a 2.6 m ridge: 18 straight 3/4 in EMT tubes, 15 printed nodes with spring-button sockets, cable bracing, hand-turned screw anchors and two standard tarpaulins. It packs into a 2.1 m tube bundle and one bag, about 45 kg in total. First-order estimates: about $437 in parts (9 % over budget; about $387 without tarpaulins) and a wind rating of about 18 m/s with 3/4 in rafters, short of the 20 m/s target. See the [review note](docs/REVIEW.md) for proposed decisions.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- 3/4 in EMT conduit in four cut lengths (1 in rafters proposed)
- Printed polymer nodes in three types, castable in aluminum later
- Spring snap buttons and hitch pins
- Wire-rope brace cables with hand tensioners
- Two 4 x 6 m relief tarpaulins
- Screw ground anchors and guy lines

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> **Safety:** SnapFrame is an emergency shelter frame, not a storm refuge. With 3/4 in rafters it is estimated to stay elastic only up to gusts of about 18 m/s (65 km/h), and it is not rated for snow. Leave the shelter in storms, clear snow and standing water, keep open flames outside (polyethylene tarpaulins burn), and rate the frame for local wind and snow before relying on it.

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
