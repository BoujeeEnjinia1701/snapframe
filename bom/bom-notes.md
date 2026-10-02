# BOM notes

Costs are indicative prototype prices for one size M kit (September 2026 estimates), not quotes. Line numbers match the callouts in `media/exploded.png`, Table 1 of SNF-PRC-001 and drawing SNF-DWG-001. Node prices come from the model volumes in SNF-CAL-001 (printed at 55 % effective fill, filament $22/kg plus $1.00 machine time per node).

- Frame kit (every line except item 11): **$469.13**. Value-engineering target: USD 445 (`budget_usd`, a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 469.13 (USD 24.13 over the target). SNF-CAL-001 v0.4 quotes $469.14; the 1 cent difference comes from rounding node prices to the cent here.
- Design for construction (SNF-DDR-003, 2026-10-01) changed the frame kit from $443.32 to $469.13: new line 14, nine cable bolt sets with rings ($23.40); line 8 now has a snap hook at each end, a thimble and clips ($4.20 a cable, was $3.50); lines 5 to 7 repriced from the new node volumes (printed tabs removed, finger recesses and bolt holes added: $4.56 less in all).
- Tarpaulins (item 11, two at $25): $50.00, from agency stock and outside the frame kit (SNF-DDR-001 D1).
- All 14 lines: $519.13.
- Tube is priced per 3.05 m (10 ft) stick, one member per stick: 10 sticks of 3/4 in at $9.00 and 8 sticks of 1 in at $14.00. About 39 % of the tube bought is offcut; accepted for the prototype on US 10 ft stock on 2026-10-02, with 1.50 m posts or 6 m metric stock chosen once the first region's tube source is known (SNF-DEC-001).
- The four push-in caps for the blank corner eave sockets are included in item 12 at no extra line cost.
- Items to confirm when buying (snap button spring length, snap hook gate opening, ring and tensioner ratings, anchor eye size) are listed in the design decisions register, SNF-DEC-001.
- Decided by Amish on 2026-10-02 (SNF-DEC-001): the nodes are printed in a glass- or carbon-filled nylon of the PA12 class, not ASA or PETG, so their print prices and masses are to be re-estimated; the two rear corner feet take longer screw anchors rated for 1.5 kN; a folding step is part of the first prototype's kit; the tubes are packed in two bundles; and the front gable takes part of a third tarpaulin from agency stock, outside the frame kit like the other two. None of these is yet a change to `bom.csv`.
