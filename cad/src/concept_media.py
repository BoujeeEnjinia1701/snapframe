"""SnapFrame concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Reference size M: a 4.0 x 4.0 m gable-roof frame (16 m2 floor) in two 2.0 m bays,
eave 1.8 m, ridge 2.6 m, built from 3/4 in EMT conduit (OD 23.4 mm) joined by printed
nodes with spring-button sockets. Coordinates in mm: X along the ridge, Y across the span,
Z up, ground at Z = 0. The tarpaulin skin is shown on the rear bay only so the frame and
nodes stay visible.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Sphere, Torus, Pos, Rot, Solid, Plane, Vector, Wire, Face
from concept import Part, render_all, human_figure, _render, ROOT

# ---------------- parameters (reference size M) ----------------
L = 4000.0          # length along the ridge
W = 4000.0          # span across the frame
BAY = 2000.0        # frame spacing
H_EAVE = 1800.0     # eave node height
H_RIDGE = 2600.0    # ridge node height
Z_FOOT = 60.0       # foot node center above ground
TUBE_R = 11.7       # 3/4 in EMT, OD 23.4 mm
SOCK_R = 17.0       # node socket OD 34 mm
SOCK_L = 110.0      # socket length from node center
CORE_R = 42.0       # node core radius
TUBE_GAP = 45.0     # tube end sits this far from node center, inside the socket
SKIN_OFF = 60.0     # tarp sits this far outside member centerlines (clears the nodes)

EMT = "#A8B0B8"
NODE = "#0F766E"
TARP = "#3B6EA5"
CABLE = "#374151"
ANCHOR = "#B45309"
ROPE = "#D4A017"

XS = [0.0, BAY, L]
YE = W / 2


def V(*a):
    return Vector(*a)


def rod(a, b, r):
    a = V(*a); b = V(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def member(a, b):
    """EMT tube between two node centers, trimmed so each end sits inside its socket."""
    a = V(*a); b = V(*b); u = (b - a).normalized()
    return rod(a + u * TUBE_GAP, b - u * TUBE_GAP, TUBE_R)


def node(c, dirs, base=False, tab=None):
    """Printed node: spherical core plus one socket per member direction."""
    c = V(*c)
    s = Pos(c.X, c.Y, c.Z) * Sphere(CORE_R)
    for d in dirs:
        u = V(*d).normalized()
        s = s + Solid.make_cylinder(SOCK_R, SOCK_L, Plane(origin=c, z_dir=u))
    if base:  # foot plate with anchor hole boss
        s = s + Pos(c.X, c.Y, 6) * Box(170, 170, 12) + Pos(c.X, c.Y, 22) * Cylinder(30, 20)
    if tab is not None:  # cable or guy tab
        u = V(*tab).normalized()
        s = s + Solid.make_cylinder(9, CORE_R + 30, Plane(origin=c, z_dir=u))
    return s


def panel(pts, normal, t=8.0):
    """Flat tarp panel through the given points, pushed SKIN_OFF along the outward normal."""
    n = V(*normal).normalized()
    ps = [V(*p) + n * SKIN_OFF for p in pts]
    return Solid.extrude(Face(Wire.make_polygon(ps, close=True)), n * t)


def screw_anchor(x, y, top_z=0.0, depth=380.0):
    shaft = rod((x, y, top_z - depth), (x, y, top_z + 40), 7)
    helix = Pos(x, y, top_z - depth + 60) * Cylinder(45, 6)
    eye = Pos(x, y, top_z + 70) * Rot(90, 0, 0) * Torus(28, 6)
    return shaft + helix + eye


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


# ---------------- node positions ----------------
foot = {(x, s): (x, s * YE, Z_FOOT) for x in XS for s in (-1, 1)}
eave = {(x, s): (x, s * YE, H_EAVE) for x in XS for s in (-1, 1)}
ridge = {x: (x, 0.0, H_RIDGE) for x in XS}


def d(a, b):
    return (b[0] - a[0], b[1] - a[1], b[2] - a[2])


# ---------------- members ----------------
posts = {k: member(foot[k], eave[k]) for k in foot}
rafters = {k: member(eave[k], ridge[k[0]]) for k in eave}
ridges = {i: member(ridge[XS[i]], ridge[XS[i + 1]]) for i in range(2)}
eaves = {(i, s): member(eave[(XS[i], s)], eave[(XS[i + 1], s)]) for i in range(2) for s in (-1, 1)}

# ---------------- nodes ----------------
foot_nodes = {k: node(foot[k], [d(foot[k], eave[k])], base=True) for k in foot}
eave_nodes = {}
for (x, s), p in eave.items():
    dirs = [d(p, foot[(x, s)]), d(p, ridge[x])]
    if x > 0:
        dirs.append((-1, 0, 0))
    if x < L:
        dirs.append((1, 0, 0))
    eave_nodes[(x, s)] = node(p, dirs, tab=(0, s, -1))
ridge_nodes = {}
for x, p in ridge.items():
    dirs = [d(p, eave[(x, -1)]), d(p, eave[(x, 1)])]
    if x > 0:
        dirs.append((-1, 0, 0))
    if x < L:
        dirs.append((1, 0, 0))
    ridge_nodes[x] = node(p, dirs, tab=(1 if x == L else -1, 0, 0.4) if x in (0.0, L) else None)

# ---------------- cable bracing (4 mm wire rope with hand tensioners) ----------------
CR = 3.0
cables = []
# rear gable (x = 0): X brace between foot and opposite eave
cables += [rod(foot[(0.0, -1)], eave[(0.0, 1)], CR), rod(foot[(0.0, 1)], eave[(0.0, -1)], CR)]
# side walls: one diagonal per bay each side
for s in (-1, 1):
    cables += [rod(foot[(0.0, s)], eave[(BAY, s)], CR), rod(foot[(L, s)], eave[(BAY, s)], CR)]
# roof planes: one diagonal per bay each side
for s in (-1, 1):
    cables += [rod(eave[(0.0, s)], ridge[BAY], CR), rod(eave[(L, s)], ridge[BAY], CR)]

# ---------------- skin: tarpaulin on the rear bay (x 0 to 2000) ----------------
sl = math.atan2(H_RIDGE - H_EAVE, YE)
roof_p = panel([(-80, YE + 150, H_EAVE - 60), (BAY, YE + 150, H_EAVE - 60), (BAY, -40, H_RIDGE + 16), (-80, -40, H_RIDGE + 16)],
               (0, math.sin(sl), math.cos(sl)))
roof_m = panel([(-80, -YE - 150, H_EAVE - 60), (BAY, -YE - 150, H_EAVE - 60), (BAY, 40, H_RIDGE + 16), (-80, 40, H_RIDGE + 16)],
               (0, -math.sin(sl), math.cos(sl)))
wall_p = panel([(0, YE, 10), (BAY, YE, 10), (BAY, YE, H_EAVE), (0, YE, H_EAVE)], (0, 1, 0))
wall_m = panel([(0, -YE, 10), (BAY, -YE, 10), (BAY, -YE, H_EAVE), (0, -YE, H_EAVE)], (0, -1, 0))
gable = panel([(0, -YE, 10), (0, YE, 10), (0, YE, H_EAVE), (0, 0, H_RIDGE), (0, -YE, H_EAVE)], (-1, 0, 0))
skin = roof_p + roof_m + wall_p + wall_m + gable

# ---------------- ground anchors and guy lines ----------------
anchors = {k: screw_anchor(foot[k][0], foot[k][1], 0.0) for k in foot}
GUY = 1500.0
anchors["g0"] = screw_anchor(-GUY, 0.0)
anchors["g1"] = screw_anchor(L + GUY, 0.0)
guys = {"rear": rod((0 - 30, 0, H_RIDGE), (-GUY, 0, 70), 4), "front": rod((L + 30, 0, H_RIDGE), (L + GUY, 0, 70), 4)}

# ---------------- assemble parts with BOM numbers ----------------
C = V(L / 2, 0, 1300)
K = 0.55  # exploded view: spread every part away from the frame center


def boff(shape, extra=(0, 0, 0)):
    c = shape.bounding_box().center()
    return tuple(K * (a - b) + e for a, b, e in zip((c.X, c.Y, c.Z), (C.X, C.Y, C.Z), extra))


parts = []


def add(name, shapes, color, bom, label_key, extra=(0, 0, 0)):
    """One Part per instance; the BOM number and callout go on one clearly visible instance."""
    for k, sh in shapes.items():
        parts.append(Part(name if k == label_key else f"{name} ({k})", sh, color,
                          bom if k == label_key else None, boff(sh, extra)))


add("EMT post, 1.65 m", posts, EMT, 1, (L, -1))
add("EMT rafter, 2.06 m", rafters, EMT, 2, (L, -1))
add("EMT ridge tube, 1.91 m", ridges, EMT, 3, 1)
add("EMT eave tube, 1.91 m", eaves, EMT, 4, (1, -1))
add("Foot node with anchor plate", foot_nodes, NODE, 5, (L, -1))
add("Eave node", eave_nodes, NODE, 6, (L, -1))
add("Ridge node", ridge_nodes, NODE, 7, L)
add("Brace cable with hand tensioner", {i: c for i, c in enumerate(cables)}, CABLE, 8, 3)
add("Screw ground anchor", anchors, ANCHOR, 9, (L, -1), extra=(0, 0, -600))
add("Guy line", guys, ROPE, 10, "front", extra=(0, 0, 250))
SKIN = "Tarpaulin skin (rear bay shown)"
parts.append(Part(SKIN, skin, TARP, 11, (0, 0, 0)))

# Hero context: ground patch and a 1.75 m person at the open front corner
ground = Pos(L / 2 + 300, -250, -6) * Box(L + 2 * GUY + 1400, W + 1700, 12)
person = human_figure(1750.0, x=L + 600, y=-YE - 500, z=0.0)
person.name = "1.75 m person"
context = [Part("ground patch", ground, "#E7E5E4"), person]

render_all(
    parts, project="SnapFrame", title="Emergency shelter frame kit concept, size M", dwg_no="SNF-DWG-010",
    key_figures=["Size M: 4.0 x 4.0 m floor (16 m²), eave 1.8 m, ridge 2.6 m",
                 "18 EMT members, 3/4 in (OD 23.4 mm), longest 2.06 m",
                 "15 printed nodes, spring-button sockets, no tools",
                 "Skin: two 4 x 6 m tarpaulins (48 m²; full enclosure about 51 m²)",
                 "Kit about 45 kg, parts about $437; wind about 18 m/s (estimates)"],
    cut=False, scale_figure=False, context=context,
)

# Exploded view without the skin, which would hide the frame parts; the skin (BOM 11) is shown
# in the hero render, the blueprint sheet and the 3D model instead.
_render([p for p in parts if p.name != SKIN], ROOT / "media" / "exploded.png", offsets=True, labels=True,
        title="SnapFrame: exploded view (skin, item 11, not shown)")
