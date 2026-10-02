"""SnapFrame sizing calculations for SNF-CAL-001 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md. Geometry (cut lengths, node volumes and
bounding boxes) comes from cad/src/model.py so the note, the model and the BOM stay in step.

v0.2 applies SNF-DDR-002 (1 in ridge tubes, one eave node variant).
v0.4 applies SNF-DDR-003 (design for construction): hitch pin 15 mm from the tube end, cable bolt
sets with rings on the eave and ridge nodes, cable lengths between their real attachment points,
and the budget treated as a value-engineering target.
First-order, hand-calculation level. Not a code check and not a frame analysis.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
import model as M  # noqa: E402

# ---------------------------------------------------------------------------
# Assumptions (each is stated in the note, section 2)
# ---------------------------------------------------------------------------
RHO_AIR = 1.225          # kg/m3
V_DESIGN = 20.0          # m/s gust (R6)
SF_REQ = 1.5             # on yield (R6)
FY = 275.0               # MPa, assumed EMT yield (to confirm from supplier data)
RHO_STEEL = 7850.0       # kg/m3
CP_WALL_WW = 0.8         # windward wall
CP_WALL_LW = -0.5        # leeward wall (suction)
CP_ROOF = -0.7           # roof suction, both slopes, net of internal pressure for a closed shelter
CPI_OPEN = 0.55          # sensitivity: internal pressure with the open gable facing the wind
G = 9.81

SIZE = "M"
P = M.SIZES[SIZE]
BAY = P["bay"] / 1000; SPAN = P["span"] / 1000; ZF = M.NODE["z_foot"] / 1000
H_E = P["eave"] / 1000; H_R = P["ridge"] / 1000
HALF = SPAN / 2
RAFTER = math.hypot(HALF, H_R - H_E)             # node-center span, m
POST = H_E - ZF
PITCH = math.atan2(H_R - H_E, HALF)
LENGTH = BAY * P["bays"]


def section(kind):
    t = M.TUBES[kind]
    D = t["od"]; d = D - 2 * t["wall"]
    A = math.pi / 4 * (D ** 2 - d ** 2)                      # mm2
    I = math.pi / 64 * (D ** 4 - d ** 4)                     # mm4
    return {"od": D, "wall": t["wall"], "A": A, "I": I, "S": I / (D / 2), "kg_m": A * 1e-6 * RHO_STEEL}


SEC = {k: section(k) for k in M.TUBES}


def q(v):
    return 0.5 * RHO_AIR * v ** 2


# ---------------------------------------------------------------------------
# Panel load sharing: 45 degree tributary lines from each corner of a panel supported on four
# edges (the usual two-way rule). Short edges get triangles, long edges trapezoids.
# ---------------------------------------------------------------------------
def tributary(a, b):
    """Panel a (along X, between frames) by b (the other edge). Returns shares (area m2) for
    the edges of length a and of length b, per edge, and the ramp length on each."""
    s = min(a, b) / 2
    tri = 0.5 * min(a, b) * s                  # triangle on each short edge
    trap = (a * b - 2 * tri) / 2               # trapezoid on each long edge
    if a <= b:
        return {"a": (tri, s, "tri"), "b": (trap, s, "trap")}
    return {"a": (trap, s, "trap"), "b": (tri, s, "tri")}


def m_mid(w0, L, ramp, shape):
    """Midspan moment (N m) of a simply supported member: peak load w0 (N/m) as a symmetric
    triangle (ramp = L/2) or trapezoid with end ramps of length ramp."""
    if shape == "tri":
        return w0 * L ** 2 / 12
    return w0 * (L ** 2 / 8 - ramp ** 2 / 6)


def combine(m1, m2, cos_angle):
    return math.sqrt(m1 ** 2 + m2 ** 2 + 2 * m1 * m2 * cos_angle)


def wind_members(v, cp_roof=CP_ROOF, cpi=0.0):
    """Midspan moments (N m) and stresses at gust speed v for the middle frame and end rafter."""
    qq = q(v)
    p_roof = (abs(cp_roof) + cpi) * qq       # suction plus positive internal pressure
    p_ww = CP_WALL_WW * qq                   # internal pressure relieves the windward wall; ignored (conservative)
    p_lw = (abs(CP_WALL_LW) + cpi) * qq
    roof = tributary(BAY, RAFTER)
    wall = tributary(BAY, POST)
    out = {}
    # rafter, middle frame: roof panels on both sides
    area, ramp, shp = roof["b"]
    w0 = p_roof * ramp * 2
    out["rafter"] = m_mid(w0, RAFTER, ramp, shp)
    # ridge tube: triangle or trapezoid from each slope, vertical resultant
    area, ramp, shp = roof["a"]
    w0 = p_roof * ramp * 2 * math.cos(PITCH)
    out["ridge"] = m_mid(w0, BAY, ramp, shp)
    # post, middle frame, windward: wall panels on both sides
    area, ramp, shp = wall["b"]
    w0 = p_ww * ramp * 2
    out["post"] = m_mid(w0, POST, ramp, shp)
    # eave tube: roof share (along the roof normal) plus wall share (horizontal)
    ar, rr, sr = roof["a"]; aw, rw, sw = wall["a"]
    m_roof = m_mid(p_roof * rr, BAY, rr, sr)
    m_ww = m_mid(p_ww * rw, BAY, rw, sw)
    m_lw = m_mid(p_lw * rw, BAY, rw, sw)
    # windward: wall pushes in, roof pulls out along its normal (angle between them 90 + pitch)
    out["eave (windward)"] = combine(m_roof, m_ww, -math.sin(PITCH))
    out["eave (leeward)"] = combine(m_roof, m_lw, math.sin(PITCH))
    # end rafter, wind on the closed rear gable: gable panel horizontal plus half the roof suction
    gable_area = SPAN * POST + 0.5 * SPAN * (H_R - H_E)
    bottom = (SPAN + (SPAN - POST)) / 2 * (POST / 2)          # trapezoid on the ground edge
    sides = 2 * (0.5 * POST * POST / 2)                        # triangles on the corner posts
    per_rafter = (gable_area - bottom - sides) / 2
    w_gable = p_ww * per_rafter / RAFTER                        # spread uniformly (first order)
    m_g = w_gable * RAFTER ** 2 / 8
    area, ramp, shp = roof["b"]
    m_r = m_mid(p_roof * ramp, RAFTER, ramp, shp)
    out["rafter (end, gable wind)"] = combine(m_g, m_r, 0.0)
    return out


KIND_OF = {"rafter": "rafter", "ridge": "ridge", "post": "post", "eave (windward)": "eave",
           "eave (leeward)": "eave", "rafter (end, gable wind)": "rafter"}


def stresses(moments, tube_of=None):
    tube_of = tube_of or M.TUBE_OF
    res = {}
    for k, m in moments.items():
        s = SEC[tube_of[KIND_OF[k]]]["S"]
        sig = m * 1e3 / s
        res[k] = (m, sig, FY / sig)
    return res


def rating(tube_of=None, cp_roof=CP_ROOF, cpi=0.0):
    """Gust speed at which the weakest member reaches SF_REQ (stress scales with v squared)."""
    r = stresses(wind_members(V_DESIGN, cp_roof, cpi), tube_of)
    sf_min = min(v[2] for v in r.values())
    return V_DESIGN * math.sqrt(sf_min / SF_REQ), sf_min, min(r, key=lambda k: r[k][2])


def hr(t):
    print("\n" + t + "\n" + "-" * len(t))


def main():
    ml = M.member_lengths(SIZE)
    hr("1. Geometry, size M")
    print(f"floor {SPAN:.1f} x {LENGTH:.1f} m = {SPAN * LENGTH:.1f} m2; people at 3.5 m2: {SPAN * LENGTH / 3.5:.1f}")
    print(f"pitch {math.degrees(PITCH):.1f} deg; rafter node span {RAFTER:.3f} m; post node span {POST:.3f} m")
    # headroom: underside of rafter tube; 2.0 m or more where the roof is high enough
    r_off = SEC["1"]["od"] / 2000 / math.cos(PITCH)
    y2 = (H_R - r_off - 2.0) / ((H_R - H_E) / HALF)
    print(f"headroom 2.0 m or more over |y| <= {y2:.3f} m: {2 * y2 / SPAN * 100:.0f} % of the floor")
    for s in M.SIZES:
        p = M.SIZES[s]; l = M.member_lengths(s)
        print(f"size {s}: floor {p['span'] / 1000:.1f} x {p['bay'] * p['bays'] / 1000:.1f} m = "
              f"{p['span'] * p['bay'] * p['bays'] / 1e6:.1f} m2; cut lengths " +
              ", ".join(f"{k} {v / 1000:.3f} m" for k, v in l.items()))

    hr("2. Tube sections (ANSI C80.3 nominal)")
    for k, s in SEC.items():
        print(f"{k:>4} in EMT: OD {s['od']:.2f} mm, wall {s['wall']:.3f} mm, A {s['A']:.1f} mm2, "
              f"I {s['I']:.0f} mm4, S {s['S']:.0f} mm3, {s['kg_m']:.3f} kg/m")

    hr("3. Wind at 20 m/s gust")
    print(f"q = {q(V_DESIGN):.0f} Pa; roof suction {abs(CP_ROOF) * q(V_DESIGN):.1f} Pa; "
          f"windward wall {CP_WALL_WW * q(V_DESIGN):.1f} Pa")
    rt = tributary(BAY, RAFTER); wt = tributary(BAY, POST)
    print(f"roof panel {BAY:.2f} x {RAFTER:.3f} m: rafter edge {rt['b'][0]:.3f} m2 ({rt['b'][2]}), "
          f"ridge or eave edge {rt['a'][0]:.3f} m2 ({rt['a'][2]}), share per rafter "
          f"{rt['b'][0] / (BAY * RAFTER) * 100:.1f} %")
    print(f"wall panel {BAY:.2f} x {POST:.3f} m: post edge {wt['b'][0]:.3f} m2 ({wt['b'][2]}), "
          f"eave or ground edge {wt['a'][0]:.3f} m2 ({wt['a'][2]})")
    res = stresses(wind_members(V_DESIGN))
    print(f"{'member':26s} {'tube':>5s} {'M N m':>7s} {'MPa':>6s} {'SF':>5s}")
    for k, (m, sig, sf) in res.items():
        print(f"{k:26s} {M.TUBE_OF[KIND_OF[k]]:>5s} {m:7.1f} {sig:6.0f} {sf:5.2f} {'ok' if sf >= SF_REQ else 'BELOW 1.5'}")
    v, sfm, gov = rating()
    print(f"rating (weakest member at SF 1.5): {v:.1f} m/s ({v * 3.6:.0f} km/h, {v * 2.237:.0f} mph); governed by {gov}")
    all34 = {k: "3/4" for k in M.TUBE_OF}
    v34, sf34, g34 = rating(all34)
    print(f"all 3/4 in (TRL 2 concept): rating {v34:.1f} m/s; governed by {g34} at SF {sf34:.2f}")
    alt = dict(M.TUBE_OF, ridge="3/4")
    va, sfa, ga = rating(alt)
    print(f"DDR-001 only, 1 in rafters and 3/4 in ridge tubes (CAL-001 v0.1): rating {va:.1f} m/s; governed by {ga} at SF {sfa:.2f}")
    alt2 = dict(M.TUBE_OF, ridge="1", post="1")
    vb, sfb, gb = rating(alt2)
    print(f"sensitivity, 1 in rafters, ridge tubes and posts: rating {vb:.1f} m/s; governed by {gb} at SF {sfb:.2f}")
    vo, sfo, go = rating(cpi=CPI_OPEN)
    print(f"sensitivity, open gable facing the wind (Cpi +{CPI_OPEN}): rating {vo:.1f} m/s; governed by {go} at SF {sfo:.2f}")
    # TRL 2 method for comparison: half of each panel to the frames, uniform
    w_old = abs(CP_ROOF) * q(V_DESIGN) * BAY / 2
    m_old = w_old * RAFTER ** 2 / 8
    print(f"TRL 2 method (half of panel, uniform): rafter M {m_old:.0f} N m; "
          f"{m_old * 1e3 / SEC['3/4']['S']:.0f} MPa in 3/4 in")

    hr("4. Snow check (out of scope, for the safety note)")
    s_kpa = 0.5
    w0 = s_kpa * 1e3 * math.cos(PITCH) * rt["b"][1] * 2 * math.cos(PITCH)
    ms = m_mid(w0, RAFTER, rt["b"][1], rt["b"][2])
    print(f"0.5 kPa snow on plan, middle 1 in rafter: M {ms:.0f} N m, {ms * 1e3 / SEC['1']['S']:.0f} MPa "
          f"(yield {FY:.0f} MPa)")

    hr("5. Bracing, anchors and joints at 20 m/s")
    qq = q(V_DESIGN)
    lat = (CP_WALL_WW + abs(CP_WALL_LW)) * qq * LENGTH * POST     # transverse wall load, N
    top = lat / 2                                                  # half to eave level
    L_gx = math.hypot(SPAN, POST)
    T_gable = top / (SPAN / L_gx)
    V_gable = T_gable * POST / L_gx
    couple = top * LENGTH / 2                                      # roof cantilever from the rear gable
    side = couple / SPAN
    L_sw = math.hypot(BAY, POST)
    T_side = side / (BAY / L_sw)
    V_side = T_side * POST / L_sw
    print(f"transverse wall load {lat:.0f} N; to eave level {top:.0f} N, all to the braced rear gable")
    print(f"rear gable X cable: tension {T_gable:.0f} N, vertical at the foot {V_gable:.0f} N")
    print(f"roof cantilever couple {couple:.0f} N m; side wall force {side:.0f} N; side cable tension {T_side:.0f} N, "
          f"vertical {V_side:.0f} N")
    long_load = CP_WALL_WW * qq * (SPAN * POST + 0.5 * SPAN * (H_R - H_E))
    T_long = long_load / 2 / 2 / (BAY / L_sw)
    print(f"longitudinal wind on the rear gable {long_load:.0f} N; side cable tension (two walls, half to top) {T_long:.0f} N")
    MBL = 8000.0
    tmax = max(T_gable, T_side, T_long)
    print(f"4 mm 7x19 wire rope, assumed minimum breaking load {MBL / 1000:.1f} kN: factor {MBL / tmax:.1f}")
    # frame masses for dead load
    m_tubes = {k: SEC[M.TUBE_OF[k]]["kg_m"] * ml[k] / 1000 for k in ml}
    frame_dead = (2 * m_tubes["post"] + 2 * m_tubes["rafter"] + 2 * m_tubes["eave"] + m_tubes["ridge"] + 0.9) * G
    uplift_mid = abs(CP_ROOF) * qq * SPAN * BAY
    foot_mid = (uplift_mid - frame_dead) / 2
    foot_end = (uplift_mid / 2 - frame_dead / 2) / 2
    worst = foot_end + V_gable + V_side
    print(f"roof uplift on the middle frame {uplift_mid:.0f} N, dead load {frame_dead:.0f} N; "
          f"foot anchor {foot_mid / 1000:.2f} kN (middle), {foot_end / 1000:.2f} kN (end) from roof suction")
    print(f"worst foot (rear corner): {foot_end / 1000:.2f} + {V_gable / 1000:.2f} (gable cable) + "
          f"{V_side / 1000:.2f} (side cable) = {worst / 1000:.2f} kN, before pretension")
    pin_bear_polymer = worst / (2 * M.NODE["pin_d"] * M.NODE["wall"])
    pin_bear_steel = worst / (2 * M.NODE["pin_d"] * SEC["3/4"]["wall"])
    e = M.NODE["pin_at"] - M.NODE["pin_d"] / 2
    shear_out = 2 * 2 * e * SEC["3/4"]["wall"] * 0.6 * FY
    print(f"hitch pin at the worst foot: bearing on the polymer socket {pin_bear_polymer:.1f} MPa "
          f"({2 * pin_bear_polymer:.1f} MPa with the R9 factor of 2); on the EMT wall {pin_bear_steel:.0f} MPa; "
          f"EMT shear-out capacity {shear_out / 1000:.1f} kN")
    rt_b = rt["b"]
    shear = abs(CP_ROOF) * qq * rt_b[0] * 2 / 2
    eng = M.NODE["sock_l"] - M.NODE["tube_gap"]
    print(f"rafter end shear {shear:.0f} N; bearing in the socket over {eng:.0f} mm engagement "
          f"{shear / (SEC['1']['od'] * eng):.2f} MPa (nominal, before prying)")
    # cable bolt (SNF-DDR-003 C3): worst node is a rear corner eave node, gable cable plus roof cable
    B = M.BOLT
    p_bolt = T_gable + T_long
    lever = B["washer_t"] + B["spacer_l"] - B["ring_wire"] / 2
    m_b = p_bolt * lever / 1000
    w_b = math.pi * B["d"] ** 3 / 32
    sig_b = m_b * 1e3 / w_b
    FY_A4 = 450.0
    clamp = B["spot"] + B["recess_at"]
    bear = p_bolt / (B["d"] * clamp) + 6 * m_b * 1e3 / (B["d"] * clamp ** 2)
    print(f"cable bolt M10 at a rear corner eave node: load up to {p_bolt:.0f} N (gable plus roof cable, upper bound), "
          f"lever {lever:.1f} mm, {m_b:.1f} N m, {sig_b:.0f} MPa in the shank, factor {FY_A4 / sig_b:.1f} on 450 MPa (A4-70); "
          f"bearing on the polymer about {bear:.1f} MPa ({2 * bear:.1f} MPa with the R9 factor of 2)")

    hr("6. Node mass and cost (printed)")
    FILL = 0.55; RHO_P = 1070.0; FIL_USD = 22.0; MACH_USD = 1.0
    var = M.node_variants(SIZE)
    n_mass = 0.0; n_cost = 0.0; bb_vol = 0.0
    fam = {"foot": 0.0, "eave": 0.0, "ridge": 0.0}; fam_n = {"foot": 0, "eave": 0, "ridge": 0}
    for name, (shape, count, _) in var.items():
        mkg = shape.volume * 1e-9 * RHO_P * FILL
        cost = mkg * FIL_USD + MACH_USD
        b = shape.bounding_box()
        bb = b.size.X * b.size.Y * b.size.Z * 1e-9
        n_mass += mkg * count; n_cost += cost * count; bb_vol += bb * count
        f = name.split("-")[0]; fam[f] += cost * count; fam_n[f] += count
        print(f"{name:13s} x{count}: solid {shape.volume / 1000:6.1f} cm3, printed {mkg * 1000:4.0f} g, "
              f"${cost:5.2f} each, box {b.size.X:.0f} x {b.size.Y:.0f} x {b.size.Z:.0f} mm")
    for f in fam:
        print(f"  {f} nodes: {fam_n[f]} at mean ${fam[f] / fam_n[f]:.2f}")
    print(f"nodes total {n_mass:.2f} kg, ${n_cost:.2f}; sum of bounding boxes {bb_vol:.3f} m3")

    hr("7. Mass, packages and cost, size M")
    # cable assemblies between their attachment points (SNF-DDR-003): anchor eye to cable ring
    CL = M.cable_lengths(SIZE)
    kinds = {}
    for k, v in CL.items():
        kinds.setdefault(k[0], []).append(v)
    for k, v in kinds.items():
        print(f"{k} cables: {len(v)} at {min(v):.0f} to {max(v):.0f} mm eye to eye (wire, hooks not counted)")
    cable_len = sum(v for k, v in CL.items() if k[0] != "guy") / 1000
    counts = {"post": 6, "rafter": 6, "ridge": 2, "eave": 4}
    tube_kg = sum(counts[k] * m_tubes[k] for k in counts)
    tube_m = sum(counts[k] * ml[k] for k in counts) / 1000
    mass = {
        "tubes": tube_kg,
        "nodes": n_mass,
        "cables": cable_len * 0.065 + 10 * 0.17,
        "cable bolt sets": 9 * 0.13,
        "anchors": 8 * 0.45,
        "guys": 2 * (3.5 * 0.025 + 0.05),
        "buttons and pins": 36 * 0.01 + 12 * 0.03,
        "straps and bag": 0.4 + 0.6,
    }
    tarps = 2 * 4 * 6 * 0.19
    frame_kit = sum(mass.values())
    for k, v in mass.items():
        print(f"{k:18s} {v:5.2f} kg")
    print(f"tube length {tube_m:.2f} m; cable length {cable_len:.1f} m (eye to eye, 10 cables)")
    print(f"frame kit {frame_kit:.1f} kg ({frame_kit * 2.205:.0f} lb); tarpaulins (agency stock) {tarps:.1f} kg; "
          f"with tarpaulins {frame_kit + tarps:.1f} kg")
    bundle = tube_kg + 0.4
    rest = frame_kit - bundle
    ods = [SEC[M.TUBE_OF[k]]["od"] for k in counts for _ in range(counts[k])]
    bundle_vol = sum(d ** 2 for d in ods) * 1e-6 * 1.15 * 2.10
    bag_vol = bb_vol * 0.6 + 0.012
    print(f"package 1, tube bundle: {bundle:.1f} kg, {bundle_vol:.3f} m3 (hex packing factor 1.15, 2.10 m)")
    print(f"package 2, bag: {rest:.1f} kg without tarpaulins ({rest + tarps:.1f} kg with); contents "
          f"about {bag_vol:.3f} m3 without tarpaulins (nodes nest to 60 % of their boxes, plus 0.012 m3)")
    split_a = counts["rafter"] * m_tubes["rafter"] + counts["ridge"] * m_tubes["ridge"] + 0.2
    split_b = bundle - split_a
    print(f"option, two tube bundles: rafters and ridge tubes {split_a:.1f} kg; posts and eave tubes {split_b:.1f} kg")

    price = {"3/4": 9.00, "1": 14.00}
    tube_cost = sum(counts[k] * price[M.TUBE_OF[k]] for k in counts)
    cost = {
        "tubes (18 sticks)": tube_cost,
        "nodes (15)": n_cost,
        "brace cables (10)": 10 * 4.20,
        "cable bolt sets (9)": 9 * 2.60,
        "screw anchors (8)": 8 * 4.00,
        "guy lines (2)": 2 * 3.00,
        "buttons and pins": 24.00,
        "straps and bag": 20.00,
    }
    total = sum(cost.values())
    for k, v in cost.items():
        print(f"{k:20s} ${v:7.2f}")
    target = 445  # budget_usd in project.yaml: a value-engineering target, not a limit (Amish, 2026-10-01)
    print(f"frame kit ${total:.2f}; value-engineering target ${target}: ${abs(total - target):.2f} "
          f"{'over' if total > target else 'under'} ({(total / target - 1) * 100:+.1f} %); "
          f"tarpaulins (agency stock) $50.00; with tarpaulins ${total + 50:.2f}")
    bought = 18 * 3.05
    print(f"offcut: {bought:.1f} m bought, {tube_m:.1f} m used, {(1 - tube_m / bought) * 100:.0f} % offcut")

    hr("8. Skin (R7)")
    ov = 0.15
    roof = 2 * (RAFTER + ov) * (LENGTH + 2 * 0.10)
    walls = 2 * LENGTH * H_E
    gable = SPAN * H_E + 0.5 * SPAN * (H_R - H_E)
    print(f"roof {roof:.1f} m2, side walls {walls:.1f} m2, each gable {gable:.1f} m2; "
          f"one gable {roof + walls + gable:.1f} m2, both {roof + walls + 2 * gable:.1f} m2; two tarpaulins 48.0 m2")

    hr("9. Erection time estimate (R4)")
    solo = 36 * 20 / 60 + 8 * 2 + 10 * 1.5 + 20
    joint = 5 + 3 * 3
    print(f"one-person tasks {solo:.0f} person-min shared by two = {solo / 2:.1f} min; "
          f"two-person tasks (layout, raising 3 frames) {joint} min; total about {solo / 2 + joint:.0f} min")


if __name__ == "__main__":
    main()
