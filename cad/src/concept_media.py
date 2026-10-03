"""SnapFrame concept media from the parametric model (TRL 3).

Run from the repo root:  python cad/src/concept_media.py
Frame geometry comes from cad/src/model.py (size M, 1 in rafters per SNF-DDR-001 and 1 in ridge tubes per SNF-DDR-002,
constructable design per SNF-DDR-003: cable bolts with rings, cables clipped to rings and anchor eyes).
The tarpaulin skin is shown on the rear bay and on the front gable (part of a third tarpaulin, cut to include a door flap
shown rolled up, decided 2026-10-02) so the frame and nodes stay visible between them; tarpaulins are agency stock, outside
the kit budget (SNF-DDR-001 D1). Cutting plan: cad/src/skin_plan.py.
CONCEPT, NOT FOR FABRICATION.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build123d import Box, Pos, Vector, Wire, Face, Solid
from concept import Part, render_all, human_figure, _render, ROOT
import model as M
from build123d import Cylinder, Plane  # noqa: F811

SIZE = "M"
P = M.SIZES[SIZE]
L = P["bay"] * P["bays"]; W = P["span"]; BAY = P["bay"]
H_EAVE, H_RIDGE = P["eave"], P["ridge"]
YE = W / 2
SKIN_OFF = 60.0

COLORS = {1: "#A8B0B8", 2: "#7C8792", 3: "#A8B0B8", 4: "#A8B0B8", 5: "#0F766E", 6: "#0F766E",
          7: "#0F766E", 8: "#374151", 9: "#B45309", 10: "#D4A017", 12: "#4B5563", 14: "#111827", 15: "#6D28D9", 16: "#B45309"}
TARP = "#3B6EA5"
EXTRA = {9: (0, 0, -600), 10: (0, 0, 250), 15: (0, 0, 150), 16: (0, 0, -600)}


def panel(pts, normal, t=8.0):
    n = Vector(*normal).normalized()
    ps = [Vector(*p) + n * SKIN_OFF for p in pts]
    return Solid.extrude(Face(Wire.make_polygon(ps, close=True)), n * t)


sl = math.atan2(H_RIDGE - H_EAVE, YE)
skin = (panel([(-80, YE + 150, H_EAVE - 60), (BAY, YE + 150, H_EAVE - 60), (BAY, -40, H_RIDGE + 16), (-80, -40, H_RIDGE + 16)],
              (0, math.sin(sl), math.cos(sl)))
        + panel([(-80, -YE - 150, H_EAVE - 60), (BAY, -YE - 150, H_EAVE - 60), (BAY, 40, H_RIDGE + 16), (-80, 40, H_RIDGE + 16)],
                (0, -math.sin(sl), math.cos(sl)))
        + panel([(0, YE, 10), (BAY, YE, 10), (BAY, YE, H_EAVE), (0, YE, H_EAVE)], (0, 1, 0))
        + panel([(0, -YE, 10), (BAY, -YE, 10), (BAY, -YE, H_EAVE), (0, -YE, H_EAVE)], (0, -1, 0))
        + panel([(0, -YE, 10), (0, YE, 10), (0, YE, H_EAVE), (0, 0, H_RIDGE), (0, -YE, H_EAVE)], (-1, 0, 0)))

# front gable: lower strip with the door flap opening (1.0 x 1.7 m, flap rolled up at the top), and the gable triangle
DOOR_W, DOOR_H = 1000.0, 1700.0
front = panel([(L, -YE, 10), (L, YE, 10), (L, YE, H_EAVE), (L, 0, H_RIDGE), (L, -YE, H_EAVE)], (1, 0, 0))
front = front - Pos(L + SKIN_OFF + 4, 0, 10 + DOOR_H / 2) * Box(40, DOOR_W, DOOR_H)
flap = Solid.make_cylinder(55.0, DOOR_W, Plane(origin=(L + SKIN_OFF + 70.0, -DOOR_W / 2, 10 + DOOR_H + 70.0), z_dir=(0, 1, 0)))
skin = skin + front + flap

C = Vector(L / 2, 0, 1300)
K = 0.55


def boff(shape, extra=(0, 0, 0)):
    c = shape.bounding_box().center()
    return tuple(K * (a - b) + e for a, b, e in zip((c.X, c.Y, c.Z), (C.X, C.Y, C.Z), extra))


lengths = M.member_lengths(SIZE)
NAMES = {1: f"EMT post, 3/4 in, {lengths['post'] / 1000:.2f} m", 2: f"EMT rafter, 1 in, {lengths['rafter'] / 1000:.2f} m",
         3: f"EMT ridge tube, 1 in, {lengths['ridge'] / 1000:.2f} m", 4: f"EMT eave tube, 3/4 in, {lengths['eave'] / 1000:.2f} m",
         5: "Foot node with two anchor slots", 6: "Eave node", 7: "Ridge node", 8: "Brace cable with hand tensioner",
         9: "Screw ground anchor", 10: "Guy line", 12: "Snap buttons, hitch pins and caps", 14: "Cable bolt set and ring",
         15: "Folding step", 16: "Long screw anchor, rear corner (560 mm)"}

parts = []
for no, (_, shapes) in M.assembly(SIZE).items():
    if no == 12:
        continue                     # buttons, pins and caps: too small to show at shelter scale
    lead_key = max(shapes, key=lambda kk: shapes[kk].bounding_box().center().X - shapes[kk].bounding_box().center().Y)
    for k, sh in shapes.items():
        lead = k == lead_key
        parts.append(Part(NAMES[no] if lead else f"{NAMES[no]} ({k})", sh, COLORS[no], no if lead else None,
                          boff(sh, EXTRA.get(no, (0, 0, 0)))))
SKIN = "Tarpaulin skin, agency stock (rear bay and front gable with door flap shown)"
parts.append(Part(SKIN, skin, TARP, 11, (0, 0, 0)))

ground = Pos(L / 2 + 300, -250, -6) * Box(L + 2 * M.GUY_OUT + 1400, W + 1700, 12)
person = human_figure(1750.0, x=L + 600, y=-YE - 500, z=0.0)
person.name = "1.75 m person"
context = [Part("ground patch", ground, "#E7E5E4"), person]

render_all(
    parts, project="SnapFrame", title="Emergency shelter frame kit concept, size M", dwg_no="SNF-DWG-010",
    date="2026-10-02",
    key_figures=["Size M: 4.0 x 4.0 m floor (16 m²), eave 1.8 m, ridge 2.6 m",
                 "18 EMT members: 1 in rafters and ridge, 3/4 in posts and eaves",
                 "15 printed nodes in 4 variants (filled PA12-class nylon), no tools; folding step in the kit",
                 "Frame kit 46.2 kg, $701 (value-engineering target $445)",
                 "Wind rating 19.5 m/s, 3/4 in post governs (SNF-CAL-001 v0.6)"],
    cut=False, scale_figure=False, context=context, rev="P2",
)

_render([p for p in parts if p.name != SKIN], ROOT / "media" / "exploded.png", offsets=True, labels=True,
        title="SnapFrame: exploded view (skin, item 11, not shown)", size=(10, 6))
