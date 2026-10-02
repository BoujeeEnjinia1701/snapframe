---
doc_id: SNF-PRB-001
title: SnapFrame problem statement
project: SnapFrame
doc_type: Problem statement
version: "0.7"
status: Draft
date: '2026-10-02'
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
  change: Populate to TRL 2 (problem, users, context, constraints, out of scope, prior work, open questions)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Apply SNF-DDR-001 (budget covers the frame kit, snow and cyclone out of scope); citations checked and deep-linked
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Stronger sources
- version: "0.6"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish ($445, SNF-DDR-002)
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: "First partners decided by Amish on 2026-10-02; IFRC Shelter Research Unit and Field Ready named as first candidates to approach"
---

# SnapFrame problem statement

After a disaster, families need a covered, weather-tight space within days, and the frame that holds up the sheeting is the hard part: it must ship compactly, go up without tools or skilled labor, and survive wind. Standard relief tarpaulins are everywhere; a frame that fits them, built from a steel tube sold in almost every hardware store, is not. Design with, not for: requirements must come from co-design sessions and field trials with the intended users through a local partner.

## The problem

In the first weeks after an earthquake, flood or storm, the most common shelter response is plastic sheeting over whatever frame people can find. The International Federation of Red Cross and Red Crescent Societies (IFRC) shelter kit, for example, provides two 4 x 6 m woven plastic tarpaulins, rope, fixings and tools, but leaves the frame to locally found timber or bamboo ([IFRC and ICRC items catalogue, shelter kit KRELSHEK02](https://itemscatalogue.redcross.int/relief--4/shelter-and-construction-materials--23/shelter-and-construction-kits--104/shelter-kit--KRELSHEK02.aspx)). Where timber is scarce, costly or has been used up, the result is low, sagging shelters that collapse in wind and use the sheeting badly.

Purpose-built alternatives sit at the other extreme:

- **Family tents** are quick to deploy and familiar, but they are single-purpose. The UNHCR family tent gives 16 m² of main floor plus two 3.5 m² vestibules ([UNHCR family tent fact sheet](https://unis.unvienna.org/pdf/factsheets/UNHCR_tent.pdf)), and when the canvas wears out, the poles are rarely reused.
- **Flat-pack shelters** such as Better Shelter give 17.5 m² with a steel frame and rigid panels ([Better Shelter, Relief Housing Unit](https://bettershelter.org/relief-housing-unit-rhu/)). They are robust, but cost far more than a tent, arrive as a large crate and depend on one supplier for spare parts.
- **Improvised steel frames** from electrical metallic tubing (EMT) conduit are already common for event shade and geodesic domes, where tube ends are flattened, drilled and bolted ([Domerama, strut flattening](https://www.domerama.com/fabricating/making-the-struts/geodesic-dome-struts-flattening/)). They are cheap, but each needs a pipe bender, a drill, bolts and spanners on site, and bolted joints loosen.

The gap is a frame kit that uses a globally stocked tube (EMT, made to ANSI C80.3 in North America and to similar metric standards elsewhere), connects with pre-made nodes that lock by hand, ships as a bundle of straight tubes and a box of nodes, and is sized to the tarpaulins that relief agencies already stock. Nodes are generated from parameters so that one design covers several shelter sizes, and can be printed near the response or cast in aluminum at scale.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Displaced household (four to six people) | A covered living space of 3.5 m² or more per person, the Sphere minimum for warm climates ([UNHCR Emergency Handbook, shelter standards](https://emergency.unhcr.org/emergency-assistance/shelter-camp-and-settlement/shelter-and-housing/emergency-shelter-solutions-and-standards)), with standing headroom, up on the first day | Camps, host-family plots, the site of a damaged home; warm to temperate climates in the first release |
| Shelter team of a relief agency or NGO | A kit that fits existing tarpaulin stock, ships densely, can be put up by the family with a short demonstration, and can be counted and repaired | Pre-positioned stock, mixed logistics (truck, pickup, boat) |
| Community builder or local fabricator | Standard tube, printable or castable nodes, open files, no welding | Makerspace, university lab, small foundry or print farm near the response |
| Household moving from emergency to transitional shelter | A frame that can later carry better cladding (timber, corrugated sheet, woven mats) or be reused as a store or shade | The months after the emergency |
| Clinic, school or distribution point | A larger frame (about 24 m²) from the same parts | Temporary public buildings |

## Constraints

- Garage-buildable prototype, concept budget $445 USD for one size M frame kit (approved by Amish, 2026-09-26). Tarpaulins come from agency stock and are costed separately (SNF-DDR-001 D1).
- Members are trade-size EMT conduit, cut to length and drilled only. No bending, flattening or welding.
- No tools on site for erection. Hands only, plus parts of the kit itself (for example, a tube used as a lever to turn a screw anchor).
- Every package that a person carries weighs 25 kg (55 lb) or less (three packages for size M: two tube bundles and a bag, decided 2026-10-02), and no member is longer than about 2.1 m, so the kit fits a pickup bed and a standard pallet.
- Skin is standard relief tarpaulin (4 x 6 m reinforced polyethylene), tied on, not a custom-cut fabric.
- The frame must be understood and erected by people who have not seen it before, with a picture guide and no written language needed.
- Operating range about 0 to 50 °C air temperature, with node surfaces in full sun reaching higher.

## Out of scope

- Snow load (SNF-DDR-001 D7). The first release is for warm and temperate climates; cold-climate winterization needs a heavier frame and is a later variant.
- Cyclone and hurricane rating (SNF-DDR-001 D7). SnapFrame is an emergency shelter, not a storm refuge. Occupants must follow local evacuation guidance.
- Floors, insulation, doors that lock, and sanitation.
- Multi-story use or hanging loads beyond a lamp and a mosquito net.

## Prior work

- **IFRC shelter kit.** Two 4 x 6 m tarpaulins plus rope, fixings and tools; the frame comes from local material ([IFRC and ICRC items catalogue](https://itemscatalogue.redcross.int/relief--4/shelter-and-construction-materials--23/shelter-and-construction-kits--104/shelter-kit--KRELSHEK02.aspx)). SnapFrame is sized so the same two tarpaulins cover the roof, both side walls and one gable.
- **UNHCR family tent.** 16 m² main floor plus two 3.5 m² vestibules, canvas over poles, for a family of five ([UNHCR family tent fact sheet](https://unis.unvienna.org/pdf/factsheets/UNHCR_tent.pdf)). SnapFrame size M matches the main floor area.
- **Better Shelter (Relief Housing Unit).** 17.5 m², steel frame, polymer panels, supplied as a flat pack; panels are rated for at least three years and the frame for at least ten ([Better Shelter](https://bettershelter.org/relief-housing-unit-rhu/)). It shows that a flat-pack frame works in the field, and that fire performance of the cladding must be addressed early; Zurich set the units aside over fire concerns in 2015 ([Humanosphere](https://www.humanosphere.org/basics/2015/12/ikea-shelters-fail/)).
- **EMT geodesic domes and shade structures.** Widely built by hobbyists and event crews from EMT with flattened, drilled and bolted ends ([Domerama](https://www.domerama.com/fabricating/making-the-struts/geodesic-dome-struts-flattening/)). They prove the tube is available, cheap and strong enough for light cladding, and show the weakness of site-drilled, bolted joints.
- **MERO space frame.** Max Mengeringhausen's tube construction method from the end of the 1930s builds structures from industrially prefabricated series elements ([MERO](https://mero.de/en/the-company/)): tubular rods screwed into near-spherical node pieces ([EP0475216B1, MERO Raumstruktur](https://patents.google.com/patent/EP0475216B1/de)). SnapFrame applies the same principle at family-shelter scale, with hand-locking joints in place of screwed ones.
- **Tent pole snap buttons.** Spring-loaded buttons that pop into a hole to lock two tubes, as used in camping gear and walking aids. SnapFrame uses the same part at every tube end.
- **Wind loading.** Design pressures follow the method of ASCE/SEI 7 ([ASCE](https://www.asce.org)) at first order: dynamic pressure q = ½ρv² times a pressure coefficient.

## Open questions

- Which partner and region to design with first (an IFRC national society shelter team, an NGO with a print farm, or a university humanitarian engineering group)? Decided 2026-10-02: the first candidate to approach is the IFRC Shelter Research Unit, for a technical review of the kit with standard relief tarpaulins, with Field Ready as the printing partner; the region is taken from the first warm-climate response the review points to. Nothing is agreed (SNF-DEC-001).
- Tarpaulins come from agency stock (decided, SNF-DDR-001 D1). Do partner agencies stock a fire-retardant tarpaulin (R13)?
- Nodes are printed for the prototype and designed for casting later (decided, SNF-DDR-001 D3). Which polymer, and are printed nodes acceptable to a partner for a first field trial?
- The frame is rated at about 19.7 m/s by calculation with 1 in ridge tubes (SNF-CAL-001 v0.2, SNF-DDR-002 D8), just below the 20 m/s target. What rating do partners need, and what is the procedure above it (drop the skin, add guys, evacuate)?
- Is metric EMT or other thin-wall steel tube of similar diameter stocked in the target region, and at what price?

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate floor area, headroom, erection time, wind exposure and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design
