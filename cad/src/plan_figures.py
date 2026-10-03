"""SnapFrame build plan figures that need no 3D model: the tarpaulin cutting plan and the packing picture (SNF-BLD-001).

Run from the repo root:  python cad/src/plan_figures.py [cutting] [packing]
Writes docs/05-build-plan/cutting-plan.png (from cad/src/skin_plan.py) and docs/05-build-plan/packing.png (from
docs/04-calcs/sizing-results.json, written by docs/04-calcs/sizing.py). BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
import model as M  # noqa: E402
import skin_plan as SK  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"


def _text_clashes(fig):
    """Names of text pairs whose boxes overlap, and of texts outside the figure (a check done before saving)."""
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    W, H = fig.canvas.get_width_height()
    items = []
    for t in fig.findobj(lambda o: hasattr(o, "get_text") and hasattr(o, "get_window_extent")):
        if not t.get_text().strip() or not t.get_visible():
            continue
        items.append((t.get_text().replace("\n", " ")[:30], t.get_window_extent(rend)))
    bad = []
    for i, (n1, b1) in enumerate(items):
        if b1.x0 < 0 or b1.y0 < 0 or b1.x1 > W or b1.y1 > H:
            bad.append(("outside", n1))
        for n2, b2 in items[i + 1:]:
            if b1.overlaps(b2) and min(b1.x1, b2.x1) - max(b1.x0, b2.x0) > 2 and min(b1.y1, b2.y1) - max(b1.y0, b2.y0) > 2:
                bad.append((n1, n2))
    return bad


def cutting_plan():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Polygon
    INK, MUT, AC, WARN = "#111827", "#4B5563", "#0F766E", "#B45309"
    fig, axs = plt.subplots(3, 1, figsize=(7.6, 13.2), dpi=150)
    fig.subplots_adjust(left=0.03, right=0.97, top=0.88, bottom=0.115, hspace=0.3)
    fig.text(0.04, 0.978, "Three tarpaulins, cut up", fontsize=14, fontweight="bold", color=INK, va="top")
    fig.text(0.04, 0.953, "Each 4 x 6 m tarpaulin drawn to scale (metres). Grey is spare.\nOrange is the edge that stands on the ground; the small cut-outs at its "
             "two ends are the corner cable hems.", fontsize=8.5, color=MUT, va="top", linespacing=1.4)
    fills = {"Roof sheet": "#93C5FD", "wall": "#BFDBFE", "door": "#BFDBFE", "tri2": "#C7D2FE"}
    NW, NH = SK.NOTCH_W, SK.NOTCH_H

    def base(ax, t, title):
        ax.set_xlim(-0.6, 6.6); ax.set_ylim(-0.55, 4.45); ax.set_aspect("equal"); ax.set_axis_off()
        ax.add_patch(Rectangle((0, 0), 6.0, 4.0, fc="#F3F4F6", ec=INK, lw=1.4))
        ax.text(-0.55, 4.28, title, fontsize=10, fontweight="bold", color=INK, va="bottom")
        ax.annotate("", xy=(0, -0.28), xytext=(6.0, -0.28), arrowprops=dict(arrowstyle="<->", color=MUT, lw=0.8))
        ax.text(3.0, -0.34, "6.0 m", ha="center", va="top", fontsize=8, color=MUT)
        ax.annotate("", xy=(6.28, 0), xytext=(6.28, 4.0), arrowprops=dict(arrowstyle="<->", color=MUT, lw=0.8))
        ax.text(6.36, 2.0, "4.0 m", rotation=90, va="center", fontsize=8, color=MUT)

    def strip(ax, p, ground, label, door=False):
        t, name, u0, v0, w, h, shape, note = p
        ax.add_patch(Rectangle((u0, v0), w, h, fc="#BFDBFE", ec=INK, lw=1.2))
        # ground edge and corner cable hems
        if ground == "bottom":
            ax.plot([u0, u0 + w], [v0, v0], color=WARN, lw=3)
            cuts = [(u0, v0), (u0 + w - NW, v0)]; cdim = (NW, NH)
        elif ground == "top":
            ax.plot([u0, u0 + w], [v0 + h, v0 + h], color=WARN, lw=3)
            cuts = [(u0, v0 + h - NH), (u0 + w - NW, v0 + h - NH)]; cdim = (NW, NH)
        else:
            ax.plot([u0 + w, u0 + w], [v0, v0 + h], color=WARN, lw=3)
            cuts = [(u0 + w - NH, v0), (u0 + w - NH, v0 + h - NW)]; cdim = (NH, NW)
        for cx, cy in cuts:
            ax.add_patch(Rectangle((cx, cy), cdim[0], cdim[1], fc="#F3F4F6", ec=INK, lw=0.9))
        ax.text(u0 + w / 2, v0 + h / 2 + (0.28 if door else 0), label, ha="center", va="center", fontsize=8.5, color=INK)

    ax = axs[0]; base(ax, 1, "Tarpaulin 1: the roof")
    ax.add_patch(Rectangle((0, 0), 6.0, 4.0, fc=fills["Roof sheet"], ec=INK, lw=1.2))
    r = SK.RAFTER
    for u, lab in ((3.0 - r, "eave line"), (3.0 + r, "eave line")):
        ax.plot([u, u], [0, 4.0], color=MUT, lw=0.9, ls=":")
        ax.text(u, 4.08, lab, ha="center", fontsize=7.5, color=MUT)
    ax.plot([3.0, 3.0], [0, 4.0], color=AC, lw=1.1, ls="--"); ax.text(3.0, 4.08, "ridge", ha="center", fontsize=7.5, color=AC)
    ax.text(3.0, 2.0, "Roof sheet, used whole\nover the ridge, 24.0 m\u00b2", ha="center", va="center", fontsize=9, color=INK)
    ax.text(0.42, 2.0, f"{(6.0 - 2 * r) / 2:.2f} m skirt past the eave", ha="center", va="center", rotation=90, fontsize=7, color=MUT)

    ax = axs[1]; base(ax, 2, "Tarpaulin 2: the two side walls and the rear gable")
    pcs = [p for p in SK.PIECES if p[0] == 2]
    strip(ax, pcs[0], "bottom", "Side wall, left\n4.0 x 2.0 m, 8.0 m\u00b2")
    strip(ax, pcs[1], "top", "Side wall, right\n4.0 x 2.0 m, 8.0 m\u00b2")
    strip(ax, pcs[2], "right", "Rear gable,\nlower part\n2.0 x 4.0 m,\nturned", )

    ax = axs[2]; base(ax, 3, "Tarpaulin 3: front gable with door flap, gable tops")
    ax.add_patch(Rectangle((4.0, 0), 2.0, 2.0, fc="#E5E7EB", ec=MUT, lw=0.8, hatch="///"))
    ax.add_patch(Rectangle((0, 2.9), 6.0, 1.1, fc="#E5E7EB", ec=MUT, lw=0.8, hatch="///"))
    ax.text(5.0, 1.0, "spare\n4.0 m\u00b2", ha="center", va="center", fontsize=8, color=MUT)
    ax.text(3.0, 3.45, "spare 6.6 m\u00b2", ha="center", va="center", fontsize=8, color=MUT)
    front = [p for p in SK.PIECES if p[0] == 3][0]
    strip(ax, front, "bottom", "", door=True)
    dw, dh = SK.DOOR_W, SK.DOOR_H
    ax.add_patch(Rectangle((2.0 - dw / 2, 0), dw, dh, fc="#FDE68A", ec=INK, lw=1.0, hatch="..."))
    ax.plot([2.0 - dw / 2, 2.0 + dw / 2], [dh, dh], color=INK, lw=1.4, ls="--")
    ax.text(2.0, dh + 0.1, "hinge (uncut)", ha="center", fontsize=7, color=INK)
    ax.text(0.8, 0.95, "door flap\n1.0 x 1.7 m,\ncut by two\nslits", ha="center", va="center", fontsize=7.5, color=INK)
    ax.text(3.2, 1.1, "Front gable,\nlower part\n4.0 x 2.0 m,\n8.0 m\u00b2", ha="center", va="center", fontsize=8.5, color=INK)
    ax.add_patch(Polygon([(0, 2.0), (4.0, 2.0), (2.0, 2.9)], fc="#C7D2FE", ec=INK, lw=1.2))
    ax.add_patch(Polygon([(2.0, 2.9), (6.0, 2.9), (4.0, 2.0)], fc="#A5B4FC", ec=INK, lw=1.2))
    ax.text(2.0, 2.25, "front gable top", ha="center", fontsize=7.5, color=INK)
    ax.text(4.0, 2.65, "rear gable top", ha="center", fontsize=7.5, color=INK)
    fig.text(0.04, 0.092, f"Frame needs {SK.needs()['total']:.1f} m\u00b2 of skin; three tarpaulins give 72.0 m\u00b2 and the pieces use {72 - SK.spare():.1f} m\u00b2.\n"
             f"Spare in all {SK.spare():.1f} m\u00b2 (with the offcuts beside the triangles).\nCorner cable hem: a {NW * 1000:.0f} x {NH * 1000:.0f} mm cut-out, edges folded and taped.",
             fontsize=8, color=MUT, va="top", linespacing=1.4)
    fig.text(0.04, 0.008, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color=WARN)
    fig.text(0.97, 0.008, "github.com/BoujeeEnjinia1701/snapframe", fontsize=7, color=AC, ha="right", family="monospace")
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / "cutting-plan.png"
    print("text clashes:", _text_clashes(fig))
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


def packing():
    import json
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
    INK, MUT, AC, WARN = "#111827", "#4B5563", "#0F766E", "#B45309"
    R = json.loads((ROOT / "docs" / "04-calcs" / "sizing-results.json").read_text())
    fig, axs = plt.subplots(1, 3, figsize=(11, 5.4), dpi=150, gridspec_kw={"width_ratios": [1, 1, 1.25]})
    fig.subplots_adjust(left=0.03, right=0.98, top=0.8, bottom=0.2, wspace=0.12)
    fig.text(0.03, 0.965, "How the kit is packed: three packages", fontsize=14, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.915, "Each package is 25 kg or less. Tubes are drawn from the end, to scale; the two tube bundles are strapped with two cam straps each.",
             fontsize=8.5, color=MUT, va="top")

    def bundle(ax, title, od, rows, col, lines):
        ax.set_xlim(-6, 6); ax.set_ylim(-4.2, 9.2); ax.set_aspect("equal"); ax.set_axis_off()
        ax.text(0, 8.7, title, ha="center", fontsize=10, fontweight="bold", color=INK)
        r = od / 20.0
        y0 = 0.0
        for j, n in enumerate(rows):
            y = y0 + j * r * 1.75
            for i in range(n):
                x = (i - (n - 1) / 2) * r * 2.0
                ax.add_patch(Circle((x, y), r, fc=col, ec=INK, lw=0.8)); ax.add_patch(Circle((x, y), r * 0.8, fc="white", ec="none"))
        ax.add_patch(Rectangle((-max(rows) * r - 0.3, -r - 0.3), 2 * max(rows) * r + 0.6, (len(rows) - 1) * r * 1.75 + 2 * r + 0.6,
                               fc="none", ec=WARN, lw=1.6, ls="--"))
        for k, t in enumerate(lines):
            ax.text(0, -2.3 - k * 0.8, t, ha="center", fontsize=8, color=INK)
    one = M.TUBES["1"]["od"]; tq = M.TUBES["3/4"]["od"]
    bundle(axs[0], "Tube bundle A", one, [3, 3, 2], "#F59E0B",
           ["6 rafters 2.064 m, 2 ridge tubes 1.910 m", "1 in conduit, 8 tubes",
            f"{R['bundle_a_kg']:.1f} kg, {R['bundle_a_m3']:.3f} m\u00b3, 2 cam straps"])
    bundle(axs[1], "Tube bundle B", tq, [4, 3, 3], "#38BDF8",
           ["6 posts 1.650 m, 4 eave tubes 1.910 m", "3/4 in conduit, 10 tubes",
            f"{R['bundle_b_kg']:.1f} kg, {R['bundle_b_m3']:.3f} m\u00b3, 2 cam straps"])
    ax = axs[2]; ax.set_xlim(0, 10); ax.set_ylim(-4.2, 9.2); ax.set_axis_off()
    ax.text(5, 8.7, "The bag", ha="center", fontsize=10, fontweight="bold", color=INK)
    ax.add_patch(FancyBboxPatch((0.6, 0.4), 8.8, 7.4, boxstyle="round,pad=0.1,rounding_size=0.5", fc="#F3F4F6", ec=INK, lw=1.4))
    items = ["15 printed nodes, nested", "10 brace cables with hooks", "9 cable bolt sets", "6 screw anchors, 2 long anchors",
             "2 guy lines", "buttons, hitch pins, caps", "folding step, folded", "layout cord and pegs"]
    for k, t in enumerate(items):
        ax.text(1.0, 7.2 - k * 0.85, "\u2022 " + t, fontsize=8, color=INK)
    ax.text(5, -0.5, "Duffel bag about 0.08 m\u00b3", ha="center", fontsize=8, color=INK)
    ax.text(5, -1.3, f"{R['bag_kg']:.1f} kg, about {R['bag_m3']:.3f} m\u00b3 of contents", ha="center", fontsize=8, color=INK)
    ax.text(5, -2.1, "The three tarpaulins come from agency stock", ha="center", fontsize=8, color=MUT)
    ax.text(5, -2.9, f"and are not in the bag ({R['tarps_kg']:.1f} kg for three)", ha="center", fontsize=8, color=MUT)
    fig.text(0.03, 0.05, f"Frame kit {R['frame_kit_kg']:.1f} kg in all, carried by two people. Longest member 2.064 m.", fontsize=8.5, color=INK)
    fig.text(0.98, 0.012, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color=WARN, ha="right")
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / "packing.png"
    print("text clashes:", _text_clashes(fig))
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out




if __name__ == "__main__":
    for w in (sys.argv[1:] or ["cutting", "packing"]):
        print(w, "->", {"cutting": cutting_plan, "packing": packing}[w]())
