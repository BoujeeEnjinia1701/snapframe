"""SnapFrame general arrangement drawing SNF-DWG-001 Rev P5 (TRL 3, constructable design, SNF-DDR-003, decisions of 2026-10-02).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/SNF-DWG-001.svg, .pdf and .png. Geometry from cad/src/model.py.
PRELIMINARY, NOT FOR FABRICATION.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(ROOT / "cad" / "src"))
from build123d import Compound, Pos
from drawing import Sheet, project_views, _t, INK, MUTED
import model as M

DATE = "2026-09-25"
DATE_P4 = "2026-10-01"
DATE_P5 = "2026-10-02"
work = ROOT / "cad" / "drawings" / "_views"

asm = M.assembly("M")
frame = Compound([sh for no, (_, shapes) in asm.items() if no not in (9, 12, 15, 16) for sh in shapes.values()])
views = project_views(frame, work / "frame")
var = M.node_variants("M")
bolt = {"eave": M.cable_bolt(M.V(*M.BOLT_DIR["eave"])), "ridge-end": M.cable_bolt(M.V(*M.BOLT_DIR["ridge"]))}
nodes = {n: project_views(Compound([var[n][0]] + ([bolt[n]] if n in bolt else [])), work / n)
         for n in ("eave", "ridge-end", "foot")}

ml = M.member_lengths("M")
p = M.SIZES["M"]
s = Sheet(project="SnapFrame", title="General arrangement, size M", dwg_no="SNF-DWG-001", rev="P5",
          author="Amish Chadha", date=DATE_P5, scale=1 / 50,
          material="EMT to ANSI C80.3; nodes printed in filled PA12-class nylon; see bom/bom.csv and SNF-CAL-001",
          revisions=[("P1", "Preliminary general arrangement (TRL 3)", DATE, "AC"),
                     ("P2", "1 in ridge tubes; one eave node variant (DDR-002)", DATE, "AC"),
                     ("P3", "Layout and labels tidied", DATE, "AC"),
                     ("P4", "Design for construction (DDR-003): cable bolts, slots, pin", DATE_P4, "AC"),
                     ("P5", "Folding step, long rear anchors, filled nylon nodes; 19.5 m/s (CAL v0.6)", DATE_P5, "AC")])
s.add_ortho(views, ["front", "top", "right"])

s.add_svg(views["iso"], 268, 50, 150, 40, label="Isometric view", sublabel="Not to scale")
x0 = 268
for i, (n, title, item) in enumerate([("eave", "Eave node, all six", 6), ("ridge-end", "Ridge node, end", 7),
                                       ("foot", "Foot node", 5)]):
    s.add_svg(nodes[n]["iso"], x0 + i * 51, 104, 46, 34, label=f"{title} ({item})", sublabel="Detail, not to scale")

s.add_notes("Key dimensions and data (size M)", [
    f"Floor {p['span'] / 1000:.1f} x {p['bay'] * p['bays'] / 1000:.1f} m, bays {p['bays']} x {p['bay'] / 1000:.1f} m; "
    f"eave {p['eave'] / 1000:.1f} m, ridge {p['ridge'] / 1000:.1f} m (node centers)",
    f"Cut lengths: post {ml['post']:.0f}, rafter {ml['rafter']:.0f}, ridge and eave {ml['eave']:.0f} mm",
    "Tubes: 1 in EMT rafters and ridge (OD 29.5 mm); 3/4 in EMT posts and eaves (OD 23.4 mm)",
    f"Sockets: {M.NODE['sock_l'] - M.NODE['tube_gap']:.0f} mm engagement, bore = tube OD + "
    f"{M.NODE['clear']:.1f} mm, wall {M.NODE['wall']:.0f} mm; core {2 * M.NODE['core_r']:.0f} mm",
    f"Button hole {M.NODE['button_d']:.0f} mm at {M.NODE['button_at']:.0f} mm from tube end, in a "
    f"{M.NODE['recess_d']:.0f} mm finger recess; pin hole {M.NODE['pin_d']:.0f} mm at {M.NODE['pin_at']:.0f} mm",
    f"Foot plate {M.NODE['plate']:.0f} x {M.NODE['plate']:.0f} x {M.NODE['plate_t']:.0f} mm, two "
    f"{M.NODE['slot_w']:.0f} mm anchor slots at 45 deg; anchor eye down on the plate",
    "Eave and ridge nodes: M10 cable bolt with spacer and 6 mm ring; cables clip to rings and anchor eyes",
    f"Guy anchors {M.GUY_OUT / 1000:.1f} m beyond each gable; 10 brace cables, 4 mm",
    "Wind rating 19.5 m/s at SF 1.5 (post governs, frame analysis); not rated for snow",
    "Corner eave nodes: socket past the gable left blank and capped",
    "Folding step (15) and two 560 mm rear anchors (16) not drawn",
], x=268, y=150, width=150)
s.save(ROOT / "cad" / "drawings" / "SNF-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/SNF-DWG-001.svg, .pdf, .png")
