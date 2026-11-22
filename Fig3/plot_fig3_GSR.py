"""
Nature-style Fig. 3: Reduced Mantle (left) vs Oxidized Mantle (right).

Reads gouc*.txt (material field, RLE-compressed) from Reduced/ and Oxidized/,
using the zoom / colour map from vis_cto3.m and the layout style of plot_fig4.py.
"""

import os
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Rectangle

# ---------------------------------------------------------------------------
# Paths & cases
# ---------------------------------------------------------------------------
BASE = Path(__file__).resolve().parent
REDUCED_DIR = Path(os.environ.get("GSR_REDUCED_DATA_OVERRIDE", BASE / "Fig3a_Reduced_Moho55km_GSR"))
OXIDIZED_DIR = Path(os.environ.get("GSR_OXIDIZED_DATA_OVERRIDE", BASE / "Fig3b_Oxidized_Moho55km_GSR"))

# File steps (gouc{N}.txt) — chronological snapshots for each model
STEPS_REDUCED = [0, 70, 130, 180]
STEPS_OXIDIZED = [0, 80, 160, 360]  # 360 time-matches original 280

# Model / zoom (km) — same as vis_cto3.m
X_SIZE, Z_SIZE = 2000.0, 420.0
X_BEG, X_END = 500.0, 1500.0
Z_BEG, Z_END = 0.0, 420.0
Z_OFFSET = 10.0  # MATLAB: z_vec = z_vec - 10

# Nature double-column figure (~183 mm wide)
FIG_W_IN = 183 / 25.4
DPI = 600

# Panel row gap as a fraction of panel height (0 = touching).
HSPACE = 0.05

# Legend swatch size (pt)
LEGEND_SWATCH_W_PT = 18
LEGEND_SWATCH_H_PT = 12
LEGEND_LABEL_GAP = 0.06

# Material legend (index → name), colours from composition colormap
MATERIAL_LEGEND = [
    (0, "Air"),
    (5, "Upper Crust"),
    (6, "Lower Crust"),
    (8, "Mantle Lithosphere"),
    (10, "Asthenosphere"),
    (15, "Carbonated Mantle"),
    (16, "Molten Mantle"),
]

OUT_PNG = Path(os.environ.get("GSR_OUTPUT_OVERRIDE", BASE / "Fig3_Reduced_vs_Oxidized_GSR.png"))


def figure_height_in(n_rows: int, *, hspace: float, bottom: float, top: float) -> float:
    """Height so equal-aspect panels pack tightly with the given hspace."""
    left, right = 0.08, 0.98
    usable_w = FIG_W_IN * (right - left)
    panel_w = usable_w / (2.0 + 0.12)  # account for wspace
    data_aspect = (Z_END - Z_BEG) / (X_END - X_BEG)
    panel_h = panel_w * data_aspect
    axes_block = n_rows * panel_h * (1.0 + hspace) - hspace * panel_h
    return axes_block / (top - bottom)


# ---------------------------------------------------------------------------
# Material colormap (vis_cto3.m C_map, indices 0–38)
# ---------------------------------------------------------------------------
def _hex_rgb(h: str) -> list[float]:
    h = h.lstrip("#")
    return [int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4)]


def material_cmap():
    # Scheme 02 sediment_ochre (Nature-leaning geological categorical).
    # Legend materials overwritten; unused indices keep MATLAB C_map hues.
    colors = np.array(
        [
            [1.00000, 1.00000, 1.00000],  # 0 Air
            [238 / 255, 232 / 255, 170 / 255],  # 1
            [238 / 255, 232 / 255, 170 / 255],  # 2
            [0.9290, 0.6940, 0.1250],  # 3
            [0.8500, 0.3250, 0.0980],  # 4
            _hex_rgb("#F2E6C8"),  # 5 Upper Crust
            _hex_rgb("#C9A66B"),  # 6 Lower Crust
            _hex_rgb("#6B8F71"),  # 7 Dry ML
            _hex_rgb("#6B8F71"),  # 8 Mantle Lithosphere
            [0.3010, 1.0000, 1.0000],  # 9
            _hex_rgb("#E8C4A8"),  # 10 Asthenosphere
            _hex_rgb("#8FA8B0"),  # 11 Mantle Transition Zone
            [152 / 255, 79 / 255, 49 / 255],  # 12 Dry Ec
            [44 / 255, 47 / 255, 59 / 255],  # 13 Dry Pyr
            _hex_rgb("#A03C3C"),  # 14 Carbonatite
            _hex_rgb("#3D3D3D"),  # 15 Buoyant Mantle
            _hex_rgb("#A8A0A0"),  # 16 Molten Mantle
            [0.50196, 0.50196, 0.00000],  # 17
            [0.50196, 0.50196, 0.00000],  # 18
            [1.00000, 1.00000, 1.00000],  # 19
            [1.00000, 1.00000, 1.00000],  # 20
            [1.00000, 1.00000, 1.00000],  # 21
            [1.00000, 1.00000, 1.00000],  # 22
            [1.00000, 1.00000, 0.80000],  # 23
            [1.00000, 1.00000, 0.31765],  # 24
            [0.92549, 0.35294, 0.72941],  # 25
            [0.74510, 0.27451, 0.58824],  # 26
            [0.00000, 1.00000, 0.00000],  # 27
            [0.00000, 1.00000, 0.00000],  # 28
            [1.00000, 0.00000, 0.00000],  # 29
            [1.00000, 0.00000, 0.00000],  # 30
            [1.00000, 0.00000, 0.00000],  # 31
            [1.00000, 0.00000, 0.00000],  # 32
            [1.00000, 0.00000, 0.00000],  # 33
            [1.00000, 0.00000, 0.00000],  # 34
            [1.00000, 1.00000, 0.31765],  # 35
            [0.00000, 1.00000, 0.00000],  # 36
            [0.00000, 1.00000, 0.00000],  # 37
            [0.00000, 1.00000, 0.00000],  # 38
        ]
    )
    cmap = ListedColormap(colors)
    cmap.set_bad("white")
    bounds = np.arange(-0.5, len(colors) + 0.5, 1.0)
    norm = BoundaryNorm(bounds, cmap.N)
    return cmap, norm, colors


# ---------------------------------------------------------------------------
# I/O
# ---------------------------------------------------------------------------
def load_numbers(path: Path) -> np.ndarray:
    """Load whitespace-separated floats (handles irregular column counts)."""
    return np.fromfile(path, sep=" ", dtype=np.float64)


def decode_composition(path: Path) -> tuple[float, np.ndarray]:
    """Decode RLE composition file → (time_yr, grid[nz, nx]), MATLAB order."""
    data = load_numbers(path)
    time = float(data[0])
    nx = int(data[1])
    nz = int(data[2])
    vec = data[3:]

    flat = np.ones(nz * nx, dtype=np.float64)
    num = 0
    ind = 0
    n = len(vec)
    while num < n:
        value = vec[num]
        if value == -2:
            n_colors = int(vec[num + 1])
            material = vec[num + 2]
            flat[ind : ind + n_colors] = material
            ind += n_colors
            num += 3
        else:
            flat[ind] = np.nan if value == -1 else value
            ind += 1
            num += 1

    grid = flat.reshape((nz, nx), order="F")
    return time, grid


def zoom_composition(grid: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Zoom composition grid and build x/z coordinate vectors (km)."""
    nz, nx = grid.shape
    x_beg_i = 0 if X_BEG == 0 else int(round((X_BEG / X_SIZE) * nx))
    x_end_i = int(round((X_END / X_SIZE) * nx))
    z_beg_i = 0 if Z_BEG == 0 else int(round((Z_BEG / Z_SIZE) * nz))
    z_end_i = int(round((Z_END / Z_SIZE) * nz))

    if Z_BEG == 0 and X_BEG != 0:
        z_beg_i = 0
    cropped = grid[z_beg_i:z_end_i, x_beg_i:x_end_i]

    nz_c, nx_c = cropped.shape
    x = np.linspace(X_BEG, X_END, nx_c)
    z = np.linspace(Z_BEG, Z_END, nz_c) - Z_OFFSET
    return cropped, x, z


# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------
def apply_nature_style():
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
            "font.size": 9,
            "axes.labelsize": 10,
            "axes.titlesize": 10,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "axes.linewidth": 0.6,
            "xtick.major.width": 0.6,
            "ytick.major.width": 0.6,
            "xtick.major.size": 2.5,
            "ytick.major.size": 2.5,
            "xtick.direction": "out",
            "ytick.direction": "out",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "savefig.dpi": DPI,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.02,
        }
    )


def style_axis(ax, *, show_xlabel: bool, show_ylabel: bool, show_xticklabels: bool):
    ax.set_xlim(X_BEG, X_END)
    ax.set_ylim(Z_END - Z_OFFSET, Z_BEG - Z_OFFSET)  # depth down (axis ij)
    ax.set_aspect("auto")
    ax.set_xticks([500, 750, 1000, 1250, 1500])
    ax.set_yticks([0, 100, 200, 300, 400])
    ax.tick_params(which="both", top=False, right=False)
    for spine in ax.spines.values():
        spine.set_linewidth(0.6)

    if show_xlabel:
        ax.set_xlabel("Distance (km)", labelpad=6)
    else:
        ax.set_xlabel("")
    if not show_xticklabels:
        ax.set_xticklabels([])

    if show_ylabel:
        ax.set_ylabel("Depth (km)")
    else:
        ax.set_ylabel("")
        ax.set_yticklabels([])


def pack_panel_rows(axes: np.ndarray, hspace: float):
    """Re-stack panel rows so HSPACE really controls inter-row gap."""
    fig = axes[0, 0].figure
    fig.canvas.draw()

    n_rows = axes.shape[0]
    z_span = (Z_END - Z_OFFSET) - (Z_BEG - Z_OFFSET)
    x_span = X_END - X_BEG
    data_aspect = z_span / x_span

    pos00 = axes[0, 0].get_position()
    panel_w = pos00.width
    panel_h = panel_w * data_aspect
    gap = hspace * panel_h
    y_top = pos00.y1

    for i in range(n_rows):
        y1 = y_top - i * (panel_h + gap)
        y0 = y1 - panel_h
        for j in range(2):
            p = axes[i, j].get_position()
            axes[i, j].set_position([p.x0, y0, p.width, panel_h])


def panel_label(ax, label: str):
    ax.text(
        0.02,
        0.96,
        label,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=11,
        fontweight="bold",
        color="k",
        bbox=dict(boxstyle="square,pad=0.15", facecolor="white", edgecolor="none", alpha=0.85),
    )


def time_label(ax, time_yr: float):
    t_myr = time_yr / 1.0e6
    ax.text(
        0.98,
        0.96,
        f"{t_myr:.2f} Myr",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=9,
        color="k",
        bbox=dict(boxstyle="square,pad=0.15", facecolor="white", edgecolor="none", alpha=0.85),
    )

def model_depth_km(p_gpa: float) -> float:
    """Depth below the surface of pressure p_gpa in the models: depthp() in markvis.c
    uses P = 3300 kg/m^3 * 9.80665 m/s^2 * depth (4.5 GPa = 139 km, 10 GPa = 309 km)."""
    return p_gpa * 1e9 / (3300.0 * 9.80665) / 1e3


def add_redox_front(ax, depth_km: float, label: str):
    """Black dashed redox-front marker on the initial snapshots (panels a and e)."""
    ax.axhline(
        depth_km,
        color="k",
        linestyle=(0, (5, 2.5)),
        linewidth=0.9,
        zorder=4,
    )
    ax.annotate(
        label,
        xy=(0.5, depth_km),
        xycoords=ax.get_yaxis_transform(),
        xytext=(0, 2),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=8,
        color="k",
        zorder=5,
        annotation_clip=False,
        bbox=dict(boxstyle="square,pad=0.12", facecolor="white", edgecolor="none", alpha=0.9),
    )


def add_material_legend(leg_ax, colors: np.ndarray):
    """Draw composition legend in a single row below the panels."""
    n = len(MATERIAL_LEGEND)
    label_gap = LEGEND_LABEL_GAP
    y_top = 0.88

    leg_ax.set_xlim(0, 1)
    leg_ax.set_ylim(0, 1)
    leg_ax.axis("off")

    bbox = leg_ax.get_window_extent().transformed(leg_ax.figure.dpi_scale_trans.inverted())
    ax_w_pt = bbox.width * 72.0
    ax_h_pt = bbox.height * 72.0
    sw_w = LEGEND_SWATCH_W_PT / max(ax_w_pt, 1.0)
    sw_h = LEGEND_SWATCH_H_PT / max(ax_h_pt, 1.0)

    centres = np.linspace(0.5 * sw_w, 1.0 - 0.5 * sw_w, n)

    for k, (idx, name) in enumerate(MATERIAL_LEGEND):
        cx = float(centres[k])
        y0 = y_top - sw_h
        x0 = cx - 0.5 * sw_w
        face = colors[idx]
        edge = "0.35" if float(np.mean(face)) > 0.92 else "0.2"
        leg_ax.add_patch(
            Rectangle(
                (x0, y0),
                sw_w,
                sw_h,
                facecolor=face,
                edgecolor=edge,
                linewidth=0.55,
                transform=leg_ax.transAxes,
                clip_on=False,
            )
        )
        label = name.replace(" ", "\n", 1) if len(name) > 12 else name
        leg_ax.text(
            cx,
            y0 - label_gap,
            label,
            transform=leg_ax.transAxes,
            ha="center",
            va="top",
            fontsize=8,
            color="k",
            linespacing=1.05,
        )


def plot_panel(ax, path: Path, cmap, norm, *, label: str, show_xlabel: bool, show_ylabel: bool):
    t, grid = decode_composition(path)
    grid, x, z = zoom_composition(grid)
    ax.pcolormesh(
        x,
        z,
        grid,
        cmap=cmap,
        norm=norm,
        shading="nearest",
        rasterized=True,
    )
    style_axis(ax, show_xlabel=show_xlabel, show_ylabel=show_ylabel, show_xticklabels=show_xlabel)
    panel_label(ax, label)
    time_label(ax, t)


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
def main():
    apply_nature_style()
    cmap_c, norm_c, colors = material_cmap()

    if len(STEPS_REDUCED) != len(STEPS_OXIDIZED):
        raise ValueError("STEPS_REDUCED and STEPS_OXIDIZED must have the same length")
    n_rows = len(STEPS_REDUCED)

    left, right, top = 0.08, 0.98, 0.965
    panel_bottom = 0.18
    fig_h = figure_height_in(n_rows, hspace=HSPACE, bottom=panel_bottom, top=top)
    fig_h += 0.95

    fig = plt.figure(figsize=(FIG_W_IN, fig_h))
    outer = fig.add_gridspec(
        2,
        1,
        height_ratios=[1.0, 0.12],
        hspace=0.08,
        left=left,
        right=right,
        top=top,
        bottom=0.03,
    )
    gs = outer[0].subgridspec(n_rows, 2, wspace=0.12, hspace=HSPACE)
    axes = np.empty((n_rows, 2), dtype=object)
    for i in range(n_rows):
        axes[i, 0] = fig.add_subplot(gs[i, 0])
        axes[i, 1] = fig.add_subplot(gs[i, 1])
    leg_ax = fig.add_subplot(outer[1])

    # Column-major panel labels: left a–d, right e–h
    labels_left = "abcd"
    labels_right = "efgh"

    for i, (step_r, step_o) in enumerate(zip(STEPS_REDUCED, STEPS_OXIDIZED)):
        last = i == n_rows - 1
        plot_panel(
            axes[i, 0],
            REDUCED_DIR / f"gouc{step_r}.txt",
            cmap_c,
            norm_c,
            label=labels_left[i],
            show_xlabel=last,
            show_ylabel=True,
        )
        plot_panel(
            axes[i, 1],
            OXIDIZED_DIR / f"gouc{step_o}.txt",
            cmap_c,
            norm_c,
            label=labels_right[i],
            show_xlabel=last,
            show_ylabel=False,
        )
        if i == 0:
            axes[i, 0].set_title("Reduced Mantle", pad=4)
            axes[i, 1].set_title("Oxidized Mantle", pad=4)
            # RF = 4.5 GPa (reduced) and 10 GPa (oxidized), converted as in the models
            add_redox_front(axes[i, 0], model_depth_km(4.5), "Redox front at 4.5 GPa")
            add_redox_front(axes[i, 1], model_depth_km(10.0), "Redox front at 10 GPa")

    pack_panel_rows(axes, HSPACE)

    pos_l = axes[-1, 0].get_position()
    pos_r = axes[-1, 1].get_position()
    leg_h = 0.065
    leg_gap = 0.055
    leg_y0 = max(0.015, pos_l.y0 - leg_gap - leg_h)
    leg_ax.set_position([pos_l.x0, leg_y0, pos_r.x1 - pos_l.x0, leg_h])
    add_material_legend(leg_ax, colors)

    fig.savefig(OUT_PNG, dpi=DPI)
    print(f"Saved: {OUT_PNG}")
    plt.close(fig)


if __name__ == "__main__":
    main()
