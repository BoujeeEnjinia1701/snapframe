"""SnapFrame parametric model (build123d), TRL 3.

Run from the repo root:  python cad/src/model.py
Exports:
  cad/step/snapframe-M-assembly.step      size M frame assembly (tubes, nodes, cables, anchors, guys)
  cad/step/snapframe-{S,M,L}-nodes.step   every node variant of each size, laid out in a row
  cad/stl/snapframe-{S,M,L}-<node>.stl    printable node variants (massing-plus level, not print-ready)

Massing-plus detail: correct interfaces (socket bores, engagement, button and pin holes,
foot plate anchor slot) and main dimensions; no fillets, print orientation or tolerances
for fabrication. PRELIMINARY, NOT FOR FABRICATION.

Coordinates in mm: X along the ridge, Y across the span, Z up, ground at Z = 0.
Frame lines at X = 0, BAY, 2 BAY, ...; eave nodes at Y = +/- span/2.
"""
from __future__ import annotations
import math
from dataclasses import dataclass, field
from pathlib import Path

from build123d import (Box, Cylinder, Sphere, Torus, Pos, Rot, Solid, Plane, Vector, Compound,
                       export_step, export_stl)

ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Parameters. Edit these, not the geometry below.
# ---------------------------------------------------------------------------
# Tube sections (ANSI C80.3 EMT nominal): OD and wall in mm
TUBES = {
    "3/4": {"od": 23.42, "wall": 1.245},   # 0.922 in OD, 0.049 in wall
    "1":   {"od": 29.54, "wall": 1.448},   # 1.163 in OD, 0.057 in wall
}
TUBE_OF = {"post": "3/4", "rafter": "1", "ridge": "3/4", "eave": "3/4"}   # DDR-001 D2: 1 in rafters

NODE = {
    "core_r": 42.0,        # spherical core radius
    "sock_l": 110.0,       # socket length from node center
    "tube_gap": 45.0,      # tube end sits this far from node center (engagement = sock_l - tube_gap)
    "clear": 0.6,          # diametral clearance, bore = tube OD + clear
    "wall": 5.0,           # socket wall thickness (polymer)
    "button_d": 6.0,       # spring button hole, 25 mm from the tube end
    "button_at": 25.0,
    "pin_d": 8.0,          # hitch pin cross hole at tension joints, 50 mm from the tube end
    "pin_at": 50.0,
    "plate": 170.0,        # foot plate side
    "plate_t": 12.0,
    "z_foot": 60.0,        # foot node center above ground
    "anchor_off": 62.0,    # anchor shaft offset outboard of the foot node center
    "slot_w": 18.0,        # anchor slot width, open to the outer edge of the plate
    "tab_r": 9.0,          # cable or guy tab
}

SIZES = {
    #        span W, bays, bay, eave, ridge
    "S": {"span": 3000.0, "bays": 2, "bay": 1500.0, "eave": 1800.0, "ridge": 2400.0},
    "M": {"span": 4000.0, "bays": 2, "bay": 2000.0, "eave": 1800.0, "ridge": 2600.0},
    "L": {"span": 4000.0, "bays": 3, "bay": 2000.0, "eave": 1800.0, "ridge": 2600.0},
}
GUY_OUT = 1500.0       # guy anchors this far beyond each gable
CABLE_R = 2.0          # 4 mm wire rope
ANCHOR_DEPTH = 380.0


def V(*a):
    return Vector(*a)


def bore_of(kind):
    return TUBES[TUBE_OF[kind]]["od"] + NODE["clear"]


def sock_r_of(kind):
    return bore_of(kind) / 2 + NODE["wall"]


def _perp(u):
    """A unit vector perpendicular to u, horizontal where possible (for cross holes)."""
    ref = V(0, 0, 1) if abs(u.Z) < 0.9 else V(1, 0, 0)
    return u.cross(ref).normalized()


def rod(a, b, r):
    a = V(*a); b = V(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def tube(a, b, kind):
    """Hollow EMT member between two node centers, trimmed to sit inside its sockets."""
    a = V(*a); b = V(*b); u = (b - a).normalized()
    p, q = a + u * NODE["tube_gap"], b - u * NODE["tube_gap"]
    t = TUBES[TUBE_OF[kind]]
    ln = (q - p).length
    outer = Solid.make_cylinder(t["od"] / 2, ln, Plane(origin=p, z_dir=u))
    inner = Solid.make_cylinder(t["od"] / 2 - t["wall"], ln, Plane(origin=p, z_dir=u))
    return outer - inner


@dataclass
class Socket:
    direction: tuple
    kind: str              # member kind, sets the bore
    pinned: bool = False   # hitch pin cross hole (tension joint)


def node(sockets, foot=False, tab=None, outboard=(0, 1, 0)):
    """Printed node at the origin: spherical core, one bored socket per member, optional foot plate and tab."""
    n = NODE
    s = Sphere(n["core_r"])
    cuts = []
    for sk in sockets:
        u = V(*sk.direction).normalized()
        s = s + Solid.make_cylinder(sock_r_of(sk.kind), n["sock_l"], Plane(origin=V(0, 0, 0), z_dir=u))
        # bore from the tube-end stop to the socket mouth
        cuts.append(Solid.make_cylinder(bore_of(sk.kind) / 2, n["sock_l"] - n["tube_gap"] + 1,
                                        Plane(origin=u * n["tube_gap"], z_dir=u)))
        w = _perp(u)
        at_b = u * (n["tube_gap"] + n["button_at"])
        cuts.append(Solid.make_cylinder(n["button_d"] / 2, sock_r_of(sk.kind) + 2, Plane(origin=at_b, z_dir=w)))
        if sk.pinned:
            at_p = u * (n["tube_gap"] + n["pin_at"])
            ln = 2 * sock_r_of(sk.kind) + 4
            cuts.append(Solid.make_cylinder(n["pin_d"] / 2, ln, Plane(origin=at_p - w * (ln / 2), z_dir=w)))
    if foot:
        z0 = -n["z_foot"]
        o = V(*outboard).normalized()
        s = s + Pos(0, 0, z0 + n["plate_t"] / 2) * Box(n["plate"], n["plate"], n["plate_t"])
        s = s + Pos(0, 0, z0 + n["plate_t"] + 20) * Cylinder(30, 40)   # boss joining core to plate
        slot_len = n["plate"] / 2 - n["anchor_off"] + n["slot_w"] / 2 + 1
        c = o * (n["anchor_off"] + slot_len / 2 - n["slot_w"] / 2)
        slot = Box(n["slot_w"] if abs(o.Y) > 0.5 else slot_len, slot_len if abs(o.Y) > 0.5 else n["slot_w"], 40)
        cuts.append(Pos(c.X, c.Y, z0) * slot)
        a = o * n["anchor_off"]
        cuts.append(Pos(a.X, a.Y, z0) * Cylinder(n["slot_w"] / 2, 40))
    if tab is not None:
        u = V(*tab).normalized()
        s = s + Solid.make_cylinder(n["tab_r"], n["core_r"] + 30, Plane(origin=V(0, 0, 0), z_dir=u))
        eye = u * (n["core_r"] + 22)
        cuts.append(Solid.make_cylinder(3.5, 2 * n["tab_r"] + 2,
                                        Plane(origin=eye - _perp(u) * (n["tab_r"] + 1), z_dir=_perp(u))))
    for c in cuts:
        s = s - c
    return s


def screw_anchor(x, y, top_z=20.0, depth=ANCHOR_DEPTH):
    shaft = rod((x, y, top_z - depth), (x, y, top_z + 30), 7)
    helix = Pos(x, y, top_z - depth + 60) * Cylinder(45, 6)
    eye = Pos(x, y, top_z + 58) * Rot(90, 0, 0) * Torus(28, 6)
    return shaft + helix + eye


@dataclass
class Frame:
    size: str
    p: dict
    xs: list
    foot: dict = field(default_factory=dict)
    eave: dict = field(default_factory=dict)
    ridge: dict = field(default_factory=dict)


def geometry(size="M"):
    p = SIZES[size]
    xs = [i * p["bay"] for i in range(p["bays"] + 1)]
    ye = p["span"] / 2
    f = Frame(size, p, xs)
    for x in xs:
        for s in (-1, 1):
            f.foot[(x, s)] = (x, s * ye, NODE["z_foot"])
            f.eave[(x, s)] = (x, s * ye, p["eave"])
        f.ridge[x] = (x, 0.0, p["ridge"])
    return f


def _d(a, b):
    return (b[0] - a[0], b[1] - a[1], b[2] - a[2])


def node_variants(size="M"):
    """Unique node variants of one size, at the origin: {name: (shape, count, [positions])}."""
    f = geometry(size)
    x0, xl, xm = f.xs[0], f.xs[-1], f.xs[1]
    v = {}
    v["foot"] = (node([Socket(_d(f.foot[(x0, 1)], f.eave[(x0, 1)]), "post", True)], foot=True, outboard=(0, 1, 0)),
                 len(f.foot), [f.foot[k] for k in f.foot])
    eave_c = [Socket(_d(f.eave[(x0, 1)], f.foot[(x0, 1)]), "post", True),
              Socket(_d(f.eave[(x0, 1)], f.ridge[x0]), "rafter"), Socket((1, 0, 0), "eave")]
    corner = node(eave_c, tab=(0, 1, -1))
    # corner nodes are handed: R at (first frame, +Y) and (last frame, -Y); L is its mirror image
    v["eave-corner-R"] = (corner, 2, [f.eave[(x0, 1)], f.eave[(xl, -1)]])
    v["eave-corner-L"] = (corner.mirror(Plane.YZ), 2, [f.eave[(xl, 1)], f.eave[(x0, -1)]])
    eave_m = eave_c + [Socket((-1, 0, 0), "eave")]
    v["eave-middle"] = (node(eave_m, tab=(0, 1, -1)), 2 * (len(f.xs) - 2),
                        [f.eave[k] for k in f.eave if k[0] not in (x0, xl)])
    ridge_e = [Socket(_d(f.ridge[x0], f.eave[(x0, -1)]), "rafter"), Socket(_d(f.ridge[x0], f.eave[(x0, 1)]), "rafter"),
               Socket((1, 0, 0), "ridge")]
    v["ridge-end"] = (node(ridge_e, tab=(-1, 0, 0.4)), 2, [f.ridge[x0], f.ridge[xl]])
    v["ridge-middle"] = (node(ridge_e + [Socket((-1, 0, 0), "ridge")]), len(f.xs) - 2,
                         [f.ridge[x] for x in f.xs[1:-1]])
    return v


def _place(shape, at, rot_z=0.0):
    return Pos(*at) * Rot(0, 0, rot_z) * shape


def assembly(size="M"):
    """Frame assembly grouped by BOM item: {bom_no: (name, {key: shape})}."""
    f = geometry(size)
    x0, xl = f.xs[0], f.xs[-1]
    ye = f.p["span"] / 2
    posts = {k: tube(f.foot[k], f.eave[k], "post") for k in f.foot}
    rafters = {k: tube(f.eave[k], f.ridge[k[0]], "rafter") for k in f.eave}
    ridges = {i: tube(f.ridge[f.xs[i]], f.ridge[f.xs[i + 1]], "ridge") for i in range(len(f.xs) - 1)}
    eaves = {(i, s): tube(f.eave[(f.xs[i], s)], f.eave[(f.xs[i + 1], s)], "eave")
             for i in range(len(f.xs) - 1) for s in (-1, 1)}

    var = node_variants(size)
    feet = {k: _place(var["foot"][0], f.foot[k], 0 if k[1] > 0 else 180) for k in f.foot}
    eaves_n = {}
    R, Lh = var["eave-corner-R"][0], var["eave-corner-L"][0]
    for (x, s), pos in f.eave.items():
        if x == x0:
            eaves_n[(x, s)] = _place(R, pos, 0) if s > 0 else _place(Lh, pos, 180)
        elif x == xl:
            eaves_n[(x, s)] = _place(Lh, pos, 0) if s > 0 else _place(R, pos, 180)
        else:
            eaves_n[(x, s)] = _place(var["eave-middle"][0], pos, 0 if s > 0 else 180)
    ridges_n = {}
    for x, pos in f.ridge.items():
        if x == x0:
            ridges_n[x] = _place(var["ridge-end"][0], pos, 0)
        elif x == xl:
            ridges_n[x] = _place(var["ridge-end"][0], pos, 180)
        else:
            ridges_n[x] = _place(var["ridge-middle"][0], pos, 0)

    cables = []
    fo, ea, ri = f.foot, f.eave, f.ridge
    cables += [rod(fo[(x0, -1)], ea[(x0, 1)], CABLE_R), rod(fo[(x0, 1)], ea[(x0, -1)], CABLE_R)]   # rear gable X
    xm = f.xs[1]
    for s in (-1, 1):
        cables += [rod(fo[(x0, s)], ea[(xm, s)], CABLE_R), rod(fo[(xl, s)], ea[(f.xs[-2], s)], CABLE_R)]
        cables += [rod(ea[(x0, s)], ri[xm], CABLE_R), rod(ea[(xl, s)], ri[f.xs[-2]], CABLE_R)]
    off = NODE["anchor_off"]
    anchors = {k: screw_anchor(f.foot[k][0], f.foot[k][1] + k[1] * off) for k in f.foot}
    anchors["g0"] = screw_anchor(x0 - GUY_OUT, 0.0)
    anchors["g1"] = screw_anchor(xl + GUY_OUT, 0.0)
    h = f.p["ridge"]
    guys = {"rear": rod((x0 - 60, 0, h + 20), (x0 - GUY_OUT, 0, 80), 3),
            "front": rod((xl + 60, 0, h + 20), (xl + GUY_OUT, 0, 80), 3)}
    return {
        1: ("EMT post, 3/4 in", posts), 2: ("EMT rafter, 1 in", rafters),
        3: ("EMT ridge tube, 3/4 in", ridges), 4: ("EMT eave tube, 3/4 in", eaves),
        5: ("Foot node", feet), 6: ("Eave node", eaves_n), 7: ("Ridge node", ridges_n),
        8: ("Brace cable", {i: c for i, c in enumerate(cables)}),
        9: ("Screw ground anchor", anchors), 10: ("Guy line", guys),
    }


def member_lengths(size="M"):
    """Cut lengths (mm) of each member type: node-center distance less two tube gaps."""
    f = geometry(size)
    g = 2 * NODE["tube_gap"]
    x0 = f.xs[0]
    L = lambda a, b: math.dist(a, b) - g
    return {"post": L(f.foot[(x0, 1)], f.eave[(x0, 1)]),
            "rafter": L(f.eave[(x0, 1)], f.ridge[x0]),
            "ridge": f.p["bay"] - g, "eave": f.p["bay"] - g}


def main():
    step, stl = ROOT / "cad" / "step", ROOT / "cad" / "stl"
    step.mkdir(parents=True, exist_ok=True); stl.mkdir(parents=True, exist_ok=True)
    asm = assembly("M")
    kids = []
    for no, (name, shapes) in asm.items():
        for k, sh in shapes.items():
            sh.label = f"{no} {name} {k}"
            kids.append(sh)
    export_step(Compound(children=kids), str(step / "snapframe-M-assembly.step"))
    print("wrote cad/step/snapframe-M-assembly.step", len(kids), "solids")
    for size in SIZES:
        var = node_variants(size)
        row = []
        for i, (name, (shape, count, _)) in enumerate(var.items()):
            export_stl(shape, str(stl / f"snapframe-{size}-{name}.stl"))
            placed = Pos(i * 300.0, 0, 0) * shape
            placed.label = f"{size} {name} x{count}"
            row.append(placed)
            print(f"size {size}: {name:13s} x{count:2d}  volume {shape.volume / 1000:6.1f} cm3")
        export_step(Compound(children=row), str(step / f"snapframe-{size}-nodes.step"))
    for size in SIZES:
        ml = member_lengths(size)
        print(f"size {size}: cut lengths mm " + ", ".join(f"{k} {v:.0f}" for k, v in ml.items()))


if __name__ == "__main__":
    main()
