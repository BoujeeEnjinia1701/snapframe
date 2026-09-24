# SnapFrame

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Situational Field Hardware · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $400 USD · **Difficulty:** 2 of 5

Frame kit of standard EMT conduit joined by printed or cast nodes, with parametric nodes generated for several shelter sizes.

## Problem

Emergency shelters need frames that ship flat and go up without tools.

## Concept

Frame kit of standard EMT conduit joined by printed or cast nodes, with parametric nodes generated for several shelter sizes.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- 3/4 in EMT conduit
- Nylon or aluminum nodes
- Tarp or fabric skin
- Ground anchors

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Rate the frame for local wind and snow loads before relying on it for shelter.

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
