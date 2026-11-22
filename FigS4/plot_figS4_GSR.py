"""
Nature-style Fig. S4: Material Field | Temperature (+ velocity).

Reads gouc*.txt (material, RLE), gout*.txt (T), gouu*.txt (velocity)
from FigS4_ThermalPlume_Equal3.25rho/, using the eclogite colour and zoom range from
vis_cto3.m. The first timestep (step 2) omits the velocity field.
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
DATA = Path(os.environ.get("GSR_DATA_OVERRIDE", BASE / "FigS4_ThermalPlume_Equal3.25rho_Moho55km_GSR"))
STEPS = [2, 70, 150]

# Model / zoom (km) — same as vis_cto3.m
X_SIZE, Z_SIZE = 1000.0, 420.0
X_BEG, X_END = 200.0, 800.0
Z_BEG, Z_END = 0.0, 420.0
Z_OFFSET = 10.0  # MATLAB: z_vec = z_vec - 10

T_VMIN, T_VMAX = 0.0, 1800.0  # °C

# Velocity overlay (vis_cto3.m)
V_SCALE = 3.0 * 10**11
V_STEP_X = 20
V_STEP_Z = 30

# Nature double-column figure (~183 mm wide)
FIG_W_IN = 183 / 25.4
DPI = 600
HSPACE = 0.05  # row gap as a fraction of panel height

# Horizontal layout (figure fractions). Column order:
#   col0 Material (no colourbar) | col1 Temperature (+cbar)
N_COLS = 2
LEFT = 0.06
RIGHT_EDGE = 0.010
GAP_PLAIN = 0.045   # gap between Material and Temperature
CBAR_PAD = 0.012    # panel → its colourbar
CBAR_W = 0.013      # colourbar width
CBAR_LABEL = 0.030  # colourbar → figure edge (vertical tick labels)
DATA_ASPECT = (Z_END - Z_BEG) / (X_END - X_BEG)

# Vertical layout (inches)
TOP_IN = 0.30       # margin above first row (fits titles)
XLABEL_IN = 0.40    # room below bottom row for x ticks + "Distance (km)"
LEGEND_GAP_IN = 0.04
LEGEND_IN = 0.60
BOTTOM_IN = 0.12

# Legend swatch size (pt)
LEGEND_SWATCH_W_PT = 18
LEGEND_SWATCH_H_PT = 12
LEGEND_LABEL_GAP = 0.06

# Material legend (index → name)
MATERIAL_LEGEND = [
    (0, "Air"),
    (5, "Upper Crust"),
    (6, "Lower Crust"),
    (8, "Mantle Lithosphere"),
    (10, "Asthenosphere"),
]

OUT_PNG = Path(os.environ.get("GSR_OUTPUT_OVERRIDE", BASE / "FigS4_material_T_GSR.png"))


def panel_width_frac() -> float:
    """Panel width (figure fraction) leaving room for the Temperature colourbar."""
    gap_cbar = CBAR_PAD + CBAR_W + CBAR_LABEL
    return (1.0 - LEFT - RIGHT_EDGE - GAP_PLAIN - gap_cbar) / N_COLS


def column_x0() -> list[float]:
    """Left edge (figure fraction) of each of the two columns."""
    pw = panel_width_frac()
    return [
        LEFT,
        LEFT + pw + GAP_PLAIN,
    ]


def figure_height_in(n_rows: int) -> float:
    """Total figure height (inches) for equal-aspect panels + labels + legend."""
    panel_h_in = panel_width_frac() * FIG_W_IN * DATA_ASPECT
    panels_in = n_rows * panel_h_in + (n_rows - 1) * HSPACE * panel_h_in
    return TOP_IN + panels_in + XLABEL_IN + LEGEND_GAP_IN + LEGEND_IN + BOTTOM_IN


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


def _zoom_indices(coor_x: np.ndarray, coor_z: np.ndarray) -> tuple[int, int, int, int]:
    """Find zoom window indices from coordinate vectors (km), matching MATLAB."""
    xx1, xx2 = 0, len(coor_x) - 1
    zz1, zz2 = 0, len(coor_z) - 1
    for j in range(len(coor_x) - 1):
        if coor_x[j] <= X_BEG < coor_x[j + 1]:
            xx1 = j
        elif coor_x[j] < X_END <= coor_x[j + 1]:
            xx2 = j
    for j in range(len(coor_z) - 1):
        if coor_z[j] <= Z_BEG < coor_z[j + 1]:
            zz1 = j
        elif coor_z[j] < Z_END <= coor_z[j + 1]:
            zz2 = j
    return xx1, xx2, zz1, zz2


def load_node_field(path: Path, *, subtract_kelvin: bool = False) -> tuple[float, np.ndarray, np.ndarray, np.ndarray]:
    """Load node-centred field (gouz / gout) → (time_yr, grid, x_km, z_km)."""
    data = load_numbers(path)
    time = float(data[0])
    num_x = int(data[1])
    num_z = int(data[2])
    i0 = 3
    coor_x = data[i0 : i0 + num_x] / 1000.0
    coor_z = data[i0 + num_x : i0 + num_x + num_z] / 1000.0
    vec = data[i0 + num_x + num_z :]
    if subtract_kelvin:
        vec = vec - 273.0
    grid = vec.reshape((num_z, num_x), order="F")

    xx1, xx2, zz1, zz2 = _zoom_indices(coor_x, coor_z)
    x = coor_x[xx1 : xx2 + 1]
    z = coor_z[zz1 : zz2 + 1] - Z_OFFSET
    field = grid[zz1 : zz2 + 1, xx1 : xx2 + 1]
    return time, field, x, z


def load_temperature(path: Path) -> tuple[float, np.ndarray, np.ndarray, np.ndarray]:
    return load_node_field(path, subtract_kelvin=True)


def load_velocity(path: Path) -> tuple[float, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Load gouu*.txt → (time_yr, ux, uz, x_km, z_km) within zoom, subsampled."""
    data = load_numbers(path)
    time = float(data[0])
    num_x = int(data[1])
    num_z = int(data[2])
    i0 = 3
    coor_x = data[i0 : i0 + num_x] / 1000.0
    coor_z = data[i0 + num_x : i0 + num_x + num_z] / 1000.0
    n_cell = num_x * num_z
    i1 = i0 + num_x + num_z
    ux = data[i1 : i1 + n_cell].reshape((num_z, num_x), order="F")
    uz = data[i1 + n_cell :].reshape((num_z, num_x), order="F")

    xx1, xx2, zz1, zz2 = _zoom_indices(coor_x, coor_z)
    x = coor_x[xx1 : xx2 + 1][::V_STEP_X]
    z = coor_z[zz1 : zz2 + 1][::V_STEP_Z] - Z_OFFSET
    ux_z = ux[zz1 : zz2 + 1 : V_STEP_Z, xx1 : xx2 + 1 : V_STEP_X]
    uz_z = uz[zz1 : zz2 + 1 : V_STEP_Z, xx1 : xx2 + 1 : V_STEP_X]
    return time, ux_z, uz_z, x, z


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
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
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
    ax.set_ylim(Z_END - Z_OFFSET, Z_BEG - Z_OFFSET)
    ax.set_aspect("auto")
    ax.set_xticks([200, 400, 600, 800])
    ax.set_yticks([0, 100, 200, 300, 400])
    ax.tick_params(which="both", top=False, right=False)
    for spine in ax.spines.values():
        spine.set_linewidth(0.6)

    if show_xlabel:
        ax.set_xlabel("Distance (km)", labelpad=3)
    else:
        ax.set_xlabel("")
    if not show_xticklabels:
        ax.set_xticklabels([])

    if show_ylabel:
        ax.set_ylabel("Depth (km)")
    else:
        ax.set_ylabel("")
        ax.set_yticklabels([])


def pack_panels(axes: np.ndarray) -> tuple[float, float]:
    """Place every panel with explicit x/y so nothing overlaps.

    Returns (panel_h_frac, row_gap_frac) for downstream colourbar/legend layout.
    """
    fig = axes[0, 0].figure
    fig.canvas.draw()
    fig_h_in = fig.get_size_inches()[1]

    n_rows = axes.shape[0]
    x0s = column_x0()
    pw = panel_width_frac()
    panel_h = (pw * FIG_W_IN * DATA_ASPECT) / fig_h_in
    gap = HSPACE * panel_h
    y_top = 1.0 - TOP_IN / fig_h_in

    for i in range(n_rows):
        y1 = y_top - i * (panel_h + gap)
        y0 = y1 - panel_h
        for j in range(N_COLS):
            axes[i, j].set_position([x0s[j], y0, pw, panel_h])
    return panel_h, gap


def panel_label(ax, label: str):
    ax.text(
        0.02,
        0.96,
        label,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=10,
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
        fontsize=8,
        color="k",
        bbox=dict(boxstyle="square,pad=0.15", facecolor="white", edgecolor="none", alpha=0.85),
    )


def add_material_legend(leg_ax, colors: np.ndarray):
    """Draw composition legend in a single row below the panels."""
    n = len(MATERIAL_LEGEND)
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
        label = name
        leg_ax.text(
            cx,
            y0 - LEGEND_LABEL_GAP,
            label,
            transform=leg_ax.transAxes,
            ha="center",
            va="top",
            fontsize=7.5,
            color="k",
            linespacing=1.05,
        )


def temperature_cmap():
    """Prefer Scientific Colour Maps roma (flipped); else RdYlBu_r."""
    try:
        from cmcrameri import cm as scm

        return scm.roma_r
    except ImportError:
        return "RdYlBu_r"


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
def main():
    apply_nature_style()
    cmap_c, norm_c, colors = material_cmap()
    cmap_t = temperature_cmap()

    n_rows = len(STEPS)
    fig_h = figure_height_in(n_rows)

    fig = plt.figure(figsize=(FIG_W_IN, fig_h))
    axes = np.empty((n_rows, N_COLS), dtype=object)
    for i in range(n_rows):
        for j in range(N_COLS):
            axes[i, j] = fig.add_axes([0.1, 0.1, 0.1, 0.1])  # placeholder; positioned later
    leg_ax = fig.add_axes([0.1, 0.02, 0.8, 0.06])

    t_mappable = None
    labels = "abcdefghijkl"

    for i, step in enumerate(STEPS):
        last = i == n_rows - 1
        # Column order: Material | Temperature (+velocity)
        ax_c, ax_t = axes[i, 0], axes[i, 1]

        # --- Material ---
        t_c, grid_c = decode_composition(DATA / f"gouc{step}.txt")
        grid_c, x_c, z_c = zoom_composition(grid_c)
        ax_c.pcolormesh(
            x_c, z_c, grid_c, cmap=cmap_c, norm=norm_c, shading="nearest", rasterized=True
        )
        style_axis(ax_c, show_xlabel=last, show_ylabel=True, show_xticklabels=last)
        panel_label(ax_c, labels[i * N_COLS + 0])
        time_label(ax_c, t_c)
        if i == 0:
            ax_c.set_title("Material Field", pad=4)

        # --- Temperature + velocity ---
        t_t, grid_t, x_t, z_t = load_temperature(DATA / f"gout{step}.txt")
        t_mappable = ax_t.pcolormesh(
            x_t,
            z_t,
            grid_t,
            cmap=cmap_t,
            vmin=T_VMIN,
            vmax=T_VMAX,
            shading="auto",
            rasterized=True,
        )
        if step != 2:  # the first timestep (step 2) omits the velocity field
            _, ux, uz, x_u, z_u = load_velocity(DATA / f"gouu{step}.txt")
            XU, ZU = np.meshgrid(x_u, z_u)
            # Per-panel scale: cap the longest arrow at a fixed fraction of the panel
            speed = np.hypot(ux, uz)
            vmax = float(speed.max())
            target_len = 0.10 * (X_END - X_BEG)  # km, longest arrow
            q_scale = (vmax / target_len) if vmax > 0 else 1.0
            ax_t.quiver(
                XU,
                ZU,
                ux,
                uz,
                color="k",
                angles="xy",
                scale_units="xy",
                scale=q_scale,
                width=0.004,
                headwidth=3.5,
                headlength=4.0,
                headaxislength=3.5,
                linewidth=0.3,
                zorder=5,
            )
        style_axis(ax_t, show_xlabel=last, show_ylabel=False, show_xticklabels=last)
        panel_label(ax_t, labels[i * N_COLS + 1])
        time_label(ax_t, t_t)
        if i == 0:
            ax_t.set_title(r"Temperature ($^\circ$C)", pad=4)

    pack_panels(axes)

    # Temperature colourbar to the right of col1
    pos_t0 = axes[0, 1].get_position()
    pos_t1 = axes[-1, 1].get_position()
    cax_t = fig.add_axes([pos_t0.x1 + CBAR_PAD, pos_t1.y0, CBAR_W, pos_t0.y1 - pos_t1.y0])
    cbar_t = fig.colorbar(t_mappable, cax=cax_t)
    cbar_t.set_ticks([0, 450, 900, 1350, 1800])
    cbar_t.ax.tick_params(labelsize=8, width=0.6, length=2.5)
    cbar_t.outline.set_linewidth(0.6)
    for lbl in cbar_t.ax.get_yticklabels():
        lbl.set_rotation(270)
        lbl.set_va("center")

    # Material legend under both columns, below the x-axis labels
    pos_l = axes[-1, 0].get_position()
    pos_r = axes[-1, 1].get_position()
    leg_h = LEGEND_IN / fig_h
    leg_y0 = max(0.01, pos_t1.y0 - (XLABEL_IN + LEGEND_GAP_IN) / fig_h - leg_h)
    leg_ax.set_position([pos_l.x0, leg_y0, pos_r.x1 - pos_l.x0, leg_h])
    add_material_legend(leg_ax, colors)

    fig.savefig(OUT_PNG, dpi=DPI)
    print(f"Saved: {OUT_PNG}")
    plt.close(fig)


if __name__ == "__main__":
    main()
