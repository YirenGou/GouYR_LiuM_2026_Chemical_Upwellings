"""
Two-panel figure on the mantle redox front (both panels drawn by this script).

a  Schematic carbon speciation diagram, redrawn from C_PhaseDiagram.jpg
   (boundaries and colours digitized from the CorelDRAW export).
b  Published constraints on the depth of the redox front (onset of carbonate
   melting in upwelling mantle) as a function of mantle oxidation state.

Data sources, placement rules and the figure caption: RedoxFront_references.md

v2: panel a carries a pressure axis (GPa) on its right side and panel b the same
pressure axis on its left side. Pressure follows the numerical models: depthp() in
markvis.c sets P = 3300 kg/m^3 * 9.80665 m/s^2 * depth below the surface, and
i2vis.c uses that P to place the redox front (4.5 or 10 GPa) and the carbonate
ledge (2.5 GPa).
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

HERE = Path(__file__).resolve().parent
OUT = HERE / "FigS1_v2"

Z_TOP, Z_BOT = 50.0, 350.0

# Pressure-depth conversion of the numerical models (depthp() in markvis.c)
RHO_MODEL, G_MODEL = 3300.0, 9.80665                 # kg/m^3, m/s^2
GPA_PER_KM = RHO_MODEL * G_MODEL * 1e3 / 1e9         # 0.03236 GPa/km
P_TICKS = [2, 4, 6, 8, 10]       # GPa


def p_of_z(z):
    return np.asarray(z, float) * GPA_PER_KM


def z_of_p(p):
    return np.asarray(p, float) / GPA_PER_KM

# =============================================================== panel a data
# Reduced | oxidized carbon boundary, digitized from C_PhaseDiagram.jpg: depth (km), dFMQ
A_BOUNDARY = np.array([
    (50.0, -4.64), (52.5, -4.40), (54.6, -4.21), (56.7, -4.01), (58.8, -3.82), (60.9, -3.63),
    (63.0, -3.44), (65.1, -3.25), (67.2, -3.065), (69.3, -2.88), (71.4, -2.71), (73.5, -2.54),
    (75.6, -2.39), (77.7, -2.24), (79.8, -2.13), (81.9, -2.01), (83.3, -1.934), (85.4, -1.84),
    (87.5, -1.76), (89.6, -1.704), (91.7, -1.655), (93.8, -1.618), (95.9, -1.587), (98.0, -1.565),
    (100.1, -1.546), (102.2, -1.531), (104.3, -1.52), (106.4, -1.516), (108.5, -1.508),
    (110.6, -1.508), (112.7, -1.51), (114.8, -1.516), (116.9, -1.52), (119.0, -1.523),
    (121.1, -1.531), (123.2, -1.538), (350.0, -2.264),
])
A_GD = 164.7                     # graphite | diamond
A_VAPOR, A_LEDGE = 87.9, 112.9   # CO2 vapor | carbonate ledge | carbonatite melt
A_COL = {"graphite": "#BBBBBB", "diamond": "#899ECA", "carbonatite": "#F08842",
         "magnesite": "#DA8AA2", "vapor": "#F8E176", "ledge": "#C66419"}


def a_boundary(z):
    return np.interp(z, A_BOUNDARY[:, 0], A_BOUNDARY[:, 1])


# =============================================================== panel b data
# ---- Stagno et al. (2013), Fig. 3a: dFMQ along a 1320 C adiabat for fixed bulk
#      Fe3+/SumFe, digitized at 107.9 and 245.9 km
STAGNO_ISO = {2: (-2.31, -4.46), 3: (-1.57, -3.76), 4: (-1.08, -3.23),
              5: (-0.69, -2.85), 6: (-0.37, -2.52), 7: (-0.085, -2.24)}
# their graphite/diamond-carbonate (EMOD/DCDM) curve: depth (km), dFMQ
STAGNO_DCDM = np.array([
    (57.6, -3.01), (63.6, -2.67), (69.5, -2.38), (75.4, -2.14), (81.3, -1.96),
    (87.2, -1.84), (93.1, -1.775), (99.0, -1.75), (110.9, -1.74), (135.0, -1.77),
    (158.0, -1.80), (170.0, -1.825), (182.0, -1.86), (200.0, -1.89), (211.0, -1.925),
    (223.0, -1.95), (235.0, -1.98), (247.0, -2.00),
])
Z_REF = 96.45          # depth of 3 GPa (PREM), reference level of the x axis
ISO_SLOPE = np.mean([(b - a) / (245.9 - 107.9) for a, b in STAGNO_ISO.values()])  # per km

# ---- Zhang et al. (2024), Fig. 10a: same type of diagram (Tp = 1320 C) extended to 15 %.
#      bulk Fe3+/SumFe (%) -> (dFMQ at 3 GPa, depth in km where the line meets the buffer).
#      15 % meets it at ~324 km, beyond the plotted end of their curve, and is not used.
ZHANG_FRONT = {2: (-2.12, 83), 3: (-1.37, 121), 4: (-0.89, 155), 5: (-0.47, 186),
               6: (-0.15, 209), 7: (0.11, 232), 8: (0.39, 250), 9: (0.62, 267),
               10: (0.76, 280), 11: (0.91, 291), 12: (1.11, 299), 13: (1.18, 307),
               14: (1.31, 316)}


def fmq_at_ref(fe3_pct):
    """dFMQ at 3 GPa of mantle with a given bulk Fe3+/SumFe (2-7 %), Stagno et al. (2013)."""
    pct = np.array(sorted(STAGNO_ISO))
    f108 = np.array([STAGNO_ISO[p][0] for p in pct])
    return np.interp(np.log10(fe3_pct), np.log10(pct), f108) + ISO_SLOPE * (Z_REF - 107.9)


def front_depth(x_ref):
    """Depth at which mantle with dFMQ = x_ref at 3 GPa meets Stagno's DCDM curve."""
    z = np.linspace(60, 247, 3741)
    d = x_ref + ISO_SLOPE * (z - Z_REF) - np.interp(z, STAGNO_DCDM[:, 0], STAGNO_DCDM[:, 1])
    i = np.nonzero(np.diff(np.sign(d)))[0]
    return z[i[-1]] if len(i) else np.nan


def x_of(pct):
    """Position on the lower axis of a bulk Fe3+/SumFe value (upper axis)."""
    return float(fmq_at_ref(np.array([pct]))[0]) if pct <= 7 else ZHANG_FRONT[pct][0]


A_XLIM = (-5.0, 1.0)
B_XLIM = (-2.8, 3.9)


def redox_front_curve():
    """fO2 and depth of the orange line (1) continued by the blue line (5).

    Vertices are the ones panel b plots, so a given log fO2 has the same depth
    on the white dashed line.
    """
    pct = np.array(sorted(STAGNO_ISO))
    xs = fmq_at_ref(pct)
    xx = np.linspace(float(xs[0]), float(xs[-1]), 200)
    zz = np.array([front_depth(float(x)) for x in xx])
    ext = [k for k in sorted(ZHANG_FRONT) if k > 7]
    x = np.r_[xx, [ZHANG_FRONT[k][0] for k in ext]]
    z = np.r_[zz, [float(ZHANG_FRONT[k][1]) for k in ext]]
    if np.any(np.diff(x) <= 0) or np.any(np.diff(z) <= 0):
        raise ValueError("redox-front curve is not increasing in fO2 and depth")
    return x, z


def clip_front_to_panel(x, z):
    """Redox front inside panel a.

    The left end stops at the first intersection with the black phase boundary
    or the dashed line under the carbonate ledge. It does not continue left
    of that point. The right end is the panel edge.
    """
    x_hi = A_XLIM[1]
    z_at_right = float(np.interp(x_hi, x, z))
    x_ledge = float(np.interp(A_LEDGE, z, x))
    d = x - a_boundary(z)
    i = np.where((d[:-1] <= 0) & (d[1:] > 0))[0]
    if len(i):
        i = int(i[0])
        t = float(-d[i] / (d[i + 1] - d[i]))
        x_cross = float(x[i] + t * (x[i + 1] - x[i]))
    else:
        x_cross = float(x[0])
    # the intersection further to the right is the one reached first from the right
    x_left = max(x_ledge, x_cross)
    z_left = float(np.interp(x_left, x, z))
    keep = (x > x_left) & (x < x_hi)
    return np.r_[x_left, x[keep], x_hi], np.r_[z_left, z[keep], z_at_right]


# ==================================================================== styling
COL = {"c1": "#D55E00", "c3": "#009E73", "c5": "#0072B2", "data": "#3C3C3C", "line": "#231916"}
FS_TICK, FS_LAB, FS_NOTE, FS_NUM, FS_PANEL = 9, 10, 8, 7.5, 12


def style_axes(ax):
    ax.set_ylim(Z_BOT, Z_TOP)
    ax.set_yticks([100, 150, 200, 250, 300])
    ax.tick_params(labelsize=FS_TICK)


def panel_a(ax, front):
    """front: (fO2, depth) of the orange and blue lines, clipped to panel a."""
    x_f, z_f = front
    x_full, z_full = redox_front_curve()
    z = np.r_[np.linspace(Z_TOP, 124, 400), Z_BOT]
    xb = a_boundary(z)

    def right_of_boundary(z1, z2, extra):
        zz = np.r_[z1, z[(z > z1) & (z < z2)], z2]
        return np.r_[np.c_[a_boundary(zz), zz], extra]

    # Below the ledge, the same fO2 has the same depth as in panel b.
    # Shallower than that depth: carbonatite. Deeper: magnesite.
    zz = np.linspace(A_LEDGE, Z_BOT, 500)
    x_front = np.interp(zz, z_full, x_full, left=x_full[0], right=A_XLIM[1] + 1.0)
    x_bound = a_boundary(zz)
    x_right = np.full_like(zz, A_XLIM[1])
    carb = x_front < A_XLIM[1]
    ax.fill_betweenx(zz[carb], np.maximum(x_bound[carb], x_front[carb]), x_right[carb],
                     color=A_COL["carbonatite"], lw=0)
    ax.fill_betweenx(zz, x_bound, np.minimum(x_front, A_XLIM[1]),
                     where=x_front > x_bound, color=A_COL["magnesite"], lw=0)

    zg = np.r_[z[z < A_GD], A_GD]
    ax.fill_betweenx(zg, A_XLIM[0], a_boundary(zg), color=A_COL["graphite"], lw=0)
    zd = np.linspace(A_GD, Z_BOT, 50)
    ax.fill_betweenx(zd, A_XLIM[0], a_boundary(zd), color=A_COL["diamond"], lw=0)
    for z1, z2, key, extra in [
        (Z_TOP, A_VAPOR, "vapor", [(A_XLIM[1], A_VAPOR), (A_XLIM[1], Z_TOP)]),
        (A_VAPOR, A_LEDGE, "ledge", [(A_XLIM[1], A_LEDGE), (A_XLIM[1], A_VAPOR)]),
    ]:
        ax.add_patch(Polygon(right_of_boundary(z1, z2, extra), closed=True, fc=A_COL[key], ec="none"))

    lk = dict(color=COL["line"], lw=1.2, solid_capstyle="round")
    ax.plot(xb, z, **lk)
    ax.plot([A_XLIM[0], a_boundary(A_GD)], [A_GD, A_GD], **lk)
    for zl in (A_VAPOR, A_LEDGE):
        ax.plot([a_boundary(zl), A_XLIM[1]], [zl, zl], color=COL["line"], lw=1.0, ls=(0, (5, 2.5)))
    ax.plot(x_f, z_f, color="white", lw=1.3, ls=(0, (6, 2.5)), zorder=4)

    tk = dict(ha="center", va="center", fontsize=FS_LAB, color=COL["line"])
    ax.text(-0.15, 68, r"CO$_2$ vapor", **tk)
    ax.text(-3.5, 108, "Graphite", **tk)
    ax.text(-3.5, 258, "Diamond", **tk)
    ax.text(0.05, 142, "Carbonatite\n(melt)", linespacing=1.15, **tk)
    ax.text(-0.85, 250, "Magnesite\n(solid)", linespacing=1.15, **tk)
    wt = dict(ha="center", va="center", fontsize=FS_NOTE + 0.5, color="white", style="italic")
    ax.text(-0.25, 0.5 * (A_VAPOR + A_LEDGE), "Carbonate ledge", **wt)

    # on the carbonatite side of the front, rotated to the local slope
    rx = -0.2
    rz = float(np.interp(rx, x_f, z_f))
    i = int(np.searchsorted(x_f, rx))
    i = min(max(i, 1), len(x_f) - 1)
    p1, p2 = ax.transData.transform([(x_f[i - 1], z_f[i - 1]), (x_f[i], z_f[i])])
    ang = np.degrees(np.arctan2(p2[1] - p1[1], p2[0] - p1[0]))
    perp = np.array([-(p2[1] - p1[1]), p2[0] - p1[0]])
    perp /= np.hypot(*perp)
    mid = ax.transData.transform((rx, rz))
    if ax.transData.inverted().transform(mid + perp)[1] > rz:
        perp = -perp
    gap = 0.75 * (FS_NOTE + 0.5) / 72.0 * ax.figure.dpi
    rx, rz = ax.transData.inverted().transform(mid + perp * gap)
    ax.text(rx, rz, "Redox front ?", rotation=ang, rotation_mode="anchor", **wt)

    ax.set_xticks([-4, -3, -2, -1, 0])
    ax.set_xlabel(r"Log $f$O$_2$ (relative to FMQ)", fontsize=FS_LAB, labelpad=3)
    ax.set_ylabel("Depth (km)", fontsize=FS_LAB, labelpad=3)

    axp = ax.secondary_yaxis("right", functions=(p_of_z, z_of_p))
    axp.set_yticks(P_TICKS)
    axp.tick_params(labelsize=FS_TICK)
    axp.set_ylabel("Pressure (GPa)", fontsize=FS_LAB, labelpad=3)


def panel_b(ax):
    X0, X_SPLIT, X1 = B_XLIM[0], 1.5, B_XLIM[1]
    ax.set_xlim(X0, X1)
    # left axis: pressure, same ticks as the right axis of panel a
    ax.set_yticks(z_of_p(P_TICKS))
    ax.set_yticklabels([str(p) for p in P_TICKS])
    ax.set_xticks([-2, -1, 0, 1])
    # same axis title as panel a; the caption states that b is referenced to 3 GPa
    ax.set_xlabel(r"Log $f$O$_2$ (relative to FMQ)", fontsize=FS_LAB, labelpad=3)
    ax.xaxis.set_label_coords(0.5 * (X_SPLIT - X0) / (X1 - X0), -0.085)

    ck = dict(ms=5.5, mfc="white", mew=1.4)

    # ---- trends of redox-front depth with oxidation state (circles and lines)
    # (1) Stagno et al. 2013: Fe3+/SumFe = 2-7 %
    pct = np.array(sorted(STAGNO_ISO))
    xs = fmq_at_ref(pct)
    zs = np.array([front_depth(x) for x in xs])
    xx = np.linspace(xs[0], xs[-1], 200)
    ax.plot(xx, [front_depth(x) for x in xx], color=COL["c1"], lw=1.4, zorder=4)
    ax.plot(xs, zs, "o", mec=COL["c1"], zorder=6, **ck)
    ax.text(xs[0] - 0.12, zs[0] - 2, "1", fontsize=FS_NUM, color=COL["c1"], ha="right", va="center")
    # (3) Stagno & Frost 2010: onset at <100 km for Fe3+/SumFe = 0.03, <150 km for ~0.1
    sx, sz = [x_of(3), x_of(10)], [100.0, 150.0]
    ax.plot(sx, sz, color=COL["c3"], lw=1.4, zorder=4)
    ax.plot(sx, sz, "o", mec=COL["c3"], zorder=6, **ck)
    ax.text(sx[0] + 0.14, sz[0] - 3, "3", fontsize=FS_NUM, color=COL["c3"], ha="left", va="center")
    # (5) Zhang et al. 2024: the same calculation as (1), continued to 8-14 %
    ext = [p for p in sorted(ZHANG_FRONT) if p > 7]
    zx = np.array([ZHANG_FRONT[p][0] for p in ext])
    zz = np.array([ZHANG_FRONT[p][1] for p in ext])
    ax.plot(np.r_[xs[-1], zx], np.r_[zs[-1], zz], color=COL["c5"], lw=1.4, zorder=3)
    ax.plot(zx, zz, "o", mec=COL["c5"], zorder=5, **ck)
    ax.text(zx[-1] + 0.02, zz[-1] + 13, "5", fontsize=FS_NUM, color=COL["c5"], ha="center", va="center")

    # ---- single estimates: open square at the reported value or mid-range,
    #      capped bars for the reported range
    def point(x, z, num, xerr=None, zerr=None, dx=0.0, dz=0.0, ha="center", va="bottom"):
        ax.errorbar(x, z, xerr=xerr, yerr=zerr, fmt="s", ms=4.8, mfc="white", mec=COL["data"],
                    mew=1.2, ecolor=COL["data"], elinewidth=1.1, capsize=2.5, capthick=1.1, zorder=7)
        up = zerr[0][0] if isinstance(zerr, list) else (zerr or 0)
        ax.text(x + dx, z - up - 4 + dz, num, fontsize=FS_NUM, color=COL["data"], ha=ha, va=va)

    def span(x, z1, z2, num, **kw):
        point(x, 0.5 * (z1 + z2), num, zerr=0.5 * (z2 - z1), **kw)

    def below(z1, z2):          # keyword arguments that put the label under the bar
        return dict(dz=(z2 - z1) + 8, va="top")

    # (2) Aulbach & Stagno 2016: Archaean mantle, Tp = 1420 C, Fe3+/SumFe = 2 %, ~100 km;
    #     x bar = +/-0.33 log units, the 2-sigma of their Archaean fO2
    point(x_of(2), 100, "2", xerr=0.33, dz=9, va="top")
    # (4) Davis & Cottrell 2021: MORB source Fe3+/SumFe = 5.3 +/- 0.3 %; 200-230 km
    dc = fmq_at_ref(np.array([5.0, 5.3, 5.6]))
    point(dc[1], 215, "4", xerr=[[dc[1] - dc[0]], [dc[2] - dc[1]]], zerr=15, dx=-0.16, dz=19,
          ha="right", va="center")
    # (5) Zhang et al. 2024: MORB source Fe3+/SumFe = 6-8 % -> carbonate melting at 200-250 km
    z6, z7, z8 = (ZHANG_FRONT[k][0] for k in (6, 7, 8))
    point(z7, 225, "5", xerr=[[z7 - z6], [z8 - z7]], zerr=25, dx=0.1)

    # ---- depth-only studies, ordered by the deepest reported depth
    ax.axvline(X_SPLIT, color="0.6", lw=0.7, zorder=1)
    ax.text(0.5 * (X_SPLIT + X1), Z_TOP + 10, "Depth only studies", fontsize=FS_NOTE, color="0.35",
            ha="center", va="center")
    xb = np.linspace(X_SPLIT + 0.2, X1 - 0.2, 9)
    span(xb[0], 150, 240, "6", **below(150, 240))      # Fux et al. 2025: ~8-5 GPa, "240-150 km"
    span(xb[1], 150, 250, "7")                         # Yaxley et al. 2019 (review)
    span(xb[2], 200, 250, "8")                         # Dasgupta et al. 2013: redox front
    span(xb[3], 230, 250, "9")                         # Schmidt et al. 2026
    point(xb[4], 250, "10", dz=12, va="top")           # Rohrbach & Schmidt 2011
    point(xb[5], 260, "11", dz=12, va="top")           # seismic: Gu et al. 2005; Hua et al. 2023
    span(xb[6], 200, 330, "12")                        # Dasgupta & Hirschmann 2006
    span(xb[7], 270, 330, "13", **below(270, 330))     # Dasgupta et al. 2013: locally oxidized mantle
    point(xb[8], 255, "14", zerr=[[255 - 180], [340 - 255]])  # Sun & Zhou 2023: mean and range

    # ---- top axis: equivalent bulk Fe3+/SumFe (2-7 % Stagno et al. 2013, 8-14 % Zhang et al. 2024)
    axt = ax.twiny()
    axt.set_xlim(X0, X1)
    axt.set_xticks(list(xs) + list(zx))
    axt.set_xticklabels([str(p) for p in pct] + [str(p) if p in (8, 10, 14) else "" for p in ext],
                        fontsize=FS_TICK)
    axt.set_xlabel(r"Bulk Fe$^{3+}$/$\Sigma$Fe (%)", fontsize=FS_LAB, labelpad=4)
    axt.xaxis.set_label_coords(0.5 * (xs[0] + zx[-1] - 2 * X0) / (X1 - X0), 1.085)
    return pct, xs, zs, axt.xaxis.label


def main():
    plt.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "mathtext.fontset": "custom", "mathtext.rm": "Arial", "mathtext.it": "Arial:italic",
        "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
        "axes.linewidth": 1.0, "xtick.major.width": 1.0, "ytick.major.width": 1.0,
        "xtick.major.size": 3.5, "ytick.major.size": 3.5, "xtick.direction": "out",
        "ytick.direction": "out", "savefig.dpi": 600,
    })

    # ---- layout in mm (Nature double column = 183 mm); both frames share top and bottom
    W, H = 183.0, 103.0
    top, height = 13.0, 77.0
    a_left, a_w = 14.0, 64.0      # v2: narrower, room for the two pressure axes
    b_left, b_right = 98.0, 180.0

    def box(left, width):
        return [left / W, 1 - (top + height) / H, width / W, height / H]

    fig = plt.figure(figsize=(W / 25.4, H / 25.4))
    axa = fig.add_axes(box(a_left, a_w))
    axb = fig.add_axes(box(b_left, b_right - b_left))
    for ax in (axa, axb):
        style_axes(ax)
    axa.set_xlim(*A_XLIM)
    x_full, z_full = redox_front_curve()
    front = clip_front_to_panel(x_full, z_full)
    panel_a(axa, front)
    pct, xs, zs, top_label = panel_b(axb)

    # panel letters on the baseline of the top-axis title of panel b
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    bb = top_label.get_window_extent(rend)
    _, _, descent = rend.get_text_width_height_descent(top_label.get_text(),
                                                       top_label.get_fontproperties(), ismath=True)
    y_base = (bb.y0 + descent) / fig.bbox.height
    for x_mm, lab in ((1.0, "a"), (b_left - 8.5, "b")):
        fig.text(x_mm / W, y_base, lab, fontsize=FS_PANEL, fontweight="bold", va="baseline", ha="left")

    for suffix in ("png", "pdf", "svg"):
        try:
            fig.savefig(OUT.with_suffix("." + suffix))
        except PermissionError:     # file open in another program
            print(f"NOT written (file is open elsewhere): {OUT.name}.{suffix}")
    x_f, z_f = front
    print("depth at the same log fO2 on the white line and on lines 1 and 5:")
    for x_chk in (-2.0, -1.0, 0.0, 1.0):
        print(f"  {x_chk:+.0f}: {float(np.interp(x_chk, x_f, z_f)):.1f} km")
    for p, x, z in zip(pct, xs, zs):
        print(f"Fe3+/SumFe {p}%: dFMQ(3 GPa) {x:+.2f}, redox front {z:.0f} km")
    for p_chk in (2.5, 4.5, 10.0):
        print(f"{p_chk:4.1f} GPa = {float(z_of_p(p_chk)):.1f} km (model conversion)")
    print("wrote", OUT.name + ".png/.pdf/.svg")


if __name__ == "__main__":
    main()
