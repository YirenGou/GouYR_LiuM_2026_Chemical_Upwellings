"""
Nature-style Fig. 4: composition (left) and water content (right).

Reads gouc*.txt (material field, RLE-compressed) and gouz*.txt (H as ppm H/Si)
from the model subdirectory, converts olivine water to wt ppm H2O for plotting,
matching the zoom / colour maps used in vis_cto3.m and vis_node3_H.m.
"""

import os
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import BoundaryNorm, LinearSegmentedColormap, ListedColormap
from matplotlib.patches import Rectangle

# ---------------------------------------------------------------------------
# Paths & cases
# ---------------------------------------------------------------------------
BASE = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get(
    "GSR_DATA_OVERRIDE",
    BASE / "Fig4_C-H_MTZ0.2PhaseChange_0.1MPa0.01WeakML_MinMiu1E19rho3.28_CL100km_8000ppm_CorrectT_GSR",
))
STEPS = [1, 70, 130, 200]

# Model / zoom (km) — same as MATLAB scripts
X_SIZE, Z_SIZE = 2000.0, 670.0
X_BEG, X_END = 500.0, 1500.0
Z_BEG, Z_END = 0.0, 450.0
Z_OFFSET = 10.0  # MATLAB: z_vec = z_vec - 10

# Olivine (Fo90) H/Si (atomic ppm) → H2O (wt ppm):
#   wt ppm = (H/Si ppm) * M_H2O / (2 * M_ol) , M_ol ≈ 146.94 g/mol
# Equivalent to H2O_wtppm ≈ (H/Si)_ppm / 16.3
M_OLIVINE_FO90 = 146.94
M_H2O = 18.015
HSI_TO_WT_PPM = M_H2O / (2.0 * M_OLIVINE_FO90)

H_VMIN, H_VMAX = 0.0, 80.0  # wt ppm H2O

# Sequential H2O colour map: white (0 ppm) → deep blue (80 ppm)
H_CMAP_STOPS = ["#FFFFFF", "#DEEBF7", "#9ECAE1", "#3182BD", "#08519C"]


def h2o_cmap():
    return LinearSegmentedColormap.from_list("h2o_blue", H_CMAP_STOPS, N=256)


# Nature double-column figure (~183 mm wide)
FIG_W_IN = 183 / 25.4
DPI = 600

# Panel row gap as a fraction of panel height (0 = touching).
# NOTE: visual gaps were mostly from equal-aspect letterboxing, not HSPACE;
# panels are now packed explicitly so this value actually controls spacing.
HSPACE = 0.05

# Legend swatch size (pt)
LEGEND_SWATCH_W_PT = 18
LEGEND_SWATCH_H_PT = 12
# Gap between colour swatch and its label (axes fraction). Larger → farther.
LEGEND_LABEL_GAP = 0.06
# Gap between the two legend rows (axes fraction).
LEGEND_ROW_GAP = 0.08

# Material legend (index → name), colours from composition colormap
MATERIAL_LEGEND = [
    (0, "Air"),
    (5, "Upper Crust"),
    (6, "Lower Crust"),
    (8, "Mantle Lithosphere"),
    (10, "Asthenosphere"),
    (11, "Mantle Transition Zone"),
    (14, "Carbonatite"),
    (15, "Buoyant Mantle"),
    (16, "Molten Mantle"),
]

OUT_PNG = Path(os.environ.get("GSR_OUTPUT_OVERRIDE", BASE / "Fig4_composition_H_GSR.png"))
#OUT_PDF = BASE / "Fig4_composition_H_GSR.pdf"


def figure_height_in(n_rows: int, *, hspace: float, bottom: float, top: float) -> float:
    """Height so equal-aspect panels pack tightly with the given hspace."""
    left, right = 0.08, 0.90
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


def load_hydrogen(path: Path) -> tuple[float, np.ndarray, np.ndarray, np.ndarray]:
    """Load gouz*.txt → (time_yr, H2O wt ppm[nz,nx], x_km, z_km) within zoom.

    Model files store olivine water as atomic ppm H/Si; convert to wt ppm H2O.
    """
    data = load_numbers(path)
    time = float(data[0])
    num_x = int(data[1])
    num_z = int(data[2])
    i0 = 3
    coor_x = data[i0 : i0 + num_x] / 1000.0
    coor_z = data[i0 + num_x : i0 + num_x + num_z] / 1000.0
    vec = data[i0 + num_x + num_z :]
    grid = vec.reshape((num_z, num_x), order="F")

    xx1, xx2 = 0, num_x - 1
    zz1, zz2 = 0, num_z - 1
    for j in range(num_x - 1):
        if coor_x[j] <= X_BEG < coor_x[j + 1]:
            xx1 = j
        elif coor_x[j] < X_END <= coor_x[j + 1]:
            xx2 = j
    for j in range(num_z - 1):
        if coor_z[j] <= Z_BEG < coor_z[j + 1]:
            zz1 = j
        elif coor_z[j] < Z_END <= coor_z[j + 1]:
            zz2 = j

    x = coor_x[xx1 : xx2 + 1]
    z = coor_z[zz1 : zz2 + 1] - Z_OFFSET
    h_si = grid[zz1 : zz2 + 1, xx1 : xx2 + 1]
    h = h_si * HSI_TO_WT_PPM  # atomic ppm H/Si → wt ppm H2O (olivine Fo90)
    return time, h, x, z


# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------
def apply_nature_style():
    # Base sizes are prior values + 2 pt
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
    # Fill the axes box; equal km aspect is enforced by pack_panel_rows().
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
    """Re-stack panel rows so HSPACE really controls inter-row gap.

    ``set_aspect('equal')`` letterboxes inside each GridSpec cell, which looks
    like row gaps even when hspace=0. Here we set each axes box to the data
    aspect and stack rows from the top with gap = hspace * panel_height.
    """
    fig = axes[0, 0].figure
    fig.canvas.draw()

    n_rows = axes.shape[0]
    z_span = (Z_END - Z_OFFSET) - (Z_BEG - Z_OFFSET)
    x_span = X_END - X_BEG
    data_aspect = z_span / x_span  # height / width in data units

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


def add_depth_marker(ax, depth_km: float, label: str):
    """Black dashed depth marker, same style as Fig. 3 redox fronts."""
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
    """Draw composition legend in a single row; swatches span Depth → colorbar."""
    n = len(MATERIAL_LEGEND)
    ncols = n  # one row
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

    # First/last swatches flush to legend-axes edges (Depth ylabel → colorbar).
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
        # Wrap long names onto two lines so 8 items fit in one row
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


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
def main():
    apply_nature_style()
    cmap_c, norm_c, colors = material_cmap()

    n_rows = len(STEPS)
    left, right, top = 0.08, 0.90, 0.965
    # Panel-block sizing; extra figure height reserved for x-labels + legend
    panel_bottom = 0.22
    fig_h = figure_height_in(n_rows, hspace=HSPACE, bottom=panel_bottom, top=top)
    fig_h += 1.05

    fig = plt.figure(figsize=(FIG_W_IN, fig_h))
    # Nested gridspec: plot block + legend row
    # hspace = gap between "Distance (km)" and the legend (larger → farther)
    # height_ratios[1] = legend block height (only needs to fit 2 packed rows)
    outer = fig.add_gridspec(
        2,
        1,
        height_ratios=[1.0, 0.14],
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

    h_mappable = None
    labels_left = "aceg"
    labels_right = "bdfh"

    for i, step in enumerate(STEPS):
        ax_c = axes[i, 0]
        ax_h = axes[i, 1]
        last = i == n_rows - 1

        c_path = DATA_DIR / f"gouc{step}.txt"
        t_c, grid_c = decode_composition(c_path)
        grid_c, x_c, z_c = zoom_composition(grid_c)
        ax_c.pcolormesh(
            x_c,
            z_c,
            grid_c,
            cmap=cmap_c,
            norm=norm_c,
            shading="nearest",
            rasterized=True,
        )
        style_axis(ax_c, show_xlabel=last, show_ylabel=True, show_xticklabels=last)
        panel_label(ax_c, labels_left[i])
        time_label(ax_c, t_c)
        if i == 0:
            ax_c.set_title("Material Field", pad=4)
            # This run: RF = 10 GPa (redox melting), CL = 3 GPa (carbonate ledge).
            # Depths converted as in the models (3 GPa = 93 km, 10 GPa = 309 km).
            add_depth_marker(ax_c, model_depth_km(3.0), "Carbonate ledge at 3 GPa")
            add_depth_marker(ax_c, model_depth_km(10.0), "Redox front at 10 GPa")

        z_path = DATA_DIR / f"gouz{step}.txt"
        t_h, grid_h, x_h, z_h = load_hydrogen(z_path)
        h_mappable = ax_h.pcolormesh(
            x_h,
            z_h,
            grid_h,
            cmap=h2o_cmap(),
            vmin=H_VMIN,
            vmax=H_VMAX,
            shading="auto",
            rasterized=True,
        )
        style_axis(ax_h, show_xlabel=last, show_ylabel=False, show_xticklabels=last)
        panel_label(ax_h, labels_right[i])
        time_label(ax_h, t_h)
        if i == 0:
            ax_h.set_title(r"Water content (wt ppm H$_2$O)", pad=4)

    # Pack panels so HSPACE controls real gaps; then park legend under them
    pack_panel_rows(axes, HSPACE)
    pos0 = axes[0, 1].get_position()
    pos1 = axes[-1, 1].get_position()
    cax = fig.add_axes([0.92, pos1.y0, 0.018, pos0.y1 - pos1.y0])
    cbar = fig.colorbar(h_mappable, cax=cax)
    #cbar.set_label(r"H$_2$O (wt ppm)", fontsize=10)
    cbar.set_ticks([0, 20, 40, 60, 80])
    cbar.ax.tick_params(labelsize=9, width=0.6, length=2.5)
    cbar.outline.set_linewidth(0.6)

    # Place legend below panels; left = Depth ylabel, right = water colorbar (incl. ticks)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    inv = fig.transFigure.inverted()
    depth_bbox = axes[-1, 0].yaxis.label.get_window_extent(renderer=renderer).transformed(inv)
    cbar_bbox = cax.get_tightbbox(renderer).transformed(inv)
    leg_x0 = depth_bbox.x0
    leg_x1 = cbar_bbox.x1
    leg_h = 0.065
    leg_gap = 0.055  # space for "Distance (km)" labels
    leg_y0 = max(0.015, pos1.y0 - leg_gap - leg_h)
    leg_ax.set_position([leg_x0, leg_y0, leg_x1 - leg_x0, leg_h])

    add_material_legend(leg_ax, colors)

    fig.savefig(OUT_PNG, dpi=DPI)
#    fig.savefig(OUT_PDF)
    print(f"Saved: {OUT_PNG}")
#    print(f"Saved: {OUT_PDF}")
    plt.close(fig)


if __name__ == "__main__":
    main()
