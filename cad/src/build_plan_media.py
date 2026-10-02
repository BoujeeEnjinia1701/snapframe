"""SnapFrame prototype build plan pictures (SNF-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|tubes|cables|joints|steps ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/SNF-DWG-101 to 109        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/cable-assembly.png  how a brace cable is made up (matplotlib, also on SNF-DWG-109)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
import model as M  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
SIZE = "M"

# tessellate each shape once: the same shapes appear in many pictures
_cache = {}
GROUPS = {}
_tris0 = bv._tris


def _tris_cached(shape, tol=1.0):
    import numpy as np
    from build123d import Compound
    if id(shape) in GROUPS:
        vs, ts, n = [], [], 0
        for ch in GROUPS[id(shape)][1]:
            v, t = _tris_cached(ch, tol)
            if len(t):
                vs.append(v); ts.append(t + n); n += len(v)
        if vs:
            return np.vstack(vs), np.vstack(ts)
    k = id(shape)
    if k not in _cache:
        _cache[k] = (_tris0(shape, tol), shape)
    return _cache[k][0]


bv._tris = _tris_cached

# leader end points chosen by hand for parts whose automatic point would mislead (part name -> 3D point)
LEAD = {}
_draw0 = bv._draw_labels


def _draw_lead(ax, proj, pts, names, W, H, numbers=None):
    import numpy as np
    pts = [np.asarray(LEAD[n], float) if n in LEAD else p for p, n in zip(pts, names)]
    LEAD.clear()                     # each picture sets its own leader points
    return _draw0(ax, proj, pts, names, W, H, numbers)


bv._draw_labels = _draw_lead


class AsShown(float):
    """Title block scale for a sheet whose views are at two scales: prints as '1:10 and 2:1'."""
    def __new__(cls, text):
        o = float.__new__(cls, 0.5); o.text = text; return o

    def __lt__(self, other):
        return True

    def __rtruediv__(self, other):
        t = self.text

        class _F:
            def __format__(self, spec):
                return t
        return _F()

C, LEN = M.comps(SIZE)
F, NODES, MEMBERS = M.layout(SIZE)
X0, XM, XL = F.xs[0], F.xs[1], F.xs[-1]
YE = F.p["span"] / 2
ML = M.member_lengths(SIZE)
CL = {k: v - 2 * M.HOOK_L for k, v in LEN.items()}

def thick(pred, r=9.0):
    """Cables and guys redrawn as thicker rods between their attachment points, so they show in
    whole-frame pictures (their true diameter is 4 and 6 mm)."""
    out = []
    for k, (a, b) in M.CABLE_ENDS.items():
        if pred(("cable",) + k):
            out.append(M.rod(a, b, r))
    return fuse(out)


COL = {"post": "#0E7490", "rafter": "#B45309", "ridge": "#7C3AED", "eave": "#1D4ED8",
       "foot": "#0F766E", "eavenode": "#16A34A", "ridgenode": "#15803D", "bolt": "#111827", "ring": "#D4A017",
       "anchor": "#92400E", "cable": "#374151", "guy": "#D97706", "cap": "#DC2626", "pin": "#1F2937",
       "button": "#6B7280", "spring": "#C2410C", "hook": "#4B5563", "ground": "#E7E5E4"}


GROUPS = {}


def fuse(shapes):
    """Group shapes for drawing without a boolean union (much faster on hollow, drilled parts).
    The members are remembered so each is tessellated once, however many pictures it is in."""
    from build123d import Compound
    sh = [x for x in shapes if x is not None]
    if len(sh) == 1:
        return sh[0]
    c = Compound(sh)
    GROUPS[id(c)] = (c, sh)
    return c


def sel(pred):
    return [c for k, c in C.items() if pred(k)]


def S(pred):
    return fuse(c.shape for c in sel(pred))


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def ground(x0=-700, x1=4700, y0=-2700, y1=2700, z=-1.0):
    from build123d import Box, Pos
    return part("Ground", Pos((x0 + x1) / 2, (y0 + y1) / 2, z - 4) * Box(x1 - x0, y1 - y0, 8), COL["ground"])


def frame_line(x):
    """Every part of one gable frame at frame line x: posts, eave nodes, rafters, ridge node, feet, pins, buttons, caps, bolts."""
    def f(k):
        if k[0] == "node":
            return (k[1] in ("foot", "eave") and k[2] == x) or (k[1] == "ridge" and k[2] == x)
        if k[0] == "tube":
            return k[1] in ("post", "rafter") and k[2] == x
        if k[0] in ("pin", "button"):
            return k[1] in ("post", "rafter") and k[2] == x
        if k[0] == "cap":
            return k[2] == x
        if k[0] in ("bolt", "ring"):
            return (k[1] == "eave" and k[2] == x) or (k[1] == "ridge" and k[2] == x)
        return False
    return f


def is_tube(kind, x=None):
    return lambda k: k[0] == "tube" and k[1] == kind and (x is None or k[2] == x)


def is_node(kind, x=None):
    return lambda k: k[0] == "node" and k[1] == kind and (x is None or k[2] == x)


# ----------------------------------------------------------------- overview
def overview():
    groups = [
        ("Foot nodes (6), with hitch pins", lambda k: is_node("foot")(k) or (k[0] == "pin" and k[-1][0] == "foot"), COL["foot"], (0, 0, -700)),
        ("Posts (6), snap buttons inside", is_tube("post"), COL["post"], (0, 0, -250)),
        ("Eave nodes (6) with cable bolts and rings; caps (4)", lambda k: is_node("eave")(k) or (k[0] in ("bolt", "ring") and k[1] == "eave")
         or (k[0] == "pin" and k[-1][0] == "eave") or k[0] == "cap", COL["eavenode"], (0, 0, 250)),
        ("Rafters (6)", is_tube("rafter"), COL["rafter"], (0, 0, 650)),
        ("Ridge nodes (3), cable bolts and rings", lambda k: is_node("ridge")(k) or (k[0] in ("bolt", "ring") and k[1] == "ridge"),
         COL["ridgenode"], (0, 0, 1100)),
        ("Eave tubes (4)", is_tube("eave"), COL["eave"], (0, 0, 450)),
        ("Ridge tubes (2)", is_tube("ridge"), COL["ridge"], (0, 0, 1350)),
        ("Screw anchors (6 at the feet)", lambda k: k[0] == "anchor" and k[1] not in ("rear", "front"), COL["anchor"], (0, 0, -1150)),
        ("Brace cables (10) with snap hooks", lambda k: k[0] in ("cable", "hook") and k[1] != "guy", COL["cable"], (0, 0, 0)),
        ("Guy lines (2) and guy anchors (2)", lambda k: (k[0] in ("cable", "hook") and k[1] == "guy") or (k[0] == "anchor" and k[1] in ("rear", "front")),
         COL["guy"], (0, 0, 0)),
    ]
    parts = []
    for n, p, c, e in groups:
        sh = S(p)
        if "Brace cables" in n:
            sh = thick(lambda k: k[1] != "guy")
        if "Guy lines" in n:
            sh = fuse([thick(lambda k: k[1] == "guy"), S(lambda k: k[0] == "anchor" and k[1] in ("rear", "front"))])
        parts.append(part(n, sh, c, e))
    return bv.overview(parts, OUT / "overview.png", "SnapFrame size M prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Cables drawn thicker than they are; snap buttons sit inside the tube ends; tarpaulins not shown",
                       elev=20, azim=-62, size=(11, 8.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches: nodes
def node_local(v):
    return M.node_variants(SIZE)[v][0]


def hardware_local(v):
    """Cable bolt and ring of a node variant, in node coordinates, for the sheet views."""
    a = M.V(*M.BOLT_DIR["eave" if v == "eave" else "ridge"])
    return M.cable_bolt(a)


def near(parts, key, half=380):
    """Neighbours cut down to a box round a node, so the inset shows the node large enough to see."""
    c = NODES[key][1]
    return [part(p.name, win(p.shape, c, (half, half, half)), p.color) for p in parts]


def node_sheets():
    base = dict(project="SnapFrame", date=DATE)
    out = []
    feet_ctx = [part("Post", S(is_tube("post", X0)), COL["post"]), part("Anchor", S(lambda k: k[0] == "anchor" and k[1] == (X0, -1)), COL["anchor"])]
    n = M.NODE
    out.append(bv.component_sheet(
        Part("Foot node", C[("node", "foot", X0, -1)].shape, COL["foot"]),
        near([part("Post", C[("tube", "post", X0, -1)].shape, COL["post"]), part("Anchor", C[("anchor", (X0, -1))].shape, COL["anchor"])], ("foot", X0, -1), half=200),
        dwg_no="SNF-DWG-101", title="SnapFrame foot node (make 6): making sketch",
        material="Printed polymer (to be chosen, ASA class assumed), about 410 g",
        view_shape=node_local("foot"), inset_view=(30, -40),
        notes=["Print 6, plate down on the bed; supports under the core only.",
               "Plate 170 x 170 x 12 mm; core 84 mm ball, its centre 60 mm up.",
               "One socket straight up: bore 24.0 mm, 65 mm deep to a flat stop;",
               "  1.5 mm chamfer at the mouth so the button rides in.",
               "Button hole 6 mm, 85 mm above the core centre, on the outboard",
               "  side, in a 16 mm finger recess with 1.5 mm of wall left.",
               "Hitch pin hole 8 mm right through, 60 mm above the core centre,",
               "  in line with the button hole.",
               "Two anchor slots 18 mm wide at 45 degrees either side of the",
               "  outboard side, round-ended 62 mm from the centre, open at",
               "  the corners. The anchor uses the slot that points away from",
               "  the shelter's middle (rear feet backward, front feet forward).",
               "Check: a post end slides in to the stop with the button pressed."],
        **base))
    eave_ctx = [part("Post", C[("tube", "post", X0, -1)].shape, COL["post"]),
                part("Rafter", C[("tube", "rafter", X0, -1)].shape, COL["rafter"]),
                part("Eave tube", C[("tube", "eave", 0, -1)].shape, COL["eave"]),
                part("Cable bolt", C[("bolt", "eave", X0, -1)].shape, COL["bolt"])]
    out.append(bv.component_sheet(
        Part("Eave node", C[("node", "eave", X0, -1)].shape, COL["eavenode"]), near(eave_ctx, ("eave", X0, -1)),
        dwg_no="SNF-DWG-103", title="SnapFrame eave node (make 6): making sketch",
        material="Printed polymer (to be chosen), about 256 g; M10 cable bolt set",
        view_shape=fuse([node_local("eave"), hardware_local("eave")]), inset_view=(18, -35),
        notes=["Print 6, all the same. Four sockets from the 84 mm core:",
               "  post straight down (24.0 bore, hitch pin 60 mm from the centre);",
               "  rafter inward and up 21.8 degrees (30.1 bore);",
               "  two eave tube sockets along the ridge line (24.0 bore).",
               "Every bore 65 mm deep to a flat stop, 1.5 mm mouth chamfer, 6 mm",
               "  button hole 85 mm out in a 16 mm finger recess.",
               "Cable bolt hole 10.5 mm through the centre, pointing inward and",
               "  35 degrees down; flat spot face 39 mm out on that side, 27 mm",
               "  nut recess on the far side, its floor 22 mm from the centre.",
               "Fit: 30 mm washer, 14 x 10 mm spacer with the 6 mm ring on it,",
               "  24 mm washer, M10 x 90 bolt; 20 mm washer and nyloc nut in the",
               "  recess. Snug plus a quarter turn: do not crush the print.",
               "At the four corners the socket past the gable takes a cap."],
        **base))
    ridge_ctx = [part("Rafters", S(is_tube("rafter", X0)), COL["rafter"]),
                 part("Ridge tube", C[("tube", "ridge", 0)].shape, COL["ridge"]),
                 part("Cable bolt", C[("bolt", "ridge", X0)].shape, COL["bolt"])]
    out.append(bv.component_sheet(
        Part("Ridge node, end", C[("node", "ridge", X0)].shape, COL["ridgenode"]), near(ridge_ctx, ("ridge", X0)),
        dwg_no="SNF-DWG-105", title="SnapFrame ridge node, end (make 2): making sketch",
        material="Printed polymer (to be chosen), about 247 g; M10 cable bolt set",
        view_shape=fuse([node_local("ridge-end"), hardware_local("ridge")]), inset_view=(25, -50),
        notes=["Print 2, the same for the rear and the front (the front one is",
               "  turned round). Three 30.1 mm sockets from the 84 mm core:",
               "  two rafters, each 21.8 degrees below level, out to the sides;",
               "  one ridge tube along the ridge line, toward the middle frame.",
               "Bores 65 mm deep to a flat stop, 1.5 mm mouth chamfer, 6 mm",
               "  button hole 85 mm out in a 16 mm finger recess.",
               "Cable bolt hole 10.5 mm straight down through the centre: spot face",
               "  on the underside, nut recess on top so nothing stands proud",
               "  under the roof tarpaulin.",
               "Same bolt set as the eave node. The guy line ties to its ring.",
               "Check: the ring swings freely on the spacer."],
        **base))
    mid_ctx = [part("Rafters", S(is_tube("rafter", XM)), COL["rafter"]),
               part("Ridge tubes", S(is_tube("ridge")), COL["ridge"]),
               part("Cable bolt", C[("bolt", "ridge", XM)].shape, COL["bolt"])]
    out.append(bv.component_sheet(
        Part("Ridge node, middle", C[("node", "ridge", XM)].shape, COL["ridgenode"]), near(mid_ctx, ("ridge", XM)),
        dwg_no="SNF-DWG-106", title="SnapFrame ridge node, middle (make 1): making sketch",
        material="Printed polymer (to be chosen), about 271 g; M10 cable bolt set",
        view_shape=fuse([node_local("ridge-middle"), hardware_local("ridge")]), inset_view=(25, -50),
        notes=["Print 1. As the end ridge node with a fourth socket: two",
               "  30.1 mm ridge sockets, one each way along the ridge line.",
               "Bores 65 mm deep to a flat stop, 1.5 mm mouth chamfer, 6 mm",
               "  button hole 85 mm out in a 16 mm finger recess.",
               "Cable bolt straight down; the four roof cables clip to its ring.",
               "Print on its side with supports; the box is 220 x 219 x 99 mm,",
               "  so the printer bed must be at least 230 mm.",
               "Check: each ridge tube slides in to the stop with the button",
               "  pressed, and the ring swings freely on the spacer."],
        **base))
    return out


# ----------------------------------------------------------------- making sketches: tubes
def tube_sheet(kind, dwg, count, title, material, notes, pinned=False):
    from build123d import Box, Pos
    from drawing import Sheet, project_views
    L = ML[kind]
    t = M.TUBES[M.TUBE_OF[kind]]
    full = M.tube((-M.NODE["tube_gap"], 0, 0), (L + M.NODE["tube_gap"], 0, 0), kind, (0, -1, 0), (0, 1, 0), pinned)
    seg = 55.0
    endA = full & (Pos(seg / 2, 0, 0) * Box(seg, 60, 60))
    endB = full & (Pos(L - seg / 2, 0, 0) * Box(seg, 60, 60))
    work = DWG / f"_{dwg}_views"
    vf = project_views(full, work / "full")
    va = project_views(endA, work / "a")
    vb = project_views(endB, work / "b")
    s = Sheet(project="SnapFrame", title=title, dwg_no=dwg, rev="P1", author="Amish Chadha", date=DATE,
              concept="BUILD PLAN SKETCH, PLAN NOT YET BUILT", scale=AsShown("10, ends 2:1"), material=material,
              revisions=[("P1", "Making sketch for the prototype build plan", DATE, "AC")])
    k_full = 0.1
    x0, y0 = 22.0, 44.0
    s.add_svg(vf["front"], x0, y0, scale=k_full, label="Whole tube, front view",
              sublabel="Scale 1:10; looking at the front (along +Y)")
    tl = (L + 0.35) * k_full
    s._dim(x0, y0, x0 + tl, y0, f"{L:.0f}", "above", off=6)
    k = 2.0
    ya = 104.0
    s.add_svg(va["front"], x0, ya, scale=k, label="End A detail, front view",
              sublabel="Scale 2:1; button hole facing you")
    s.add_svg(vb["front"], x0 + 128, ya, scale=k, label="End B detail, front view",
              sublabel="Scale 2:1; button hole on the far side")
    od = t["od"]
    hA = (od + 0.35) * k
    # end A: the tube end is at the left of its detail
    s._dim(x0, ya, x0 + M.NODE["button_at"] * k, ya, f"{M.NODE['button_at']:.0f}", "above", off=13)
    if pinned:
        s._dim(x0, ya, x0 + M.NODE["pin_at"] * k, ya, f"{M.NODE['pin_at']:.0f}", "above", off=5)
    s._dim(x0, ya, x0, ya + hA, f"{od:.2f}", "left", off=5)
    xb1 = x0 + 128 + (seg + 0.35) * k
    s._dim(xb1 - M.NODE["button_at"] * k, ya, xb1, ya, f"{M.NODE['button_at']:.0f}", "above", off=13)
    if pinned:
        s._dim(xb1 - M.NODE["pin_at"] * k, ya, xb1, ya, f"{M.NODE['pin_at']:.0f}", "above", off=5)
    mk, _, na, nbk = next(m for m in MEMBERS if m[1] == kind)
    nb = C[("tube",) + mk]
    others = S(lambda kk: kk[0] in ("tube", "node") and kk != nb.key)
    inset = bv.where_it_goes(Part(kind, nb.shape, COL[kind]), [Part("frame", others, "#D1D5DB")],
                             work / "where.png", elev=22, azim=-55)
    s.add_image(str(inset), 276, 30, 140, 70, label="Where it goes", sublabel="This part in colour, the rest of the frame in grey")
    s.add_notes("How to make it and how it fits", notes, x=276, y=112, width=140)
    s.save(DWG / dwg)
    shutil.rmtree(work, ignore_errors=True)
    return DWG / f"{dwg}.png"


def tube_sheets(only=None):
    out = []
    common = ["Saw square (a pipe cutter or a fine blade); deburr inside",
              "  and out with a reamer and a file, and wipe clean.",
              "Mark one line along the whole tube with a straight edge. Every hole",
              "  is on that line: the button hole at end A on the line, the button",
              "  hole at end B on the opposite side (turn the tube half a turn).",
              "Centre punch, drill 3 mm, then 6 mm for the button holes."]
    if not only or "post" in only:
      out.append(tube_sheet("post", "SNF-DWG-102", 6, "SnapFrame post (make 6): making sketch",
                          "3/4 in EMT, ANSI C80.3, OD 23.42 x 1.245 mm, one 3.05 m stick each", [
                              f"Cut 6 lengths of {ML['post']:.0f} mm from 3/4 in EMT.", *common,
                              "Hitch pin holes: 8 mm right through, 15 mm from each end,",
                              "  on the marked line (drill both walls in one pass in a vee",
                              "  block so the holes line up).",
                              "Paint a 40 mm colour band (post colour) at each end, starting",
                              "  70 mm in, so it shows beside the socket mouth.",
                              "Push a 3/4 in snap button into each end, V spring first, until",
                              "  the button clicks into its 6 mm hole.",
                              "Check: the end slides into a socket to the stop and clicks."], pinned=True))
    if not only or "rafter" in only:
      out.append(tube_sheet("rafter", "SNF-DWG-104", 6, "SnapFrame rafter (make 6): making sketch",
                          "1 in EMT, ANSI C80.3, OD 29.54 x 1.448 mm, one 3.05 m stick each", [
                              f"Cut 6 lengths of {ML['rafter']:.0f} mm from 1 in EMT.", *common,
                              "No hitch pin holes in the rafters.",
                              "Colour band (rafter colour) at each end, 70 mm in.",
                              "Fit a 1 in snap button in each end until it clicks.",
                              "Check: the end slides into an eave or ridge node socket",
                              "  to the stop and clicks; the other end's button faces the",
                              "  opposite way."]))
    if not only or "eave" in only:
      out.append(tube_sheet("eave", "SNF-DWG-107", 4, "SnapFrame eave tube (make 4): making sketch",
                          "3/4 in EMT, ANSI C80.3, OD 23.42 x 1.245 mm, one 3.05 m stick each", [
                              f"Cut 4 lengths of {ML['eave']:.0f} mm from 3/4 in EMT.", *common,
                              "No hitch pin holes in the eave tubes.",
                              "Colour band (eave colour) at each end, 70 mm in; it tells",
                              "  them from the posts, which are the same tube.",
                              "Fit a 3/4 in snap button in each end until it clicks.",
                              "Check: both ends click into eave node sockets."]))
    if not only or "ridge" in only:
      out.append(tube_sheet("ridge", "SNF-DWG-108", 2, "SnapFrame ridge tube (make 2): making sketch",
                          "1 in EMT, ANSI C80.3, OD 29.54 x 1.448 mm, one 3.05 m stick each", [
                              f"Cut 2 lengths of {ML['ridge']:.0f} mm from 1 in EMT.", *common,
                              "No hitch pin holes in the ridge tubes.",
                              "Colour band (ridge colour) at each end, 70 mm in; it tells",
                              "  them from the rafters, which are the same tube.",
                              "Fit a 1 in snap button in each end until it clicks.",
                              "Check: both ends click into ridge node sockets."]))
    return out


# ----------------------------------------------------------------- cables
def cable_picture(footer=True, out=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, Circle, Ellipse
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    fig = plt.figure(figsize=(11, 5.2), dpi=150)
    ax = fig.add_axes([0.02, 0.08, 0.96, 0.78]); ax.set_xlim(0, 110); ax.set_ylim(0, 40); ax.set_axis_off()
    fig.text(0.02, 0.965, "Brace cable: how one is made up", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.02, 0.92, "Not to scale. Eye to eye: from the inside of one end loop to the inside of the hand tensioner's eye, "
             "with the tensioner let right out.", fontsize=8.5, color=MUT, va="top")
    y = 26
    # snap hook A
    ax.add_patch(FancyBboxPatch((2, y - 2.2), 8, 4.4, boxstyle="round,pad=0.6", fc="white", ec=INK, lw=1.4))
    ax.text(6, y + 5.2, "Snap hook", ha="center", fontsize=8, color=INK)
    # thimble loop and clips
    ax.add_patch(Ellipse((14, y), 6, 4.2, fc="none", ec=INK, lw=1.6))
    ax.text(14, y - 5.4, "Loop round a thimble,\ntwo wire rope clips", ha="center", va="top", fontsize=7.5, color=INK)
    for xc in (19.5, 23):
        ax.add_patch(FancyBboxPatch((xc - 1, y - 1.6), 2, 3.2, boxstyle="round,pad=0.2", fc="#9CA3AF", ec=INK, lw=0.8))
    ax.plot([17, 70], [y + 0.5, y + 0.5], color=INK, lw=1.8)
    ax.plot([17, 25], [y - 0.5, y - 0.5], color=INK, lw=1.8)
    ax.text(45, y + 2.2, "4 mm galvanized 7x19 wire rope", ha="center", fontsize=8, color=INK)
    # tensioner
    ax.add_patch(FancyBboxPatch((70, y - 2.5), 12, 5, boxstyle="round,pad=0.4", fc="#E5E7EB", ec=INK, lw=1.2))
    ax.text(76, y, "Hand\ntensioner", ha="center", va="center", fontsize=7.5, color=INK)
    ax.plot([70, 66, 64], [y - 1.2, y - 3.5, y - 9], color=INK, lw=1.4)
    ax.text(62, y - 10, "300 mm tail, taped", ha="center", va="top", fontsize=7.5, color=MUT)
    ax.add_patch(Circle((85.5, y), 2.0, fc="none", ec=INK, lw=1.6))
    ax.add_patch(FancyBboxPatch((90, y - 2.2), 8, 4.4, boxstyle="round,pad=0.6", fc="white", ec=INK, lw=1.4))
    ax.text(94, y + 5.2, "Snap hook", ha="center", fontsize=8, color=INK)
    ax.annotate("", xy=(11.5, y + 9), xytext=(87.5, y + 9), arrowprops=dict(arrowstyle="<->", color=AC, lw=1.0))
    ax.text(49.5, y + 10, "eye to eye (table)", ha="center", va="bottom", fontsize=8, color=AC)
    rows = [("Rear gable cables", 2, CL[("gable", -1)], "anchor eye of a rear corner foot to the ring of the opposite rear eave node"),
            ("Side wall cables", 4, CL[("wall", X0, 1)], "anchor eye of a corner foot to the ring of the middle eave node on that side"),
            ("Roof cables", 4, max(v for k, v in CL.items() if k[0] == "roof"), "ring of a corner eave node to the ring of the middle ridge node")]
    ax.text(2, 11.5, "Cable", fontsize=8, fontweight="bold", color=INK)
    ax.text(22, 11.5, "Make", fontsize=8, fontweight="bold", color=INK)
    ax.text(30, 11.5, "Eye to eye", fontsize=8, fontweight="bold", color=INK)
    ax.text(44, 11.5, "Runs from", fontsize=8, fontweight="bold", color=INK)
    for i, (n, q, L, frm) in enumerate(rows):
        yy = 8.3 - i * 3.0
        ax.text(2, yy, n, fontsize=8, color=INK); ax.text(22, yy, str(q), fontsize=8, color=INK)
        ax.text(30, yy, f"{round(L / 10) * 10:.0f} mm", fontsize=8, color=INK); ax.text(44, yy, frm, fontsize=8, color=INK)
    if footer:
        fig.text(0.02, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
        fig.text(0.98, 0.015, "github.com/BoujeeEnjinia1701/snapframe", fontsize=7, color=AC, ha="right", family="monospace")
    OUT.mkdir(parents=True, exist_ok=True)
    out = Path(out) if out else OUT / "cable-assembly.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


def cable_sheet():
    from drawing import Sheet
    cable_picture()
    work = DWG / "_SNF-DWG-109_views"
    pic = cable_picture(footer=False, out=work / "cable.png")
    inset = bv.where_it_goes(Part("cables", S(lambda k: k[0] in ("cable", "hook") and k[1] != "guy"), COL["cable"]),
                             [Part("frame", S(lambda k: k[0] in ("tube", "node")), "#D1D5DB")], work / "where.png", elev=22, azim=-55)
    s = Sheet(project="SnapFrame", title="SnapFrame brace cables (make 10): making sketch", dwg_no="SNF-DWG-109", rev="P1",
              author="Amish Chadha", date=DATE, concept="BUILD PLAN SKETCH, PLAN NOT YET BUILT", scale=None,
              material="4 mm galvanized 7x19 wire rope; thimbles, clips, snap hooks, hand tensioners",
              revisions=[("P1", "Making sketch for the prototype build plan", DATE, "AC")])
    s.add_image(str(pic), 20, 30, 245, 116, label="Cable assembly", sublabel="Not to scale")
    s.add_image(str(inset), 276, 30, 140, 70, label="Where they go", sublabel="Cables in colour, the frame in grey")
    s.add_notes("How to make them and how they fit", [
        "Cut the wire 700 mm longer than the eye to eye length (loop,",
        "  tensioner and tail). Tape both ends before cutting.",
        "End 1: loop the wire round a thimble and fit two wire rope clips,",
        "  saddles on the long side, nuts torqued to the clip maker's figure.",
        "End 2: pass the wire through the hand tensioner as its maker shows.",
        "Clip a snap hook to the thimble and one to the tensioner's eye.",
        "Set the length with the tensioner let out to the eye to eye length.",
        "Label each cable (gable, wall, roof) on a tag at end 1.",
        "Fit: snap hooks clip to the anchor eyes at the feet and to the",
        "  rings on the cable bolts; pull snug with the tensioner only.",
        "Check: each clip is tight after one pull of 300 N by hand scale."],
        x=276, y=112, width=140)
    s.save(DWG / "SNF-DWG-109")
    shutil.rmtree(work, ignore_errors=True)
    return DWG / "SNF-DWG-109.png"


def bolt_pieces(key):
    """The cable bolt set of node `key` in three pieces (bolt; washers and spacer; nut), placed as in the model."""
    from build123d import Pos
    v = "eave" if key[0] == "eave" else "ridge"
    a = M.rotz(M.V(*M.BOLT_DIR[v]), NODES[key][2]).normalized()
    B = M.BOLT
    c = M.V(*NODES[key][1])
    s0 = B["spot"]
    hw = M.cyl(a * s0, a, B["washer_od"] / 2, B["washer_t"]) - M.cyl(a * (s0 - 1), a, B["hole"] / 2, 10)
    s1 = s0 + B["washer_t"]
    sp = M.cyl(a * s1, a, B["spacer_od"] / 2, B["spacer_l"]) - M.cyl(a * (s1 - 1), a, B["hole"] / 2, B["spacer_l"] + 2)
    s2 = s1 + B["spacer_l"]
    hw2 = M.cyl(a * s2, a, B["head_washer_od"] / 2, B["head_washer_t"]) - M.cyl(a * (s2 - 1), a, B["hole"] / 2, 10)
    s3 = s2 + B["head_washer_t"]
    head = M.hexagon(a * s3, a, B["head_af"], B["head_h"])
    shank = M.cyl(a * (s3 - B["length"]), a, B["d"] / 2 - 0.25, B["length"])
    fw = M.cyl(-a * B["recess_at"], -a, B["nut_washer_od"] / 2, B["nut_washer_t"]) - M.cyl(-a * (B["recess_at"] - 1), -a, B["hole"] / 2, 10)
    nut = M.hexagon(-a * (B["recess_at"] + B["nut_washer_t"]), -a, B["head_af"] + 1, B["nut_h"]) - M.cyl(-a * B["recess_at"], -a, B["d"] / 2, 20)
    return {"bolt": Pos(*c) * fuse([head, shank]), "washers": Pos(*c) * fuse([hw, hw2, fw]),
            "spacer": Pos(*c) * sp, "nut": Pos(*c) * nut}


def centre_point(shape):
    """The shape's own vertex nearest its centre (a leader end that lands on the part)."""
    import numpy as np
    v, _ = _tris_cached(shape)
    m = v.mean(0)
    return v[np.argmin(np.linalg.norm(v - m, axis=1))]


# ----------------------------------------------------------------- joints
def win(sh, c, half):
    from build123d import Box, Pos
    r = sh & (Pos(*c) * Box(2 * half[0], 2 * half[1], 2 * half[2]))
    return r


def joints(only=None):
    out = []
    keep_n = set(only or range(1, 7))
    from build123d import Box, Pos, Plane
    # 01: post foot in the foot node, cut open on the post's centre plane, seen from the inboard side
    fk = (X0, 1)
    c = (0.0, YE, 120.0)
    cut = Pos(0, YE + 100, 120) * Box(400, 200, 400)              # keep the outboard half: cut on the post axis plane x = 0? use Y-plane
    keep = Pos(-50, YE, 150) * Box(100, 120, 130)                 # keep x <= 0: section on the plane through the post axis, socket only
    parts = [part("Foot node socket (cut)", C[("node", "foot") + fk].shape & keep, COL["foot"]),
             part("Post end on the socket stop (cut)", C[("tube", "post") + fk].shape & keep, COL["post"]),
             part("Hitch pin, 15 mm from the tube end", C[("pin", "post") + fk + (("foot",) + fk,)].shape & keep, COL["pin"]),
             part("Snap button in its finger recess", C[("button", "post") + fk + (("foot",) + fk,)].shape, COL["button"]),
             part("Button spring inside the tube", C[("spring", "post") + fk + (("foot",) + fk,)].shape & keep, COL["spring"])]
    pb = parts[1].shape.bounding_box()
    LEAD["Post end on the socket stop (cut)"] = (pb.max.X, pb.min.Y + 0.6, pb.min.Z + 2)
    nb_ = parts[0].shape.bounding_box()
    LEAD["Foot node socket (cut)"] = (nb_.max.X, (nb_.min.Y + nb_.max.Y) / 2, nb_.min.Z + 8)
    if 1 not in keep_n:
        LEAD.clear()
    if 1 in keep_n:
      out.append(bv.joint(parts, OUT / "joint-01.png", "Joint 1: post in the foot node (cut open through the post)",
                        subtitle="Seen from inboard. The tube end sits on the flat stop; pin 15 mm and button 40 mm from the end; the spring clears the pin",
                        elev=12, azim=-35, size=(8, 6)))
    # 02: anchor eye on the foot plate, cable hook on the eye (rear corner, seen from outside and above)
    fk = (X0, -1)
    a = C[("anchor", fk)].shape
    ab = a.bounding_box()
    cc = ((ab.min.X + ab.max.X) / 2, (ab.min.Y + ab.max.Y) / 2, 40)
    parts = [part("Foot node (anchor slot open to the corner)", win(C[("node", "foot") + fk].shape, (cc[0] + 40, cc[1] + 40, 40), (110, 110, 60)), COL["foot"]),
             part("Screw anchor eye, turned down onto the plate", win(a, cc, (60, 60, 60)), COL["anchor"]),
             part("Rear gable cable, hooked to the eye", win(S(lambda k: k[0] == "hook" and k[1] == "gable" and k[2] == -1 and k[3] == "lo"), cc, (90, 90, 90)), COL["hook"]),
             part("Side wall cable, hooked to the eye", win(S(lambda k: k[0] == "hook" and k[1] == "wall" and k[2] == X0 and k[3] == -1 and k[4] == "lo"), cc, (90, 90, 90)), COL["cable"])]
    if 2 not in keep_n:
        LEAD.clear()
    if 2 in keep_n:
      out.append(bv.joint(parts, OUT / "joint-02.png", "Joint 2: anchor on the foot plate, rear corner",
                        subtitle="Seen from outside and above. The eye sits down on the plate across the slot; both cables clip to the eye",
                        elev=38, azim=-150, size=(8, 6)))
    # 03: rear corner eave node with its post, rafter, eave tube, cap, cable bolt, ring and hooks
    ek = ("eave", X0, -1)
    ctr = M.V(*NODES[ek][1])
    h = (160, 160, 160)
    cpt = (ctr.X, ctr.Y, ctr.Z)
    parts = [part("Eave node", C[("node",) + ek].shape, COL["eavenode"]),
             part("Post (hitch pin below the node)", win(C[("tube", "post", X0, -1)].shape, cpt, h), COL["post"]),
             part("Rafter", win(C[("tube", "rafter", X0, -1)].shape, cpt, h), COL["rafter"]),
             part("Eave tube", win(C[("tube", "eave", 0, -1)].shape, cpt, h), COL["eave"]),
             part("Cap in the blank socket past the gable", C[("cap",) + ek].shape, COL["cap"]),
             part("Hitch pin", C[("pin", "post", X0, -1, ek)].shape, COL["pin"]),
             part("Cable bolt set", win(C[("bolt",) + ek].shape, tuple(ctr + M.rotz(M.V(*M.BOLT_DIR["eave"]), NODES[ek][2]) * 52), (16, 16, 16)), COL["bolt"]),
             part("Ring", C[("ring",) + ek].shape, COL["ring"]),
             part("Snap hooks of the gable and roof cables", win(S(lambda k: k[0] == "hook" and (k[1:] in (("gable", 1, "hi"), ("roof", X0, -1, "lo")))), cpt, h), COL["hook"])]
    import numpy as np
    _rv, _ = _tris_cached(C[("ring",) + ek].shape)
    LEAD["Ring"] = _rv[np.argmin(_rv[:, 2])]
    _pv, _ = _tris_cached(parts[1].shape)
    _lo = _pv[_pv[:, 2] < _pv[:, 2].min() + 40].mean(0)
    LEAD["Post (hitch pin below the node)"] = _pv[np.argmin(np.linalg.norm(_pv - _lo, axis=1))]
    if 3 not in keep_n:
        LEAD.clear()
    if 3 in keep_n:
      out.append(bv.joint(parts, OUT / "joint-03.png", "Joint 3: rear corner eave node, from inside the shelter",
                        subtitle="Four sockets; the one past the gable is capped. Cables clip to the ring on the cable bolt, never to the print",
                        elev=-12, azim=50, size=(8, 6)))
    # 04: cable bolt cut open through the eave node, on the node's frame plane (x = node centre)
    keep = Pos(ctr.X + 150, ctr.Y, ctr.Z) * Box(300, 400, 400)
    bp = bolt_pieces(ek)
    parts = [part("Eave node (cut on the frame plane)", C[("node",) + ek].shape & keep, COL["eavenode"]),
             part("M10 bolt (cut)", bp["bolt"] & keep, COL["bolt"]),
             part("Washers on the spot face and in the recess (cut)", bp["washers"] & keep, "#9CA3AF"),
             part("Spacer that carries the ring (cut)", bp["spacer"] & keep, "#E5E7EB"),
             part("Nyloc nut, below the surface (cut)", bp["nut"] & keep, "#2563EB"),
             part("Ring (cut)", C[("ring",) + ek].shape & keep, COL["ring"]),
             part("Post (cut)", win(C[("tube", "post", X0, -1)].shape, cpt, (150, 150, 150)) & keep, COL["post"]),
             part("Rafter (cut)", win(C[("tube", "rafter", X0, -1)].shape, cpt, (150, 150, 150)) & keep, COL["rafter"])]
    LEAD["Eave node (cut on the frame plane)"] = (ctr.X, ctr.Y - 22 * (1 if ek[2] < 0 else -1), ctr.Z - 28)
    if 4 not in keep_n:
        LEAD.clear()
    if 4 in keep_n:
      out.append(bv.joint(parts, OUT / "joint-04.png", "Joint 4: cable bolt through the eave node (cut open)",
                        subtitle="Seen along the ridge. Washer on a flat spot face; spacer carries the ring; nut below the surface in its recess",
                        elev=0, azim=180, size=(8, 6)))
    # 05: middle ridge node, four roof cables on one ring, seen from below
    rk = ("ridge", XM)
    rc = NODES[rk][1]
    h = (200, 200, 170)
    parts = [part("Middle ridge node", C[("node",) + rk].shape, COL["ridgenode"]),
             part("Rafters", win(S(is_tube("rafter", XM)), rc, h), COL["rafter"]),
             part("Ridge tubes", win(S(is_tube("ridge")), rc, h), COL["ridge"]),
             part("Cable bolt set", win(C[("bolt",) + rk].shape, (rc[0], rc[1], rc[2] - 52), (16, 16, 16)), COL["bolt"]),
             part("Ring", C[("ring",) + rk].shape, COL["ring"]),
             part("Four roof cables, hooked to the ring", win(S(lambda k: k[0] == "hook" and k[1] == "roof" and k[-1] == "hi"), rc, h), COL["hook"])]
    import numpy as np
    rv, _ = _tris_cached(parts[1].shape)
    low = rv[rv[:, 2] < rv[:, 2].min() + 50]
    low = low[low[:, 1] > low[:, 1].mean()].mean(0)
    LEAD["Rafters"] = rv[np.argmin(np.linalg.norm(rv - low, axis=1))]
    if 5 not in keep_n:
        LEAD.clear()
    if 5 in keep_n:
      out.append(bv.joint(parts, OUT / "joint-05.png", "Joint 5: middle ridge node from below",
                        subtitle="All four roof cables clip into the one ring; the ring swings to line up with the pull",
                        elev=-35, azim=-60, size=(8, 6)))
    # 06: eave tube end in the eave node socket, cut open on its centre plane (z = eave height)
    mk = ("eave", 0, 1)
    nk = ("eave", XM, 1)
    nc = NODES[nk][1]
    keep = Pos(nc[0], nc[1], nc[2] - 100) * Box(400, 400, 200)
    pc = (nc[0] - 85, nc[1], nc[2])
    parts = [part("Eave node socket (cut)", win(C[("node",) + nk].shape, pc, (60, 40, 40)) & keep, COL["eavenode"]),
             part("Eave tube end (cut)", win(C[("tube",) + mk].shape, pc, (60, 40, 40)) & keep, COL["eave"]),
             part("Snap button through the tube and socket", C[("button",) + mk + (nk,)].shape, COL["button"]),
             part("V spring inside the tube", C[("spring",) + mk + (nk,)].shape & keep, COL["spring"])]
    for _n, _p in (("Snap button through the tube and socket", parts[2]), ("V spring inside the tube", parts[3])):
        _b = _p.shape.bounding_box()
        LEAD[_n] = (_b.center().X, _b.center().Y, _b.max.Z)
    if 6 not in keep_n:
        LEAD.clear()
    if 6 in keep_n:
      out.append(bv.joint(parts, OUT / "joint-06.png", "Joint 6: tube end in a socket (cut open), middle eave node",
                        subtitle="The button stands 2 mm proud in a 16 mm finger recess: press it with a fingertip and pull the tube",
                        elev=60, azim=-90, size=(8, 6)))
    return out


# ----------------------------------------------------------------- assembly steps
def _flat(shape, x):
    """A frame lying on the ground: rotated 90 degrees about the line of its feet, lying toward -X."""
    from build123d import Pos, Rot
    return Pos(x, 0, 112) * Rot(0, -90, 0) * Pos(-x, 0, 0) * shape


def steps(only=None):
    out = []
    g = ground()

    def st(n, done, new, title, sub, **kw):
        if only and n not in only:
            return
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)
    from build123d import Pos, Cylinder
    pegs = fuse(Pos(*M.V(*F.foot[k])) * Pos(0, 0, 100) * Cylinder(30, 300) for k in F.foot)
    corners = [(X0, -1), (XL, -1), (XL, 1), (X0, 1)]
    cp = [tuple(M.V(*F.foot[k]) + M.V(0, 0, 15)) for k in corners]
    cord = fuse(M.rod(cp[i], cp[(i + 1) % 4], 12) for i in range(4))
    diag = fuse([M.rod(cp[0], cp[2], 9), M.rod(cp[1], cp[3], 9)])
    g1 = ground(-900, 4900, -2900, 2900)
    _c = [M.V(*q) for q in cp]
    LEAD["Knotted layout cord round the 4.0 x 4.0 m square"] = tuple((_c[1] + _c[2]) * 0.5 + M.V(0, 0, 12))
    LEAD["Six marker pegs: four corners and two side middles"] = tuple(M.V(*F.foot[(XM, 1)]) + M.V(0, 0, 240))
    LEAD["Tape both diagonals: equal within 20 mm"] = tuple(_c[3] + (_c[1] - _c[3]) * 0.3 + M.V(0, 0, 9))
    st(1, [], [part("Six marker pegs: four corners and two side middles", pegs, COL["anchor"]),
               part("Knotted layout cord round the 4.0 x 4.0 m square", cord, COL["guy"]),
               part("Tape both diagonals: equal within 20 mm", diag, COL["eave"])],
       "mark out the floor", "Peg the corners and side middles of a 4.0 x 4.0 m square; move pegs until the two diagonals are equal",
       context=[g1], elev=40, azim=-60)
    fx = frame_line(X0)
    # step 2: rear frame flat: posts into eave nodes, rafters into eave nodes and the ridge node
    def flatp(name, pred, color, e=(0, 0, 0)):
        return part(name, _flat(S(pred), X0), color, e)
    en = flatp("Eave nodes (2) with caps and cable bolts", lambda k: fx(k) and ((k[0] == "node" and k[1] == "eave") or k[0] in ("cap",) or (k[0] in ("bolt", "ring") and k[1] == "eave")), COL["eavenode"])
    posts = flatp("Posts (2), hitch pins", lambda k: fx(k) and (k[0] == "tube" and k[1] == "post" or (k[0] == "pin" and k[-1][0] == "eave")), COL["post"], (250, 0, 0))
    raf = flatp("Rafters (2)", lambda k: fx(k) and k[0] == "tube" and k[1] == "rafter", COL["rafter"], (0, 0, 0))
    rn = flatp("Ridge node, end", lambda k: fx(k) and (k[0] == "node" and k[1] == "ridge" or (k[0] in ("bolt", "ring") and k[1] == "ridge")), COL["ridgenode"], (-400, 0, 0))
    raf.explode = (0, 0, 250)
    gf = ground(X0 - 2900, X0 + 500, -2500, 2500)
    st(2, [], [en, posts, raf, rn], "build the rear frame flat on the ground",
       "Posts into the eave nodes with hitch pins; rafters into the eave nodes and the ridge node until every button clicks",
       context=[gf], elev=50, azim=-60)
    feet = flatp("Foot nodes (2), hitch pins", lambda k: fx(k) and ((k[0] == "node" and k[1] == "foot") or (k[0] == "pin" and k[-1][0] == "foot")), COL["foot"], (200, 0, 0))
    done_flat = [part("Rear frame", _flat(S(lambda k: fx(k) and not (k[0] == "node" and k[1] == "foot") and not (k[0] == "pin" and k[-1][0] == "foot")), X0), "#D1D5DB")]
    st(3, done_flat, [feet], "foot nodes onto the post ends",
       "Each foot over its post end, button clicked, hitch pin through; slots turned to point out and back",
       context=[gf], elev=50, azim=-60, label_done=False)
    rear = part("Rear frame", S(fx), "#0F766E")
    st(4, [], [mv(rear, (0, 0, 250))], "stand the rear frame on its marks",
       "Two people walk it up from the ridge end (where it lay flat, faint); feet on the rear pegs. One holds it upright until step 6",
       context=[ground(X0 - 2900, 4700, -2700, 2700), part("Frame lying flat", _flat(S(fx), X0), "#E5E7EB")], elev=22, azim=-60)
    tubes1 = part("Eave tubes (2) and ridge tube, rear bay", S(lambda k: k[0] == "tube" and k[1] in ("eave", "ridge") and k[2] == 0), COL["eave"])
    st(5, [rear], [mv(tubes1, (350, 0, 0))], "eave tubes and ridge tube into the rear frame",
       "Push each straight into its socket until it clicks; a helper holds the far ends level (a step for the ridge)",
       context=[g], elev=18, azim=-60, label_done=False)
    mid = part("Middle frame (built flat as steps 2 and 3)", S(frame_line(XM)), "#16A34A")
    st(6, [rear, tubes1], [mv(mid, (300, 0, 0))], "slide the middle frame onto the tube ends",
       "Stand it 70 mm short of its pegs, line up the three sockets, slide it back 65 mm on its feet until all three click",
       context=[g], elev=18, azim=-60, label_done=False)
    tubes2 = part("Eave tubes (2) and ridge tube, front bay", S(lambda k: k[0] == "tube" and k[1] in ("eave", "ridge") and k[2] == 1), COL["ridge"])
    front = part("Front frame", S(frame_line(XL)), "#0F766E")
    st(7, [rear, tubes1, mid], [mv(tubes2, (350, 0, 0)), mv(front, (700, 0, 0))], "front bay: tubes, then the front frame",
       "Tubes into the middle frame; slide the front frame on as in step 6; caps go in the two front corner sockets",
       context=[g], elev=18, azim=-60, label_done=False)
    frame = [part("Frame", S(lambda k: k[0] in ("tube", "node", "pin", "cap", "bolt", "ring")), "#D1D5DB")]
    anchors = part("Screw anchors (6)", S(lambda k: k[0] == "anchor" and k[1] not in ("rear", "front")), COL["anchor"])
    st(8, frame, [mv(anchors, (0, 0, 500))], "square the frame and turn in the anchors",
       "Diagonals equal; each anchor down through its slot, turned by a spare tube through the eye until the eye sits on the plate",
       context=[g], elev=25, azim=-50, label_done=False)
    fa = frame + [part("Anchors", anchors.shape, "#D1D5DB")]
    gc = part("Rear gable cables (2)", thick(lambda k: k[1] == "gable"), "#DC2626")
    st(9, fa, [gc], "rear gable cables",
       "Each from a rear corner anchor eye to the ring of the opposite eave node; pull snug; tie them where they cross",
       context=[g], elev=15, azim=-130, label_done=False)
    wc = part("Side wall cables (4)", thick(lambda k: k[1] == "wall"), "#DC2626")
    st(10, fa + [part("done", gc.shape, "#D1D5DB")], [mv(wc, (0, 0, 0))], "side wall cables",
       "From each corner anchor eye up to the ring of the middle eave node on that side; pull snug",
       context=[g], elev=15, azim=-60, label_done=False)
    rcab = part("Roof cables (4)", thick(lambda k: k[1] == "roof"), "#DC2626")
    st(11, fa + [part("done", fuse([gc.shape, wc.shape]), "#D1D5DB")], [rcab], "roof cables",
       "From the ring of each corner eave node to the ring of the middle ridge node; pull snug, front and back alike",
       context=[g], elev=40, azim=-60, label_done=False)
    guys = part("Guy anchors and guy lines (2)", fuse([thick(lambda k: k[1] == "guy", 14), S(lambda k: k[0] == "anchor" and k[1] in ("rear", "front"))]), COL["guy"])
    allc = fuse([gc.shape, wc.shape, rcab.shape])
    g2 = ground(-2300, 6300)
    st(12, fa + [part("done", allc, "#D1D5DB")], [guys], "guy anchors and guy lines",
       "Anchors 1.5 m out from each gable on the ridge line; tie each guy to the end ridge node's ring and tension it",
       context=[g2], elev=15, azim=-60, label_done=False)
    # 13: skin, as the concept (two tarpaulins; front gable open)
    from build123d import Vector, Wire, Face, Solid
    he, hr = F.p["eave"], F.p["ridge"]
    L = XL
    sl = math.atan2(hr - he, YE)

    def panel(pts, normal, t=8.0, off=60.0):
        n = Vector(*normal).normalized()
        ps = [Vector(*p) + n * off for p in pts]
        return Solid.extrude(Face(Wire.make_polygon(ps, close=True)), n * t)
    roof = fuse([panel([(-100, YE + 150, he - 60), (L + 100, YE + 150, he - 60), (L + 100, -40, hr + 16), (-100, -40, hr + 16)], (0, math.sin(sl), math.cos(sl)))
, panel([(-100, -YE - 150, he - 60), (L + 100, -YE - 150, he - 60), (L + 100, 40, hr + 16), (-100, 40, hr + 16)], (0, -math.sin(sl), math.cos(sl)))])
    walls = fuse([panel([(0, YE, 10), (L, YE, 10), (L, YE, he), (0, YE, he)], (0, 1, 0))
             , panel([(0, -YE, 10), (L, -YE, 10), (L, -YE, he), (0, -YE, he)], (0, -1, 0))
             , panel([(0, -YE, 10), (0, YE, 10), (0, YE, he), (0, 0, hr), (0, -YE, he)], (-1, 0, 0))])
    LEAD["Tarpaulin 2: side walls and rear gable"] = (L * 0.3, -YE - 64, he * 0.45)
    LEAD["Tarpaulin 1: roof, over the ridge"] = (L * 0.6, -YE * 0.5 - 30, (he + hr) / 2 + 75 + 500)
    st(13, fa + [part("done", fuse([allc, guys.shape]), "#D1D5DB")],
       [mv(part("Tarpaulin 1: roof, over the ridge", roof, "#3B6EA5"), (0, 0, 500)),
        mv(part("Tarpaulin 2: side walls and rear gable", walls, "#60A5FA"), (0, 0, 0))],
       "tarpaulins (agency stock)", "Tie through the eyelets to the tubes, never to the nodes or cables; the front gable stays open",
       context=[g2], elev=20, azim=-55, label_done=False)
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "tubes", "cables", "joints", "steps"]
    fns = {"overview": overview, "sheets": node_sheets, "tubes": tube_sheets, "cables": cable_sheet, "joints": joints, "steps": steps}
    for w in what:
        if ":" in w:
            w, arg = w.split(":")
            r = fns[w]([x if w == "tubes" else int(x) for x in arg.split(",")])
            print(w, "->", r, flush=True)
            continue
        r = fns[w]()
        print(w, "->", r, flush=True)
