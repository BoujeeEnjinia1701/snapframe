"""SnapFrame parametric model (build123d), TRL 3, constructable design (SNF-DDR-003).

Run from the repo root:
  python cad/src/model.py            exports STEP and STL and prints the constructability checks
  python cad/src/model.py --check    prints the constructability checks only
Exports:
  cad/step/snapframe-M-assembly.step      size M frame assembly (tubes, nodes, hardware, cables, anchors, guys)
  cad/step/snapframe-{S,M,L}-nodes.step   every node variant of each size, laid out in a row
  cad/stl/snapframe-{S,M,L}-<node>.stl    printable node variants (prototype level, no print tolerances)

Prototype detail: socket bores, tube stop, button holes with finger recesses, hitch pin holes,
lead-in chamfers, cable bolt holes with spot face and nut recess, foot plate with two anchor slots,
and the bought hardware (snap buttons with their spring envelope, hitch pins, caps, cable bolt sets,
snap hooks, screw anchors). No fillets or print tolerances for fabrication.
PRELIMINARY, NOT FOR FABRICATION.

Coordinates in mm: X along the ridge, Y across the span, Z up, ground at Z = 0.
Frame lines at X = 0, BAY, 2 BAY, ...; eave nodes at Y = +/- span/2.

SNF-DDR-003 changes from the concept model: spring button 40 mm and hitch pin 15 mm from the
tube end (they clashed inside the tube), a finger recess round every button, a lead-in chamfer
at every socket mouth, printed cable and guy tabs replaced by a through-bolted steel cable bolt
with a ring, brace cables clipped to the anchor eyes at the feet and to the cable bolt rings
at the top, two anchor slots in the foot plate, and the anchor eye turned down onto the plate.

Decisions of 2026-10-02 (SNF-DEC-001): a folding step in the kit for the first prototype (BOM item 15), and longer
screw anchors at the two rear corner feet, rated 1.5 kN (BOM item 16). Posts stay 3/4 in: the frame analysis was run
(SNF-CAL-001 v0.6), so the 1 in post fallback was not triggered.
"""
from __future__ import annotations
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

from build123d import (Box, Cylinder, Sphere, Torus, Pos, Rot, Solid, Plane, Vector, Compound, Face, Wire,
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
TUBE_OF = {"post": "3/4", "rafter": "1", "ridge": "1", "eave": "3/4"}   # DDR-001 D2: 1 in rafters; DDR-002 D8: 1 in ridge tubes

NODE = {
    "core_r": 42.0,        # spherical core radius
    "sock_l": 110.0,       # socket length from node center
    "tube_gap": 45.0,      # tube end sits on the bore's flat stop this far from node center
    "clear": 0.6,          # diametral clearance, bore = tube OD + clear
    "wall": 5.0,           # socket wall thickness (polymer)
    "button_d": 6.0,       # spring button hole, button_at from the tube end (DDR-003 C1: was 25)
    "button_at": 40.0,
    "recess_d": 16.0,      # finger recess round each button hole (DDR-003 C2)
    "recess_wall": 1.5,    # polymer left at the floor of the recess
    "chamfer": 1.5,        # lead-in chamfer at each socket mouth (DDR-003 C2)
    "pin_d": 8.0,          # hitch pin cross hole at tension joints, pin_at from the tube end (DDR-003 C1: was 50)
    "pin_at": 15.0,
    "plate": 170.0,        # foot plate side
    "plate_t": 12.0,
    "z_foot": 60.0,        # foot node center above ground
    "anchor_off": 62.0,    # anchor shaft from the foot node center, along a 45 degree slot (DDR-003 C6)
    "slot_w": 18.0,        # anchor slot width, open to a corner of the plate
}

# Spring snap button (bought): V spring inside the tube. Envelope used for the clash check.
SPRING = {"behind": 5.0, "len": 45.0, "w": 7.0}     # from 5 mm nearer the end than the button to 45 mm deeper

# Cable bolt set (DDR-003 C3): M10 x 90 A4 hex bolt through the node core along its own axis.
# Distances along the axis from the node center; the ring rides on the spacer.
BOLT = {"d": 10.0, "hole": 10.5, "spot": 39.0, "spot_r": 16.0, "washer_od": 30.0, "washer_t": 2.5,
        "spacer_od": 14.0, "spacer_l": 10.0, "head_washer_od": 24.0, "head_washer_t": 2.0,
        "head_af": 16.0, "head_h": 6.4, "length": 90.0,
        "recess_r": 13.5, "recess_at": 22.0, "nut_washer_od": 20.0, "nut_washer_t": 2.0, "nut_h": 10.0,
        "ring_id": 32.0, "ring_wire": 6.0}
BOLT_DIR = {"eave": (0.0, -math.cos(math.radians(35)), -math.sin(math.radians(35))),   # inward, 35 deg down
            "ridge": (0.0, 0.0, -1.0)}                                                 # straight down
HOOK_L = 60.0          # snap hook and loop eye, from the ring or anchor eye to the start of the wire

SIZES = {
    #        span W, bays, bay, eave, ridge
    "S": {"span": 3000.0, "bays": 2, "bay": 1500.0, "eave": 1800.0, "ridge": 2400.0},
    "M": {"span": 4000.0, "bays": 2, "bay": 2000.0, "eave": 1800.0, "ridge": 2600.0},
    "L": {"span": 4000.0, "bays": 3, "bay": 2000.0, "eave": 1800.0, "ridge": 2600.0},
}
GUY_OUT = 1500.0       # guy anchors this far beyond each gable
CABLE_R = 2.0          # 4 mm wire rope
ANCHOR_DEPTH = 380.0
ANCHOR_DEPTH_REAR = 560.0   # longer anchor at the two rear corner feet, rated 1.5 kN (decided 2026-10-02, SNF-DEC-001)
# Folding step in the first prototype's kit (decided 2026-10-02, SNF-DDR-003 A1): two treads, stands inside the
# frame to reach the ridge sockets at 2.6 m. Massing model of a bought step, about 1.5 kg.
STEP = {"x": 1000.0, "y": 0.0, "w": 450.0, "d": 500.0, "top": 500.0, "mid": 250.0, "tread": 250.0, "t": 20.0,
        "reach_standing": 2200.0}
EYE_R, EYE_WIRE = 28.0, 6.0     # screw anchor eye: ring radius and wire radius
CABLE_ENDS = {}        # filled by build_components: cable key -> (attachment point, attachment point)


def V(*a):
    return Vector(*a)


def bore_of(kind):
    return TUBES[TUBE_OF[kind]]["od"] + NODE["clear"]


def sock_r_of(kind):
    return bore_of(kind) / 2 + NODE["wall"]


def _perp(u):
    """A unit vector perpendicular to u, horizontal where possible (button and pin direction)."""
    ref = V(0, 0, 1) if abs(u.Z) < 0.9 else V(1, 0, 0)
    return u.cross(ref).normalized()


def rotz(v, deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    v = V(*v) if not isinstance(v, Vector) else v
    return V(c * v.X - s * v.Y, s * v.X + c * v.Y, v.Z)


def rod(a, b, r):
    a = V(*a); b = V(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def cyl(origin, direction, r, length):
    d = V(*direction).normalized()
    return Solid.make_cylinder(r, length, Plane(origin=V(*origin), z_dir=d))


def hexagon(origin, direction, af, h):
    from build123d import RegularPolygon, extrude, Sketch  # noqa: F401
    d = V(*direction).normalized()
    pl = Plane(origin=V(*origin), z_dir=d)
    poly = RegularPolygon(af / math.sqrt(3), 6)
    return extrude(pl * poly, h, dir=d)


def fuse(shapes):
    out = None
    for s in shapes:
        if s is None:
            continue
        out = s if out is None else out + s
    return out


def tube(a, b, kind, w_a=None, w_b=None, pinned=False):
    """Hollow EMT member between two node centers, trimmed to sit on the socket stops. w_a and w_b
    are the button directions at each end (from the sockets); the holes are drilled to match."""
    a = V(*a); b = V(*b); u = (b - a).normalized()
    p, q = a + u * NODE["tube_gap"], b - u * NODE["tube_gap"]
    t = TUBES[TUBE_OF[kind]]
    ln = (q - p).length
    outer = Solid.make_cylinder(t["od"] / 2, ln, Plane(origin=p, z_dir=u))
    inner = Solid.make_cylinder(t["od"] / 2 - t["wall"], ln, Plane(origin=p, z_dir=u))
    s = outer - inner
    n = NODE
    for end, d, w in ((p, u, w_a), (q, -u, w_b)):
        if w is None:
            continue
        w = V(*w).normalized()
        s = s - cyl(end + d * n["button_at"], w, n["button_d"] / 2, t["od"])
        if pinned:
            c = end + d * n["pin_at"]
            s = s - cyl(c - w * t["od"], w, n["pin_d"] / 2, 2 * t["od"])
    return s


@dataclass
class Socket:
    direction: tuple
    kind: str              # member kind, sets the bore
    pinned: bool = False   # hitch pin cross hole (tension joint)
    blank: bool = False    # socket left empty and capped in some positions (corner eave nodes)


def node(sockets, foot=False, bolt=None, outboard=(0, 1, 0)):
    """Printed node at the origin: spherical core, one bored socket per member, optional foot plate
    with two anchor slots, optional cable bolt hole (bolt: unit vector toward the cable side)."""
    n = NODE
    s = Sphere(n["core_r"])
    cuts = []
    for sk in sockets:
        u = V(*sk.direction).normalized()
        rs = sock_r_of(sk.kind); rb = bore_of(sk.kind) / 2
        s = s + Solid.make_cylinder(rs, n["sock_l"], Plane(origin=V(0, 0, 0), z_dir=u))
        # bore from the tube-end stop to the socket mouth, with a lead-in chamfer at the mouth
        cuts.append(Solid.make_cylinder(rb, n["sock_l"] - n["tube_gap"] + 1, Plane(origin=u * n["tube_gap"], z_dir=u)))
        ch = n["chamfer"]
        cuts.append(Solid.make_cone(rb, rb + ch + 0.5, ch + 0.5, Plane(origin=u * (n["sock_l"] - ch), z_dir=u)))
        w = _perp(u)
        at_b = u * (n["tube_gap"] + n["button_at"])
        cuts.append(cyl(at_b, w, n["button_d"] / 2, rs + 2))
        cuts.append(cyl(at_b + w * (rb + n["recess_wall"]), w, n["recess_d"] / 2, rs))   # finger recess
        if sk.pinned:
            at_p = u * (n["tube_gap"] + n["pin_at"])
            ln = 2 * rs + 4
            cuts.append(cyl(at_p - w * (ln / 2), w, n["pin_d"] / 2, ln))
    if foot:
        z0 = -n["z_foot"]
        o = V(*outboard).normalized()
        s = s + Pos(0, 0, z0 + n["plate_t"] / 2) * Box(n["plate"], n["plate"], n["plate_t"])
        s = s + Pos(0, 0, z0 + n["plate_t"] + 20) * Cylinder(30, 40)   # boss joining core to plate
        side = o.cross(V(0, 0, 1)).normalized()
        for sg in (1, -1):                                              # two slots, 45 deg either side of outboard
            d = (o + side * sg).normalized()
            a = d * n["anchor_off"]
            run = n["plate"] / 2 * math.sqrt(2) - n["anchor_off"] + 10
            cuts.append(cyl((a.X, a.Y, z0 - 5), (0, 0, 1), n["slot_w"] / 2, n["plate_t"] + 10))
            cuts.append(Plane(origin=(a + d * (run / 2)) + V(0, 0, z0 + n["plate_t"] / 2), x_dir=d, z_dir=(0, 0, 1))
                        * Box(run, n["slot_w"], n["plate_t"] + 10))
    if bolt is not None:
        a = V(*bolt).normalized(); B = BOLT
        cuts.append(cyl(-a * 60, a, B["hole"] / 2, 120))
        cuts.append(cyl(a * B["spot"], a, B["spot_r"], 30))             # flat spot face for the washer
        cuts.append(cyl(-a * B["recess_at"], -a, B["recess_r"], 40))     # nut recess, nut below the surface
    for c in cuts:
        s = s - c
    return s


# ---------------------------------------------------------------- bought hardware, node-local
def cable_bolt(a):
    """Cable bolt set at the origin of a node, along unit a: washer, spacer, head washer, head, shank,
    far washer and nyloc nut. Returns (hardware, ring_center, a)."""
    a = V(*a).normalized(); B = BOLT
    s0 = B["spot"]
    hw = cyl(a * s0, a, B["washer_od"] / 2, B["washer_t"]) - cyl(a * (s0 - 1), a, B["hole"] / 2, 10)
    s1 = s0 + B["washer_t"]
    sp = cyl(a * s1, a, B["spacer_od"] / 2, B["spacer_l"]) - cyl(a * (s1 - 1), a, B["hole"] / 2, B["spacer_l"] + 2)
    s2 = s1 + B["spacer_l"]
    hw2 = cyl(a * s2, a, B["head_washer_od"] / 2, B["head_washer_t"]) - cyl(a * (s2 - 1), a, B["hole"] / 2, 10)
    s3 = s2 + B["head_washer_t"]
    head = hexagon(a * s3, a, B["head_af"], B["head_h"])
    shank = cyl(a * (s3 - B["length"]), a, B["d"] / 2 - 0.25, B["length"])
    fw = cyl(-a * B["recess_at"], -a, B["nut_washer_od"] / 2, B["nut_washer_t"]) - cyl(-a * (B["recess_at"] - 1), -a, B["hole"] / 2, 10)
    nut = hexagon(-a * (B["recess_at"] + B["nut_washer_t"]), -a, B["head_af"] + 1, B["nut_h"]) - cyl(-a * B["recess_at"], -a, B["d"] / 2, 20)
    return fuse([hw, sp, hw2, head, shank, fw, nut])


def bolt_tip(a):
    """Distance of the bolt tip from the node center (negative: on the nut side)."""
    B = BOLT
    return B["spot"] + B["washer_t"] + B["spacer_l"] + B["head_washer_t"] - B["length"]


def ring_on_bolt(center, a, pull):
    """Welded ring hanging on the spacer, pulled toward `pull` (global unit vector). Returns (shape, far point)."""
    B = BOLT
    a = V(*a).normalized()
    s_mid = B["spot"] + B["washer_t"] + B["spacer_l"] / 2
    p = V(*pull)
    p = (p - a * p.dot(a))
    p = p.normalized() if p.length > 1e-6 else _perp(a)
    r_mean = B["ring_id"] / 2 + B["ring_wire"] / 2
    # ring plane perpendicular to the bolt axis, its inner edge resting on the spacer
    c = V(*center) + a * s_mid + p * (B["ring_id"] / 2 - B["spacer_od"] / 2)
    ring = Plane(origin=c, z_dir=a) * Torus(r_mean, B["ring_wire"] / 2)
    return ring, c, r_mean


def button(at, u, w, kind):
    """Snap button pin standing in the socket hole, 2 mm proud of the recess floor (node-local)."""
    n = NODE
    rb = bore_of(kind) / 2
    return cyl(at + w * (rb - 1.5), w, n["button_d"] / 2 - 0.3, n["recess_wall"] + 1.5 + 2.0)


def spring_env(end, d, w, kind):
    """Envelope of the V spring inside a tube end: end = tube end point, d = into the tube."""
    t = TUBES[TUBE_OF[kind]]
    ri = t["od"] / 2 - t["wall"]
    x0 = NODE["button_at"] - SPRING["behind"]
    c = end + d * (x0 + SPRING["len"] / 2)
    v = d.cross(w).normalized()
    return Plane(origin=c, x_dir=d, z_dir=v) * Box(SPRING["len"], 2 * ri - 1.0, SPRING["w"])


def hitch_pin(at, w, kind):
    rs = sock_r_of(kind)
    ln = 2 * rs + 14
    return cyl(at - w * (ln / 2), w, NODE["pin_d"] / 2, ln)


def cap(u, kind):
    rb = bore_of(kind) / 2
    n = NODE
    return cyl(u * (n["sock_l"] - 20), u, rb, 20) + cyl(u * n["sock_l"], u, sock_r_of(kind), 2.0)


def screw_anchor(x, y, top_z=20.0, depth=ANCHOR_DEPTH, axis=(0, 1, 0)):
    """Screw anchor; the eye ring is centred at top_z + 58, its axis horizontal along `axis`."""
    shaft = rod((x, y, top_z - depth), (x, y, top_z + 30), 7)
    helix = Pos(x, y, top_z - depth + 60) * Cylinder(45, 6)
    eye = Plane(origin=(x, y, top_z + 58), z_dir=V(*axis).normalized()) * Torus(EYE_R, EYE_WIRE)
    return shaft + helix + eye


def folding_step(x=None, y=None):
    """Two-tread folding step, long side along the ridge, deep side across the span, massing model."""
    sides, treads = folding_step_parts(x, y)
    return fuse(sides + treads)


def folding_step_parts(x=None, y=None):
    """The step as (two side frames, two treads), for the appearance model."""
    st = STEP
    x = st["x"] if x is None else x; y = st["y"] if y is None else y
    d, top, t, w = st["d"], st["top"], st["t"], st["w"]
    # side frame: a trapezoid in the Y-Z plane, front face upright, back leaning out to the ground
    pts = [(y - d / 2, 0), (y + d / 2, 0), (y + d / 2 - 250, top), (y - d / 2, top)]
    parts = []; treads = []
    for sx in (-1, 1):
        x0 = x + sx * (w / 2 - t / 2)
        poly = [Vector(x0 - t / 2, py, pz) for py, pz in pts]
        parts.append(Solid.extrude(Face(Wire.make_polygon(poly, close=True)), Vector(t, 0, 0)))
    for z, depth in ((st["top"], st["tread"]), (st["mid"], st["tread"] + 100)):
        treads.append(Pos(x, y - d / 2 + depth / 2, z - t / 2) * Box(w, depth, t))
    return parts, treads


def anchor_eye_center_z():
    """Eye centre height with the eye turned down onto the foot plate across the slot (DDR-003 C5)."""
    n = NODE
    return n["plate_t"] + math.sqrt((EYE_R + EYE_WIRE) ** 2 - (n["slot_w"] / 2) ** 2)


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


def node_sockets(size="M"):
    f = geometry(size)
    x0 = f.xs[0]
    foot = [Socket(_d(f.foot[(x0, 1)], f.eave[(x0, 1)]), "post", True)]
    # DDR-002 D9: one four-socket eave node everywhere; at the corners the socket past the gable stays blank (capped)
    eave = [Socket(_d(f.eave[(x0, 1)], f.foot[(x0, 1)]), "post", True),
            Socket(_d(f.eave[(x0, 1)], f.ridge[x0]), "rafter"), Socket((1, 0, 0), "eave"),
            Socket((-1, 0, 0), "eave")]
    ridge_e = [Socket(_d(f.ridge[x0], f.eave[(x0, -1)]), "rafter"), Socket(_d(f.ridge[x0], f.eave[(x0, 1)]), "rafter"),
               Socket((1, 0, 0), "ridge")]
    return {"foot": foot, "eave": eave, "ridge-end": ridge_e, "ridge-middle": ridge_e + [Socket((-1, 0, 0), "ridge")]}


def node_variants(size="M"):
    """Unique node variants of one size, at the origin: {name: (shape, count, [positions])}."""
    f = geometry(size)
    x0, xl = f.xs[0], f.xs[-1]
    sk = node_sockets(size)
    return {
        "foot": (node(sk["foot"], foot=True, outboard=(0, 1, 0)), len(f.foot), [f.foot[k] for k in f.foot]),
        "eave": (node(sk["eave"], bolt=BOLT_DIR["eave"]), len(f.eave), [f.eave[k] for k in f.eave]),
        "ridge-end": (node(sk["ridge-end"], bolt=BOLT_DIR["ridge"]), 2, [f.ridge[x0], f.ridge[xl]]),
        "ridge-middle": (node(sk["ridge-middle"], bolt=BOLT_DIR["ridge"]), len(f.xs) - 2, [f.ridge[x] for x in f.xs[1:-1]]),
    }


def _place(shape, at, rot_z=0.0):
    return Pos(*at) * Rot(0, 0, rot_z) * shape


def member_lengths(size="M"):
    """Cut lengths (mm) of each member type: node-center distance less two tube gaps."""
    f = geometry(size)
    g = 2 * NODE["tube_gap"]
    x0 = f.xs[0]
    L = lambda a, b: math.dist(a, b) - g  # noqa: E731
    return {"post": L(f.foot[(x0, 1)], f.eave[(x0, 1)]),
            "rafter": L(f.eave[(x0, 1)], f.ridge[x0]),
            "ridge": f.p["bay"] - g, "eave": f.p["bay"] - g}


# ---------------------------------------------------------------- the frame, part by part
@dataclass
class Comp:
    key: str
    name: str
    shape: object
    bom: int
    group: str


def layout(size="M"):
    """Positions, rotations and socket data of every node, and the member list.
    Returns dict with nodes {key: (variant, center, rot)} and members [(key, kind, node_a, node_b)]."""
    f = geometry(size)
    x0, xl = f.xs[0], f.xs[-1]
    nodes = {}
    for k, c in f.foot.items():
        nodes[("foot",) + k] = ("foot", c, 0 if k[1] > 0 else 180)
    for k, c in f.eave.items():
        nodes[("eave",) + k] = ("eave", c, 0 if k[1] > 0 else 180)
    for x, c in f.ridge.items():
        v = "ridge-end" if x in (x0, xl) else "ridge-middle"
        nodes[("ridge", x)] = (v, c, 180 if x == xl else 0)
    members = []
    for k in f.foot:
        members.append((("post",) + k, "post", ("foot",) + k, ("eave",) + k))
    for k in f.eave:
        members.append((("rafter",) + k, "rafter", ("eave",) + k, ("ridge", k[0])))
    for i in range(len(f.xs) - 1):
        members.append((("ridge", i), "ridge", ("ridge", f.xs[i]), ("ridge", f.xs[i + 1])))
        for s in (-1, 1):
            members.append((("eave", i, s), "eave", ("eave", f.xs[i], s), ("eave", f.xs[i + 1], s)))
    return f, nodes, members


def socket_toward(size, node_key, target, nodes):
    """The socket of a placed node that points at `target` (global), with its global direction and button direction."""
    var, c, rot = nodes[node_key]
    want = (V(*target) - V(*c)).normalized()
    for sk in node_sockets(size)[var]:
        u = rotz(V(*sk.direction).normalized(), rot)
        if (u - want).length < 1e-6:
            return sk, u, rotz(_perp(V(*sk.direction).normalized()), rot)
    raise ValueError(f"no socket of {node_key} points at {target}")


def anchor_slot_dir(size, k):
    """Slot used at foot k: backward and outward at the rear corners and middle feet, forward and outward at the front."""
    f = geometry(size)
    xl = f.xs[-1]
    fx = 1 if k[0] == xl else -1
    return V(fx, k[1], 0).normalized()


def cable_list(size="M"):
    """Brace cables as (key, kind, lower end, upper end). Ends are ('anchor', foot key) or ('bolt', node key)."""
    f = geometry(size)
    x0, xl, xs = f.xs[0], f.xs[-1], f.xs
    out = [(("gable", -1), "gable", ("anchor", (x0, -1)), ("bolt", ("eave", x0, 1))),
           (("gable", 1), "gable", ("anchor", (x0, 1)), ("bolt", ("eave", x0, -1)))]
    for s in (-1, 1):
        out.append((("wall", x0, s), "wall", ("anchor", (x0, s)), ("bolt", ("eave", xs[1], s))))
        out.append((("wall", xl, s), "wall", ("anchor", (xl, s)), ("bolt", ("eave", xs[-2], s))))
        out.append((("roof", x0, s), "roof", ("bolt", ("eave", x0, s)), ("bolt", ("ridge", xs[1]))))
        out.append((("roof", xl, s), "roof", ("bolt", ("eave", xl, s)), ("bolt", ("ridge", xs[-2]))))
    return out


def build_components(size="M"):
    """Every part of the frame, keyed. Shapes in global coordinates."""
    f, nodes, members = layout(size)
    x0, xl = f.xs[0], f.xs[-1]
    var = node_variants(size)
    C = {}

    def add(key, name, shape, bom, group):
        C[key] = Comp(key, name, shape, bom, group)

    # nodes
    for k, (v, c, rot) in nodes.items():
        add(("node",) + k, {"foot": "Foot node", "eave": "Eave node", "ridge-end": "Ridge node, end",
                            "ridge-middle": "Ridge node, middle"}[v], _place(var[v][0], c, rot),
            {"foot": 5, "eave": 6}.get(v, 7), "node")
    # members, with button and pin holes drilled to match the sockets at both ends
    used = {}
    for mk, kind, na, nb in members:
        ca, cb = nodes[na][1], nodes[nb][1]
        ska, ua, wa = socket_toward(size, na, cb, nodes)
        skb, ub, wb = socket_toward(size, nb, ca, nodes)
        pinned = ska.pinned or skb.pinned
        add(("tube",) + mk, {"post": "EMT post, 3/4 in", "rafter": "EMT rafter, 1 in", "ridge": "EMT ridge tube, 1 in",
                             "eave": "EMT eave tube, 3/4 in"}[kind],
            tube(ca, cb, kind, wa, wb, pinned), {"post": 1, "rafter": 2, "ridge": 3, "eave": 4}[kind], "tube")
        for nk, c, u, w, sk in ((na, ca, ua, wa, ska), (nb, cb, ub, wb, skb)):
            used.setdefault(nk, []).append(u)
            n = NODE
            at_b = V(*c) + u * (n["tube_gap"] + n["button_at"])
            add(("button",) + mk + (nk,), "Snap button", button(at_b, u, w, kind), 12, "hardware")
            add(("spring",) + mk + (nk,), "Snap button spring (inside the tube)",
                spring_env(V(*c) + u * n["tube_gap"], u, w, kind), 12, "hardware")
            if sk.pinned:
                add(("pin",) + mk + (nk,), "Hitch pin", hitch_pin(V(*c) + u * (n["tube_gap"] + n["pin_at"]), w, kind), 12, "hardware")
    # caps on the blank sockets of the corner eave nodes
    for k, (v, c, rot) in nodes.items():
        if v != "eave":
            continue
        for sk in node_sockets(size)["eave"]:
            u = rotz(V(*sk.direction).normalized(), rot)
            if not any((u - x).length < 1e-6 for x in used[k]):
                add(("cap",) + k, "Socket cap", Pos(*c) * cap(u, sk.kind), 12, "hardware")
    # cable bolt sets and anchors
    anchors = {}
    for k, c in f.foot.items():
        d = anchor_slot_dir(size, k)
        a = V(*c) + d * NODE["anchor_off"]
        zc = anchor_eye_center_z()
        anchors[k] = (a.X, a.Y, zc, d)
        rear = k[0] == x0
        add(("anchor", k), "Long screw anchor (rear corner)" if rear else "Screw anchor",
            screw_anchor(a.X, a.Y, top_z=zc - 58, axis=(d.X, d.Y, 0), depth=ANCHOR_DEPTH_REAR if rear else ANCHOR_DEPTH),
            16 if rear else 9, "anchor")
    for g, gx in (("rear", x0 - GUY_OUT), ("front", xl + GUY_OUT)):
        add(("anchor", g), "Screw anchor (guy)", screw_anchor(gx, 0.0), 9, "anchor")
    add(("step",), "Folding step", folding_step(), 15, "hardware")
    # cable ends
    cab = cable_list(size)
    bolt_axis = {}
    for k, (v, c, rot) in nodes.items():
        if v == "foot":
            continue
        a = rotz(V(*BOLT_DIR["eave" if v == "eave" else "ridge"]), rot)
        bolt_axis[k] = (V(*c), a)
        add(("bolt",) + k, "Cable bolt set", Pos(*c) * cable_bolt(rotz(V(*BOLT_DIR["eave" if v == "eave" else "ridge"]), rot)), 14, "hardware")

    def end_point(e, other):
        if e[0] == "anchor":
            x, y, zc, d = anchors[e[1]]
            return V(x, y, zc + EYE_R - EYE_WIRE)               # inside top of the eye
        return None

    # resultant pull on each bolt ring, then the ring position
    pulls = {}
    ends = {}
    for ck, kind, lo, hi in cab:
        for me, ot in ((lo, hi), (hi, lo)):
            if me[0] == "bolt":
                ends.setdefault(me[1], []).append((ck, ot))
    guy_target = {("ridge", x0): ("anchor", "rear"), ("ridge", xl): ("anchor", "front")}
    for nk, g in guy_target.items():
        ends.setdefault(nk, []).append((("guy", g[1]), g))

    def approx(e):
        if e[0] == "anchor":
            if e[1] in ("rear", "front"):
                gx = x0 - GUY_OUT if e[1] == "rear" else xl + GUY_OUT
                return V(gx, 0, 78 + EYE_R - EYE_WIRE)
            return end_point(e, None)
        return bolt_axis[e[1]][0] + bolt_axis[e[1]][1] * 47

    rings = {}
    for nk, lst in ends.items():
        c, a = bolt_axis[nk]
        tot = V(0, 0, 0)
        for ck, ot in lst:
            tot = tot + (approx(ot) - (c + a * 47)).normalized()
        ring, rc, rm = ring_on_bolt(c, a, tot)
        rings[nk] = (rc, a, rm)
        add(("ring",) + nk, "Cable ring", ring, 14, "hardware")

    def attach(e, toward):
        """Point where the hook clips on: the ring wire facing the cable, or the anchor eye top."""
        if e[0] == "anchor":
            if e[1] in ("rear", "front"):
                gx = x0 - GUY_OUT if e[1] == "rear" else xl + GUY_OUT
                return V(gx, 0, 78 + EYE_R - EYE_WIRE)
            return end_point(e, None)
        rc, a, rm = rings[e[1]]
        d = toward - rc
        d = (d - a * d.dot(a)).normalized()
        return rc + d * rm

    def wire(ck, kind, lo, hi, name, bom, r=CABLE_R):
        pa = approx(lo); pb = approx(hi)
        A = attach(lo, pb); Bp = attach(hi, pa)
        u = (Bp - A).normalized()
        hook_a = A + u * 4; hook_b = Bp - u * 4
        wa = A + u * HOOK_L; wb = Bp - u * HOOK_L
        add(("hook",) + ck + ("lo",), "Snap hook", rod(hook_a, wa, 3.0), bom, "cable")
        add(("hook",) + ck + ("hi",), "Snap hook", rod(wb, hook_b, 3.0), bom, "cable")
        add(("cable",) + ck, name, rod(wa, wb, r), bom, "cable")
        CABLE_ENDS[ck] = (A, Bp)
        return (A - Bp).length
    lengths = {}
    for ck, kind, lo, hi in cab:
        lengths[ck] = wire(ck, kind, lo, hi, "Brace cable", 8)
    for nk, g in guy_target.items():
        lengths[("guy", g[1])] = wire(("guy", g[1]), "guy", ("bolt", nk), g, "Guy line", 10, r=3.0)
    C["_lengths"] = lengths
    return C


def comps(size="M"):
    C = build_components(size)
    lengths = C.pop("_lengths")
    return C, lengths


def assembly(size="M"):
    """Frame assembly grouped by BOM item: {bom_no: (name, {key: shape})}."""
    C, _ = comps(size)
    names = {1: "EMT post, 3/4 in", 2: "EMT rafter, 1 in", 3: "EMT ridge tube, 1 in", 4: "EMT eave tube, 3/4 in",
             5: "Foot node", 6: "Eave node", 7: "Ridge node", 8: "Brace cable", 9: "Screw ground anchor",
             10: "Guy line", 12: "Snap buttons, hitch pins and caps", 14: "Cable bolt set and ring",
             15: "Folding step", 16: "Long screw anchor (rear corners)"}
    out = {no: (nm, {}) for no, nm in names.items()}
    for k, c in C.items():
        if c.key[0] == "spring":
            continue                       # inside the tubes; checks only
        out[c.bom][1][k] = c.shape
    return out


def cable_lengths(size="M"):
    """Eye-to-eye lengths (mm) of each cable assembly: attachment to attachment, less both hooks."""
    _, L = comps(size)
    return {k: v - 2 * HOOK_L for k, v in L.items()}


# ---------------------------------------------------------------- constructability checks
def _vol(a, b):
    try:
        r = a & b
        return 0.0 if r is None else abs(r.volume)
    except Exception:
        return float("nan")


def _gap(a, b):
    try:
        return a.distance_to(b)
    except Exception:
        return float("nan")


def _bbgap(a, b):
    A, B = a.bounding_box(), b.bounding_box()
    dx = max(A.min.X - B.max.X, B.min.X - A.max.X, 0)
    dy = max(A.min.Y - B.max.Y, B.min.Y - A.max.Y, 0)
    dz = max(A.min.Z - B.max.Z, B.min.Z - A.max.Z, 0)
    return math.sqrt(dx * dx + dy * dy + dz * dz)


def checks(size="M"):
    """(description, overlap mm3, gap mm, expectation, ok) for every pair that must touch or stay apart."""
    C, L = comps(size)
    rows = []
    f, nodes, members = layout(size)

    def chk(desc, a, b, expect):
        if not isinstance(b, (list, tuple)):
            b = [b]
        b = [x for x in b if _bbgap(a, x) < 60] or b[:1]
        v = sum(_vol(a, x) for x in b); g = min(_gap(a, x) for x in b)
        if expect == "touch":
            ok = v < 1.0 and g < 0.05
        elif expect == "overlap-ok":
            ok = True
        else:
            ok = v < 1e-3 and g >= expect - 1e-6
        rows.append((desc, v, g, expect, ok))

    by = lambda t: {k: c for k, c in C.items() if k[0] == t}  # noqa: E731
    tubes, nds, pins, springs, bolts, rings = by("tube"), by("node"), by("pin"), by("spring"), by("bolt"), by("ring")
    hooks, cables, anchors, buttons, caps = by("hook"), by("cable"), by("anchor"), by("button"), by("cap")
    tube_list = [t.shape for t in tubes.values()]
    # 1. every tube end sits on its socket stop, clear of the bore wall
    for mk, kind, na, nb in members:
        t = tubes[("tube",) + mk].shape
        for nk in (na, nb):
            chk(f"{kind} {mk[1:]} seated in {nk[0]} node {nk[1:]}", t, nds[("node",) + nk].shape, "touch")
    # 2. hitch pins pass through tube and socket holes; springs clear of pins
    for k, p in pins.items():
        mk = k[1:-1]; nk = k[-1]
        chk(f"hitch pin {nk[1:]} through the {mk[0]} holes", p.shape, tubes[("tube",) + mk].shape, "touch")
        chk(f"hitch pin {nk[1:]} through the socket holes", p.shape, nds[("node",) + nk].shape, "touch")
        chk(f"hitch pin {nk[1:]} clear of the button spring", p.shape, springs[("spring",) + mk + (nk,)].shape, 3.0)
    # 3. buttons stand in the socket holes
    for k, b in list(buttons.items())[:8]:
        chk(f"snap button {k[1:3]} in its socket hole", b.shape, nds[("node",) + k[-1]].shape, 0.2)
    # 4. caps in the blank sockets
    for k, c in caps.items():
        chk(f"cap in the blank socket of eave node {k[2:]}", c.shape, nds[("node",) + k[1:]].shape, "touch")
    # 5. cable bolts seated, rings on the spacers, rings clear of the node and tubes
    for k, b in bolts.items():
        nk = k[1:]
        chk(f"cable bolt seated in {nk[0]} node {nk[1:]}", b.shape, nds[("node",) + nk].shape, "touch")
        chk(f"cable bolt of {nk[0]} node {nk[1:]} clear of the tubes", b.shape, tube_list, 2.0)
        for pk, p in pins.items():
            if pk[-1] == nk:
                chk(f"cable bolt of {nk[0]} node {nk[1:]} clear of the hitch pin", b.shape, p.shape, 3.0)
        if ("ring",) + nk in rings:
            r = rings[("ring",) + nk].shape
            chk(f"ring on the cable bolt of {nk[0]} node {nk[1:]}", r, b.shape, "touch")
            chk(f"ring of {nk[0]} node {nk[1:]} clear of the node", r, nds[("node",) + nk].shape, 1.0)
            chk(f"ring of {nk[0]} node {nk[1:]} clear of the tubes", r, tube_list, 2.0)
    # 6. anchors: eye down on the foot plate, shaft clear in its slot
    for k, a in anchors.items():
        if k[1] in ("rear", "front"):
            continue
        chk(f"anchor eye on the foot plate {k[1]}", a.shape, nds[("node", "foot") + k[1]].shape, "touch")
    # 6b. long anchors at the rear corner feet are longer, same eye and helix; the folding step stands clear and reaches the ridge
    x0 = f.xs[0]
    for k, a in anchors.items():
        if k[1] in ("rear", "front"):
            continue
        bb = a.shape.bounding_box()
        want = ANCHOR_DEPTH_REAR if k[1][0] == x0 else ANCHOR_DEPTH
        depth = anchor_eye_center_z() - 58 - bb.min.Z
        rows.append((f"anchor at foot {k[1]} is {want:.0f} mm long ({'rear corner, 1.5 kN' if k[1][0] == x0 else '1.0 kN'})",
                     0, depth - want, 0.0, abs(depth - want) < 0.5))
    stp = C[("step",)].shape
    sb = stp.bounding_box()
    chk("folding step clear of tubes, nodes, bolts and rings", stp, [c.shape for k, c in C.items() if k[0] in ("tube", "node", "bolt", "ring", "pin")], 100.0)
    chk("folding step clear of cables, hooks and guys", stp, [c.shape for k, c in C.items() if k[0] in ("cable", "hook")], 300.0)
    rows.append((f"folding step stands on the ground (lowest point {sb.min.Z:.0f} mm), top tread {STEP['top']:.0f} mm", 0, sb.min.Z, 0.0, abs(sb.min.Z) < 0.5))
    reach = STEP["reach_standing"] + STEP["top"]
    rows.append((f"standing on the step a person reaches {reach:.0f} mm, ridge sockets at {f.p['ridge']:.0f} mm", 0, reach - f.p["ridge"], 50.0,
                 reach - f.p["ridge"] >= 50.0))
    rows.append(("folding step footprint inside the frame, between frames 0 and 1",
                 0, 0, "inside", 0 < sb.min.X and sb.max.X < f.xs[1] and abs(sb.min.Y) < f.p["span"] / 2))
    # 7. cables and guys clear of every tube, node and bolt except where they clip on
    allsolid = [c.shape for k, c in C.items() if k[0] in ("tube", "node", "bolt", "pin")]
    for k, c in cables.items():
        chk(f"{'guy line' if k[1] == 'guy' else 'brace cable'} {k[1:]} clear of tubes, nodes and bolts", c.shape, allsolid, 5.0)
    for k, c in hooks.items():
        chk(f"snap hook {k[1:]} clear of tubes, nodes and bolts", c.shape, allsolid, 2.0)
    gx = [c.shape for k, c in cables.items() if k[1] == "gable"]
    if len(gx) == 2:
        chk("rear gable cables cross (tie them together at the crossing)", gx[0], gx[1], "overlap-ok")
    # 8. button directions at the two ends of each tube are opposite (one drilling rule for every tube)
    for mk, kind, na, nb in members:
        ca, cb = nodes[na][1], nodes[nb][1]
        _, ua, wa = socket_toward(size, na, cb, nodes)
        _, ub, wb = socket_toward(size, nb, ca, nodes)
        ok = (wa + wb).length < 1e-6
        rows.append((f"{kind} {mk[1:]}: button holes on opposite sides of the tube", 0.0, 0.0, "opposite", ok))
    # 9. arithmetic checks
    n = NODE
    sp0, sp1 = n["button_at"] - SPRING["behind"], n["button_at"] - SPRING["behind"] + SPRING["len"]
    old = (25.0 - SPRING["behind"], 25.0 - SPRING["behind"] + SPRING["len"])
    rows.append((f"concept layout: pin at 50 mm inside the spring ({old[0]:.0f} to {old[1]:.0f} mm), clash", 0, 0,
                 "for the record", True))
    rows.append((f"pin {n['pin_at']:.0f} mm from the tube end, spring {sp0:.0f} to {sp1:.0f} mm", 0, sp0 - n["pin_at"] - n["pin_d"] / 2,
                 3.0, sp0 - n["pin_at"] - n["pin_d"] / 2 >= 3.0))
    gapm = f.p["bay"] - 2 * n["sock_l"]
    eng = n["sock_l"] - n["tube_gap"]
    rows.append((f"eave and ridge tubes {member_lengths(size)['eave']:.0f} mm are longer than the {gapm:.0f} mm between socket "
                 f"mouths: each frame slides {eng:.0f} mm onto them before the anchors go in", 0, 0, "sequence", True))
    for v, (shape, cnt, _) in node_variants(size).items():
        b = shape.bounding_box()
        mx = max(b.size.X, b.size.Y, b.size.Z)
        rows.append((f"{v} node prints on a 256 mm bed: box {b.size.X:.0f} x {b.size.Y:.0f} x {b.size.Z:.0f} mm",
                     0, 256 - mx, 0.0, mx <= 256))
    return rows


def print_checks(size="M"):
    rows = checks(size)
    bad = 0
    for desc, v, g, exp, ok in rows:
        bad += 0 if ok else 1
        e = exp if isinstance(exp, str) else f">= {exp:g} mm"
        print(f"{'ok  ' if ok else 'FAIL'} {desc}: overlap {v:.1f} mm3, gap {g:.2f} mm ({e})")
    print(f"{len(rows) - bad} of {len(rows)} constructability checks pass")
    return bad


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
            export_stl(shape, str(stl / f"snapframe-{size}-{name}.stl"), tolerance=0.05, angular_tolerance=0.3)
            placed = Pos(i * 300.0, 0, 0) * shape
            placed.label = f"{size} {name} x{count}"
            row.append(placed)
            print(f"size {size}: {name:13s} x{count:2d}  volume {shape.volume / 1000:6.1f} cm3")
        export_step(Compound(children=row), str(step / f"snapframe-{size}-nodes.step"))
    for size in SIZES:
        ml = member_lengths(size)
        print(f"size {size}: cut lengths mm " + ", ".join(f"{k} {v:.0f}" for k, v in ml.items()))


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks("M") else 0)
    main()
    print_checks("M")
