"""SnapFrame skin cutting plan for three 4 x 6 m relief tarpaulins (TRL 3, SNF-DEC-001, 2026-10-02).

Decided 2026-10-02: the roof, both side walls and the rear gable come from two tarpaulins, and the front
gable from part of a third, cut to include a door flap; the corner cable hem is settled in the same plan
(SNF-DDR-003 A2, option c). Sizes in metres. Each tarpaulin is drawn with its 6.0 m side along u and its
4.0 m side along v. Pieces are axis-aligned rectangles or isosceles triangles (given as the box they fit in).

    python cad/src/skin_plan.py        prints the plan and its checks
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import model as M

TARP_U, TARP_V = 6.0, 4.0
SIZE = "M"
P = M.SIZES[SIZE]
SPAN = P["span"] / 1000.0
LENGTH = P["bay"] * P["bays"] / 1000.0
EAVE = P["eave"] / 1000.0
RIDGE = P["ridge"] / 1000.0
RAFTER = math.hypot(SPAN / 2, RIDGE - EAVE)          # node centre to node centre, m
WALL_H = 2.0                                          # strip height: 1.8 m wall plus 0.2 m tucked under the roof sheet
GABLE_PEAK = 0.9                                      # triangle height: 0.8 m ridge rise plus 0.1 m lap
DOOR_W, DOOR_H = 1.0, 1.7
NOTCH_W, NOTCH_H = 0.40, 0.20                         # corner cable hem: cut-out at each lower corner

# (tarpaulin, name, u0, v0, width along u, height along v, shape, note)
PIECES = [
    (1, "Roof sheet", 0.0, 0.0, 6.0, 4.0, "rect", "Whole tarpaulin, 6.0 m across the slopes over the ridge, 4.0 m along it"),
    (2, "Side wall, left", 0.0, 0.0, 4.0, 2.0, "wall", "Strip 4.0 x 2.0 m, two corner cable hems"),
    (2, "Side wall, right", 0.0, 2.0, 4.0, 2.0, "wall", "Strip 4.0 x 2.0 m, two corner cable hems"),
    (2, "Rear gable, lower", 4.0, 0.0, 2.0, 4.0, "wall", "Strip 4.0 x 2.0 m turned to run across the gable, two corner cable hems"),
    (3, "Front gable, lower, with door flap", 0.0, 0.0, 4.0, 2.0, "door", "Strip 4.0 x 2.0 m; door flap 1.0 x 1.7 m cut by two slits"),
    (3, "Gable triangles, two", 0.0, 2.0, 6.0, 0.9, "tri2", "Two triangles, base 4.0 m, height 0.9 m, interlocked in a 6.0 x 0.9 m strip"),
]


def area(p):
    t, name, u0, v0, w, h, shape, note = p
    if shape == "tri2":
        return 2 * 0.5 * 4.0 * h
    return w * h


def needs():
    """Skin the frame needs, m2 (SNF-CAL-001 section 8)."""
    roof = 2 * (RAFTER + 0.15) * (LENGTH + 0.20)
    walls = 2 * LENGTH * EAVE
    gable = SPAN * EAVE + 0.5 * SPAN * (RIDGE - EAVE)
    return {"roof": roof, "walls": walls, "gable": gable, "total": roof + walls + 2 * gable}


def check():
    """(description, ok) for the plan."""
    rows = []
    n = needs()
    # 1. every piece lies inside its tarpaulin, none overlap
    for t in (1, 2, 3):
        ps = [p for p in PIECES if p[0] == t]
        for p in ps:
            ok = p[2] >= 0 and p[3] >= 0 and p[2] + p[4] <= TARP_U + 1e-9 and p[3] + p[5] <= TARP_V + 1e-9
            rows.append((f"{p[1]} lies inside tarpaulin {t} ({TARP_U:.1f} x {TARP_V:.1f} m)", ok))
        for i, a in enumerate(ps):
            for b in ps[i + 1:]:
                ok = a[2] + a[4] <= b[2] + 1e-9 or b[2] + b[4] <= a[2] + 1e-9 or a[3] + a[5] <= b[3] + 1e-9 or b[3] + b[5] <= a[3] + 1e-9
                rows.append((f"{a[1]} and {b[1]} do not overlap", ok))
    # 2. piece sizes cover what the frame needs
    rows.append((f"roof sheet 6.0 m covers the slopes {2 * RAFTER:.2f} m plus an eave skirt of {(6.0 - 2 * RAFTER) / 2:.2f} m each side",
                 6.0 >= 2 * RAFTER + 0.3))
    rows.append((f"roof sheet 4.0 m covers the ridge length {LENGTH:.1f} m", 4.0 >= LENGTH))
    rows.append((f"wall strips 4.0 x {WALL_H:.1f} m cover each side wall {LENGTH:.1f} x {EAVE:.1f} m with 0.2 m to tuck", WALL_H >= EAVE + 0.2 - 1e-9))
    rows.append((f"rear and front lower strips 4.0 m cover the {SPAN:.1f} m gable width", 4.0 >= SPAN))
    rows.append((f"gable triangles: base 4.0 m covers {SPAN:.1f} m, height {GABLE_PEAK:.1f} m covers the {RIDGE - EAVE:.1f} m rise plus lap",
                 4.0 >= SPAN and GABLE_PEAK >= RIDGE - EAVE + 0.1 - 1e-9))
    # two isosceles triangles of base 4.0 interlock in 4.0 + 2.0 = 6.0 m
    rows.append(("two triangles of base 4.0 m interlock in a 6.0 m strip (4.0 + half the base)", abs(4.0 + 4.0 / 2 - 6.0) < 1e-9))
    # 3. door flap on the front strip: two slits from the lower edge, hinged at the top
    rows.append((f"door flap {DOOR_W:.1f} x {DOOR_H:.1f} m fits the front strip height {WALL_H:.1f} m with {WALL_H - DOOR_H:.1f} m left above the hinge",
                 DOOR_H < WALL_H - 0.2))
    # 4. corner cable hem from the model: where each cable leaves the cut-out
    C, L = M.comps(SIZE)
    worst = 0.0
    for ck, (a, b) in M.CABLE_ENDS.items():
        if ck[0] not in ("gable", "wall"):
            continue
        # horizontal run along the wall plane from the lower end to the point where the cable is NOTCH_H above the ground
        a = M.V(*a); b = M.V(*b)
        d = b - a
        t = (NOTCH_H * 1000 - a.Z) / d.Z
        run = math.hypot(d.X * t, d.Y * t) / 1000
        worst = max(worst, run)
    rows.append((f"corner cable hem {NOTCH_W:.2f} x {NOTCH_H:.2f} m: every gable and wall cable is {NOTCH_H:.2f} m up after a run of "
                 f"at most {worst:.2f} m from its anchor eye", worst <= NOTCH_W + 1e-9))
    # 5. area
    used = sum(area(p) for p in PIECES)
    rows.append((f"area needed {n['total']:.1f} m2 is less than 3 x 24 = 72 m2; pieces used {used:.1f} m2, spare {72 - used:.1f} m2",
                 n["total"] < 72 and used <= 72))
    return rows


def spare():
    return 72.0 - sum(area(p) for p in PIECES)


if __name__ == "__main__":
    n = needs()
    print({k: round(v, 1) for k, v in n.items()})
    bad = 0
    for d, ok in check():
        bad += 0 if ok else 1
        print("ok  " if ok else "FAIL", d)
    print(f"{bad} failed; spare {spare():.1f} m2")
    sys.exit(1 if bad else 0)
