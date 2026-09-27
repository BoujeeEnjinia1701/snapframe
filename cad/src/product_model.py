"""SnapFrame product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders of the size M frame: galvanized EMT tubes with colour
bands at their ends, teal printed nodes with filleted cores and socket mouths, stainless spring
buttons showing in their socket holes, hitch pins with pull rings at the tension joints, push-in caps
on the blank corner sockets, foot plates with grip ribs and a size mark, screw anchors, brace cables
with hand cam tensioners, and guy lines with slide tensioners. Context is a compact soil plinth, one
relief tarpaulin fitted over the rear bay (agency stock, item 11, outside the kit) and the shared clay
mannequin standing beside the open front gable for scale.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension, node position, socket axis, bore, button and pin position comes from
cad/src/model.py (SIZES, NODE, TUBES, geometry(), node_variants(), screw_anchor()). Axes as model.py:
X along the ridge, Y across the span, Z up, ground at Z = 0, front gable at X = 4000 mm.

The front right corner eave node and the ends of its three tubes form the "internal" group, so the
"detail" view can frame that one joint. The guy lines and their anchors are in the "accessory"
group, so the hero stays compact; see docs/REVIEW.md, session 2026-09-26.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))

from build123d import Box, Cylinder, Face, Plane, Pos, Rot, Solid, Sphere, Torus, Vector, Wire, fillet
import model as M
from model import NODE, TUBES, TUBE_OF, Socket, bore_of, sock_r_of, _perp

SIZE = "M"

TITLE = "SnapFrame: tool-free emergency shelter frame of conduit and printed nodes"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 24, "az": -40,
     "note": "Product render from the front right and above (about 24 deg elevation); size M frame on a soil "
             "plinth with a tarpaulin over the rear bay, the open front gable at right and a 1.75 m person "
             "for scale. Guy lines not shown"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): EMT posts, rafters, ridge "
             "and eave tubes; foot, eave and ridge nodes; brace cables; screw anchors; guy lines. "
             "Tarpaulin not shown"},
    {"name": "detail", "groups": ["internal"], "explode": False, "el": 18, "az": -40,
     "note": "Detail from the front right, slightly above (about 18 deg elevation): front right corner eave "
             "node with the post, rafter and eave tube ends, spring buttons, hitch pin, blank socket cap "
             "and brace cable hook"},
]

# Render layout
DETAIL_KEY = ("xl", -1)        # front right corner eave node (X = 4000, Y = -2000)
STUB = 300.0                   # tube length from the detail node centre kept in the "internal" group
PERSON_AT = (4750.0, -1250.0)  # mannequin pelvis over this point, beside the open front gable
PERSON_ROT = 40.0              # turned toward the camera
PLINTH = (-450.0, 5350.0, -2650.0, 2550.0, 420.0)   # x0, x1, y0, y1, depth
EXPLODE_K = 0.38
EXPLODE_C = Vector(2000.0, 0.0, 1300.0)

# Colours (restrained product palette; kit accent for the printed nodes)
C_TUBE = "#BCC2C9"        # galvanized EMT
C_NODE = "#0F766E"
C_STEEL = "#D3D7DC"       # stainless buttons, pins
C_GALV = "#9EA5AD"        # anchors
C_CABLE = "#7A828C"
C_DARK = "#23272E"
C_CAP = "#1F2937"
C_MARK = "#E7E9EC"
C_BAND = {"post": "#C98A1B", "rafter": "#3B5B8C", "ridge": "#7E3B3B", "eave": "#5B7A2E"}
C_ROPE = "#C9A23A"
C_TAPE = "#E8ECEF"
C_TARP = "#3F6E8F"
C_HEM = "#2F5570"
C_SOIL = "#CFC7B8"
C_CLAY = "#9CA3AF"


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _V(p):
    return Vector(*p)


def _cyl_on(origin, direction, r, length):
    """Cylinder of radius r from `origin` along `direction` for `length`."""
    d = _V(direction).normalized()
    return Solid.make_cylinder(r, length, Plane(origin=_V(origin), z_dir=d))


def _ring_on(origin, direction, r_out, r_in, length):
    return _cyl_on(origin, direction, r_out, length) - _cyl_on(origin - _V(direction).normalized(), direction,
                                                               r_in, length + 2)


def _tube_span(a, b, kind, t0, t1):
    """EMT tube along a to b between distances t0 and t1 from a (same section as model.tube)."""
    a, b = _V(a), _V(b)
    u = (b - a).normalized()
    t = TUBES[TUBE_OF[kind]]
    return _ring_on(a + u * t0, u, t["od"] / 2, t["od"] / 2 - t["wall"], t1 - t0)


def _band(a, b, kind, t0, width=40.0):
    """Colour band (painted) on a tube, starting t0 from a toward b."""
    a, b = _V(a), _V(b)
    u = (b - a).normalized()
    r = TUBES[TUBE_OF[kind]]["od"] / 2
    return _ring_on(a + u * t0, u, r + 0.35, r - 0.2, width)


def _rotz(v, deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return Vector(c * v.X - s * v.Y, s * v.X + c * v.Y, v.Z)


def _d(a, b):
    return (b[0] - a[0], b[1] - a[1], b[2] - a[2])


def _sockets(f):
    """Socket lists of each node variant, as model.node_variants() builds them."""
    x0 = f.xs[0]
    foot = [Socket(_d(f.foot[(x0, 1)], f.eave[(x0, 1)]), "post", True)]
    eave = [Socket(_d(f.eave[(x0, 1)], f.foot[(x0, 1)]), "post", True),
            Socket(_d(f.eave[(x0, 1)], f.ridge[x0]), "rafter"), Socket((1, 0, 0), "eave"),
            Socket((-1, 0, 0), "eave")]
    ridge_e = [Socket(_d(f.ridge[x0], f.eave[(x0, -1)]), "rafter"),
               Socket(_d(f.ridge[x0], f.eave[(x0, 1)]), "rafter"), Socket((1, 0, 0), "ridge")]
    return {"foot": foot, "eave": eave, "ridge-end": ridge_e,
            "ridge-middle": ridge_e + [Socket((-1, 0, 0), "ridge")]}


def _finish_node(shape, foot=False):
    """Appearance fillets on a model.py node: core-to-socket junctions, socket mouths, foot plate."""
    n = NODE
    junction = [e for e in shape.edges() if abs(e.position_at(0.5).length - n["core_r"]) < 0.6]
    shape = _fillet_try(shape, junction, [6.0, 4.0, 2.5])
    mouths = []
    for e in shape.edges():
        p = e.position_at(0.5)
        for kind in ("post", "rafter"):
            if abs(p.length - math.hypot(n["sock_l"], sock_r_of(kind))) < 0.3:
                mouths.append(e)
                break
    shape = _fillet_try(shape, mouths, [1.8, 1.2, 0.8])
    if foot:
        z0 = -n["z_foot"]
        h = n["plate"] / 2
        vert = [e for e in shape.edges() if abs(e.position_at(0.5).Z - (z0 + n["plate_t"] / 2)) < 0.5
                and abs(abs(e.position_at(0.5).X) - h) < 0.5 and abs(abs(e.position_at(0.5).Y) - h) < 0.5]
        shape = _fillet_try(shape, vert, [12.0, 8.0, 5.0])
        top = [e for e in shape.edges() if abs(e.position_at(0.5).Z - (z0 + n["plate_t"])) < 0.3
               and max(abs(e.position_at(0.5).X), abs(e.position_at(0.5).Y)) > h - 14]
        shape = _fillet_try(shape, top, [2.5, 1.5, 1.0])
    return shape


def _node_hardware(sockets, blank_dirs=()):
    """Spring buttons in every tube socket and hitch pins at pinned sockets, node-local coordinates."""
    n = NODE
    buttons, pins = None, None
    for sk in sockets:
        u = _V(sk.direction).normalized()
        if any((u - _V(b)).length < 1e-6 for b in blank_dirs):
            continue
        w = _perp(u)
        rs = sock_r_of(sk.kind)
        at = u * (n["tube_gap"] + n["button_at"])
        b = _cyl_on(at + w * (rs - 3.0), w, n["button_d"] / 2 - 0.4, 3.6)
        b += Pos(*(at + w * (rs + 0.6))) * Sphere(n["button_d"] / 2 - 0.4)
        b = b & _cyl_on(at, w, n["button_d"], rs + 2.2)
        buttons = b if buttons is None else buttons + b
        if sk.pinned:
            at_p = u * (n["tube_gap"] + n["pin_at"])
            ln = 2 * rs + 16
            p = _cyl_on(at_p - w * (ln / 2), w, n["pin_d"] / 2 - 0.4, ln)
            p += _cyl_on(at_p - w * (rs + 1.0), -w, 6.0, 5.0)          # head
            ring_c = at_p - w * (rs + 16.5)
            ring = Plane(origin=ring_c, z_dir=u.cross(w)) * Torus(13.0, 2.2)
            p = p + ring
            pins = p if pins is None else pins + p
    return buttons, pins


def _tag(k):
    """Readable position tag: frame line in m along the ridge, and side A (Y < 0) or B (Y > 0)."""
    if isinstance(k, tuple):
        return f"{k[0] / 1000:g} m, side {'A' if k[1] < 0 else 'B'}"
    return f"{k / 1000:g} m"


def _placed(shape, at, rz):
    return Pos(*at) * Rot(0, 0, rz) * shape


def _panel(pts, normal, off=60.0, t=8.0):
    nv = _V(normal).normalized()
    ps = [_V(p) + nv * off for p in pts]
    return Solid.extrude(Face(Wire.make_polygon(ps, close=True)), nv * t)


def _boff(center, extra=(0, 0, 0)):
    c = _V(center)
    return tuple(EXPLODE_K * (a - b) + e for a, b, e in zip(c, EXPLODE_C, extra))


def product_parts(size=SIZE):
    f = M.geometry(size)
    p = f.p
    x0, xl = f.xs[0], f.xs[-1]
    ye = p["span"] / 2
    dk = (xl, -1)
    dn = f.eave[dk]                                   # detail node centre
    out = []

    def add(name, shape, color, material, bom, group, explode=(0, 0, 0)):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # ------------------------------------------------------------ EMT members (BOM 1 to 4)
    members = {"post": [], "rafter": [], "ridge": [], "eave": []}
    for k in f.foot:
        members["post"].append((f.foot[k], f.eave[k]))
    for k in f.eave:
        members["rafter"].append((f.eave[k], f.ridge[k[0]]))
    for i in range(len(f.xs) - 1):
        members["ridge"].append((f.ridge[f.xs[i]], f.ridge[f.xs[i + 1]]))
        for s in (-1, 1):
            members["eave"].append((f.eave[(f.xs[i], s)], f.eave[(f.xs[i + 1], s)]))
    names = {"post": ("EMT posts, 3/4 in", 1), "rafter": ("EMT rafters, 1 in", 2),
             "ridge": ("EMT ridge tubes, 1 in", 3), "eave": ("EMT eave tubes, 3/4 in", 4)}
    gap, band_at = NODE["tube_gap"], NODE["sock_l"] + 8.0
    for kind, lst in members.items():
        label, bom = names[kind]
        for i, (a, b) in enumerate(lst):
            ln = math.dist(a, b)
            mid = tuple((q + r) / 2 for q, r in zip(a, b))
            off = _boff(mid)
            t0, t1 = gap, ln - gap
            bands = [(a, b, band_at), (b, a, band_at)]
            if dn in (a, b):                              # split off the stub at the detail node
                if a == dn:
                    stub, rest = _tube_span(a, b, kind, t0, STUB), _tube_span(a, b, kind, STUB, t1)
                    sb, rb = _band(a, b, kind, band_at), _band(b, a, kind, band_at)
                else:
                    stub, rest = _tube_span(a, b, kind, ln - STUB, t1), _tube_span(a, b, kind, t0, ln - STUB)
                    sb, rb = _band(b, a, kind, band_at), _band(a, b, kind, band_at)
                add(f"{label}, end at the front corner", stub, C_TUBE, "metal", bom, "internal", off)
                add(f"{label}, colour band at the front corner", sb, C_BAND[kind], "painted", bom, "internal", off)
                add(f"{label} ({i + 1})", rest, C_TUBE, "metal", bom, "shell", off)
                add(f"{label}, colour band ({i + 1})", rb, C_BAND[kind], "painted", bom, "shell", off)
                continue
            add(f"{label} ({i + 1})", _tube_span(a, b, kind, t0, t1), C_TUBE, "metal", bom, "shell", off)
            bs = _band(*bands[0][:2], kind, band_at) + _band(*bands[1][:2], kind, band_at)
            add(f"{label}, colour bands ({i + 1})", bs, C_BAND[kind], "painted", bom, "shell", off)

    # ------------------------------------------------------------ printed nodes (BOM 5 to 7, 12)
    var = M.node_variants(size)
    socks = _sockets(f)
    fin = {nm: _finish_node(sh, foot=(nm == "foot")) for nm, (sh, _, _) in var.items()}

    # foot plate grip ribs and size mark (thin raised parts, node-local)
    zt = -NODE["z_foot"] + NODE["plate_t"]
    ribs = None
    for j in range(4):
        yy = -NODE["plate"] / 2 + 16 + j * 5.0
        r = Pos(0, yy, zt + 0.5) * Box(NODE["plate"] - 50, 2.0, 1.0)
        ribs = r if ribs is None else ribs + r
    mark = Pos(-50, 50, zt + 0.4) * Box(34, 20, 0.8)

    node_list = []                                     # (variant, key, at, rz, bom, label)
    for k in f.foot:
        node_list.append(("foot", k, f.foot[k], 0 if k[1] > 0 else 180, 5, "Foot node"))
    for k in f.eave:
        node_list.append(("eave", k, f.eave[k], 0 if k[1] > 0 else 180, 6, "Eave node"))
    for x in f.xs:
        if x == x0:
            node_list.append(("ridge-end", x, f.ridge[x], 0, 7, "Ridge node, end"))
        elif x == xl:
            node_list.append(("ridge-end", x, f.ridge[x], 180, 7, "Ridge node, end"))
        else:
            node_list.append(("ridge-middle", x, f.ridge[x], 0, 7, "Ridge node, middle"))

    for vn, k, at, rz, bom, label in node_list:
        is_d = vn == "eave" and k == dk
        grp = "internal" if is_d else "shell"
        tag = "front right corner" if is_d else _tag(k)
        off = _boff(at)
        add(f"{label} ({tag})", _placed(fin[vn], at, rz), C_NODE, "plastic", bom, grp, off)
        blank_local = []
        if vn == "eave" and k[0] in (x0, xl):
            wdir = Vector(-1 if k[0] == x0 else 1, 0, 0)
            ldir = _rotz(wdir, -rz)
            blank_local = [(round(ldir.X), round(ldir.Y), round(ldir.Z))]
            cap = _cyl_on(wdir * (NODE["sock_l"] - 14), wdir, bore_of("eave") / 2 - 0.2, 14.5)
            cap += _cyl_on(wdir * NODE["sock_l"], wdir, sock_r_of("eave") + 1.2, 6.0)
            cap = _fillet_try(cap, [e for e in cap.edges()
                                    if abs(e.position_at(0.5).dot(wdir) - NODE["sock_l"] - 6.0) < 0.2],
                              [2.0, 1.2])
            for g in range(6):                          # grip ribs round the flange
                ang = g * 60.0
                v = Vector(0, math.cos(math.radians(ang)), math.sin(math.radians(ang)))
                cap += Pos(*(wdir * (NODE["sock_l"] + 3.0) + v * (sock_r_of("eave") + 1.2))) \
                    * Box(5.0, 2.4, 2.4)
            add(f"Socket cap ({tag})", Pos(*at) * cap, C_CAP, "rubber", 12, grp,
                tuple(o + e for o, e in zip(off, (wdir * 90))))
        bt, pn = _node_hardware(socks[vn], blank_local)
        add(f"Spring buttons ({tag})", _placed(bt, at, rz), C_STEEL, "metal", 12, grp, off)
        if pn is not None:
            pw = _rotz(_perp(_V(socks[vn][0].direction).normalized()), rz)
            add(f"Hitch pin with ring ({tag})", _placed(pn, at, rz), C_STEEL, "metal", 12, grp,
                tuple(o + e for o, e in zip(off, (pw * -80))))
        if vn == "foot":
            add(f"Foot plate grip ribs and size mark ({tag})", _placed(ribs + mark, at, rz), C_MARK, "painted",
                5, "shell", off)

    # ------------------------------------------------------------ brace cables (BOM 8)
    fo, ea, ri = f.foot, f.eave, f.ridge
    xm = f.xs[1]
    cables = [(fo[(x0, -1)], ea[(x0, 1)]), (fo[(x0, 1)], ea[(x0, -1)])]
    for s in (-1, 1):
        cables += [(fo[(x0, s)], ea[(xm, s)]), (fo[(xl, s)], ea[(f.xs[-2], s)])]
        cables += [(ea[(x0, s)], ri[xm]), (ea[(xl, s)], ri[f.xs[-2]])]
    for i, (a, b) in enumerate(cables):
        a, b = _V(a), _V(b)
        u = (b - a).normalized()
        ln = (b - a).length
        off = _boff(((a + b) * 0.5))
        start = NODE["core_r"] - 4 if a != _V(dn) else NODE["core_r"] + 48
        wire = _cyl_on(a + u * start, u, M.CABLE_R, ln - start - NODE["core_r"] + 4)
        add(f"Brace cable ({i + 1})", wire, C_CABLE, "metal", 8, "shell", off)
        # hand cam tensioner and swaged sleeves near the lower end
        tc = a + u * (0.18 * ln)
        body = Plane(origin=tc, z_dir=u, x_dir=_perp(u)) * Box(18, 14, 70)
        body = _fillet_try(body, body.edges(), [3.0, 2.0, 1.0])
        lever = Plane(origin=tc + _perp(u) * 10, z_dir=u, x_dir=_perp(u)) * Box(4, 10, 56)
        sl = _cyl_on(tc + u * 50, u, 4.0, 22) + _cyl_on(tc - u * 72, u, 4.0, 22)
        add(f"Cable tensioner ({i + 1})", body + lever, C_DARK, "plastic", 8, "shell", off)
        add(f"Cable sleeves ({i + 1})", sl, C_STEEL, "metal", 8, "shell", off)

    # snap hook of the rafter-plane cable on the detail node's tab (appearance only)
    tab_l = _rotz(Vector(0, 1, -1).normalized(), 180)
    eye = _V(dn) + tab_l * (NODE["core_r"] + 22)
    eax = _perp(Vector(0, 1, -1).normalized())
    eax = _rotz(eax, 180)
    hook = Plane(origin=eye + tab_l * 6, z_dir=tab_l.cross(eax)) * Torus(11.0, 2.0)
    tail = ri[f.xs[-2]]
    tu = (_V(tail) - (eye + tab_l * 17)).normalized()
    hook += _cyl_on(eye + tab_l * 15, tu, 3.5, 30)
    add("Brace cable snap hook (front right corner)", hook, C_STEEL, "metal", 8, "internal", _boff(dn))

    # ------------------------------------------------------------ screw anchors (BOM 9)
    offa = NODE["anchor_off"]
    for k in f.foot:
        ax, ay = f.foot[k][0], f.foot[k][1] + k[1] * offa
        sh = M.screw_anchor(ax, ay)
        add(f"Screw ground anchor ({_tag(k)})", sh, C_GALV, "metal", 9, "shell", _boff(f.foot[k], (0, 0, -700)))

    # ------------------------------------------------------------ guy lines (BOM 9, 10), accessory group
    h = p["ridge"]
    for nm, (gx, sx) in {"rear": (x0 - M.GUY_OUT, -1), "front": (xl + M.GUY_OUT, 1)}.items():
        top = Vector((x0 if sx < 0 else xl) + sx * 60, 0, h + 20)
        bot = Vector(gx, 0, 80)
        u = (bot - top).normalized()
        ln = (bot - top).length
        off = _boff(((top + bot) * 0.5), (0, 0, 250))
        rope = _cyl_on(top, u, 3.0, ln)
        add(f"Guy line, {nm}", rope, C_ROPE, "fabric", 10, "accessory", off)
        tc = top + u * (0.7 * ln)
        ten = Plane(origin=tc, z_dir=u, x_dir=Vector(0, 1, 0)) * Box(22, 10, 60)
        ten = _fillet_try(ten, ten.edges(), [3.0, 2.0])
        add(f"Guy line slide tensioner, {nm}", ten, C_DARK, "plastic", 10, "accessory", off)
        tape = _ring_on(top + u * (0.35 * ln), u, 3.6, 2.5, 120)
        add(f"Guy line reflective tape, {nm}", tape, C_TAPE, "painted", 10, "accessory", off)
        add(f"Guy anchor, {nm}", M.screw_anchor(gx, 0.0), C_GALV, "metal", 9, "accessory",
            _boff((gx, 0, 0), (0, 0, -700)))

    # ------------------------------------------------------------ context (not in the kit)
    px0, px1, py0, py1, pd = PLINTH
    plinth = Pos((px0 + px1) / 2, (py0 + py1) / 2, -pd / 2) * Box(px1 - px0, py1 - py0, pd)
    plinth = _fillet_try(plinth, [e for e in plinth.edges() if abs(e.position_at(0.5).Z) < 0.5], [10.0, 5.0])
    add("Ground plinth (soil)", plinth, C_SOIL, "paper", None, "context")

    # tarpaulin over the rear bay, as concept_media.py (agency stock, item 11)
    he, hr, bay = p["eave"], p["ridge"], p["bay"]
    sl_ = math.atan2(hr - he, ye)
    nr = (0, math.sin(sl_), math.cos(sl_))
    nl = (0, -math.sin(sl_), math.cos(sl_))
    roof_r = [(-80, ye + 150, he - 60), (bay, ye + 150, he - 60), (bay, -40, hr + 16), (-80, -40, hr + 16)]
    roof_l = [(-80, -ye - 150, he - 60), (bay, -ye - 150, he - 60), (bay, 40, hr + 16), (-80, 40, hr + 16)]
    tarp = (_panel(roof_r, nr) + _panel(roof_l, nl)
            + _panel([(0, ye, 10), (bay, ye, 10), (bay, ye, he), (0, ye, he)], (0, 1, 0))
            + _panel([(0, -ye, 10), (bay, -ye, 10), (bay, -ye, he), (0, -ye, he)], (0, -1, 0))
            + _panel([(0, -ye, 10), (0, ye, 10), (0, ye, he), (0, 0, hr), (0, -ye, he)], (-1, 0, 0)))
    add("Tarpaulin, rear bay (agency stock)", tarp, C_TARP, "fabric", 11, "context")
    # hem along the open front edge of the tarpaulin, and eyelets along the eaves
    hem = (_panel([(bay - 50, -ye - 150, he - 60), (bay, -ye - 150, he - 60), (bay, 40, hr + 16),
                   (bay - 50, 40, hr + 16)], nl, off=68.0, t=1.5)
           + _panel([(bay - 50, -ye, 10), (bay, -ye, 10), (bay, -ye, he), (bay - 50, -ye, he)], (0, -1, 0),
                    off=68.0, t=1.5))
    add("Tarpaulin hem", hem, C_HEM, "fabric", 11, "context")
    lv = Vector(0, -math.cos(sl_), math.sin(sl_))      # up the left roof slope
    eyes = None
    for j in range(5):
        xx = -40 + j * (bay + 40) / 4.5
        c = _V((xx, -ye - 150, he - 60)) + _V(nl) * 69 + lv * 30
        e = _ring_on(c, _V(nl), 11.0, 6.5, 2.5)
        eyes = e if eyes is None else eyes + e
    add("Tarpaulin eyelets", eyes, C_STEEL, "metal", 11, "context")

    from context_parts import mannequin
    person = Pos(PERSON_AT[0], PERSON_AT[1], 0) * Rot(0, 0, PERSON_ROT) * mannequin(1750, "stand")
    add("Person, 1.75 m (clay mannequin)", person, C_CLAY, "clay", None, "context")
    return out


if __name__ == "__main__":
    for q in product_parts():
        s = q["shape"]
        print(f"{q['name']:52s} {q['group']:9s} {q['material']:8s} valid={s.is_valid}")
