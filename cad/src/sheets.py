"""SnapFrame general arrangement drawing SNF-DWG-001 Rev P2 (TRL 3).

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
work = ROOT / "cad" / "drawings" / "_views"

asm = M.assembly("M")
frame = Compound(children=[sh for no, (_, shapes) in asm.items() if no != 9 for sh in shapes.values()])
views = project_views(frame, work / "frame")
var = M.node_variants("M")
nodes = {n: project_views(var[n][0], work / n) for n in ("eave", "ridge-end", "foot")}

ml = M.member_lengths("M")
p = M.SIZES["M"]
s = Sheet(project="SnapFrame", title="General arrangement, size M", dwg_no="SNF-DWG-001", rev="P2",
          author="Amish Chadha", date=DATE, scale=1 / 50,
          material="EMT to ANSI C80.3; printed polymer nodes (not chosen); see bom/bom.csv and SNF-CAL-001",
          revisions=[("P1", "Preliminary general arrangement (TRL 3)", DATE, "AC"),
                     ("P2", "1 in ridge tubes; one eave node variant (DDR-002)", DATE, "AC")])
s.add_ortho(views, ["front", "top", "right"])
s._layers.append(_t(16, 27, "PRELIMINARY, NOT FOR FABRICATION. Anchors omitted from views; guy lines shown.", 2.4, 400, MUTED))

s.add_svg(views["iso"], 268, 26, 150, 62, label="Isometric view", sublabel="Not to scale")
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
    f"Button hole {M.NODE['button_d']:.0f} mm at {M.NODE['button_at']:.0f} mm from tube end; "
    f"pin hole {M.NODE['pin_d']:.0f} mm at {M.NODE['pin_at']:.0f} mm (feet, eave posts)",
    f"Foot plate {M.NODE['plate']:.0f} x {M.NODE['plate']:.0f} x {M.NODE['plate_t']:.0f} mm, "
    f"anchor slot {M.NODE['slot_w']:.0f} mm, anchor {M.NODE['anchor_off']:.0f} mm outboard",
    f"Guy anchors {M.GUY_OUT / 1000:.1f} m beyond each gable; 10 brace cables, 4 mm",
    "Wind rating 19.7 m/s at SF 1.5 (post governs); not rated for snow",
    "Corner eave nodes: socket past the gable left blank and capped",
], x=268, y=150, width=150)
s.save(ROOT / "cad" / "drawings" / "SNF-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/SNF-DWG-001.svg, .pdf, .png")
