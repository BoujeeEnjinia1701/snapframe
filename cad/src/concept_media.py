"""SnapFrame concept media from the parametric model (TRL 3).

Run from the repo root:  python cad/src/concept_media.py
Frame geometry comes from cad/src/model.py (size M, 1 in rafters per SNF-DDR-001 and 1 in ridge tubes per SNF-DDR-002).
The tarpaulin skin is shown on the rear bay only so the frame and nodes stay visible;
tarpaulins are agency stock, outside the kit budget (SNF-DDR-001 D1).
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

SIZE = "M"
P = M.SIZES[SIZE]
L = P["bay"] * P["bays"]; W = P["span"]; BAY = P["bay"]
H_EAVE, H_RIDGE = P["eave"], P["ridge"]
YE = W / 2
SKIN_OFF = 60.0

COLORS = {1: "#A8B0B8", 2: "#7C8792", 3: "#A8B0B8", 4: "#A8B0B8", 5: "#0F766E", 6: "#0F766E",
          7: "#0F766E", 8: "#374151", 9: "#B45309", 10: "#D4A017"}
TARP = "#3B6EA5"
LABEL_KEY = {1: (L, -1), 2: (L, -1), 3: 1, 4: (1, -1), 5: (L, -1), 6: (L, -1), 7: L, 8: 3, 9: (L, -1), 10: "front"}
EXTRA = {9: (0, 0, -600), 10: (0, 0, 250)}


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

C = Vector(L / 2, 0, 1300)
K = 0.55


def boff(shape, extra=(0, 0, 0)):
    c = shape.bounding_box().center()
    return tuple(K * (a - b) + e for a, b, e in zip((c.X, c.Y, c.Z), (C.X, C.Y, C.Z), extra))


lengths = M.member_lengths(SIZE)
NAMES = {1: f"EMT post, 3/4 in, {lengths['post'] / 1000:.2f} m", 2: f"EMT rafter, 1 in, {lengths['rafter'] / 1000:.2f} m",
         3: f"EMT ridge tube, 1 in, {lengths['ridge'] / 1000:.2f} m", 4: f"EMT eave tube, 3/4 in, {lengths['eave'] / 1000:.2f} m",
         5: "Foot node with anchor slot", 6: "Eave node", 7: "Ridge node", 8: "Brace cable with hand tensioner",
         9: "Screw ground anchor", 10: "Guy line"}

parts = []
for no, (_, shapes) in M.assembly(SIZE).items():
    for k, sh in shapes.items():
        lead = k == LABEL_KEY[no]
        parts.append(Part(NAMES[no] if lead else f"{NAMES[no]} ({k})", sh, COLORS[no], no if lead else None,
                          boff(sh, EXTRA.get(no, (0, 0, 0)))))
SKIN = "Tarpaulin skin, agency stock (rear bay shown)"
parts.append(Part(SKIN, skin, TARP, 11, (0, 0, 0)))

ground = Pos(L / 2 + 300, -250, -6) * Box(L + 2 * M.GUY_OUT + 1400, W + 1700, 12)
person = human_figure(1750.0, x=L + 600, y=-YE - 500, z=0.0)
person.name = "1.75 m person"
context = [Part("ground patch", ground, "#E7E5E4"), person]

render_all(
    parts, project="SnapFrame", title="Emergency shelter frame kit concept, size M", dwg_no="SNF-DWG-010",
    date="2026-09-25",
    key_figures=["Size M: 4.0 x 4.0 m floor (16 m²), eave 1.8 m, ridge 2.6 m",
                 "18 EMT members: 1 in rafters and ridge, 3/4 in posts and eaves",
                 "15 printed nodes in 4 variants, spring-button sockets, no tools",
                 "Frame kit 42.0 kg, $443 (budget $400); tarpaulins agency stock",
                 "Wind rating 19.7 m/s, 3/4 in post governs (SNF-CAL-001)"],
    cut=False, scale_figure=False, context=context,
)

_render([p for p in parts if p.name != SKIN], ROOT / "media" / "exploded.png", offsets=True, labels=True,
        title="SnapFrame: exploded view (skin, item 11, not shown)", size=(10, 6))
