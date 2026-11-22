# -*- coding: utf-8 -*-
"""
Fig. 1 v4 composite: (a) topography, (b) lithospheric thickness, (c) MTZ dVp,
(d) FWEA23 dVp section along 40N, (e) conceptual sketch.

Panels a–c are the v3 panels; c also carries the trace of the d profile.
The v3 schematic is gone and its cell holds two stacked panels:
  d: FWEA23 (Liu et al., 2024, EPSL) dVp along 40N, 110–145E, 100–800 km,
     same stepped colour scale as c. White circles are relocated earthquakes
     (TX2019slab catalogue) within 1 deg of the profile.
  e: geometric sketch on the same 110–145E line (not to scale): volatiles
     released above the stagnant slab rise as compositional upwellings, thin
     the lithosphere and feed intraplate volcanoes.

d and e are drawn after the 2 x 2 subplot closes, at positions computed
from the subplot size and margins (GMT forbids origin shifts inside a panel).
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pygmt

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
FIG1 = Path(__file__).resolve().parent
FWEA_DIR = FIG1 / "MTZ_StagnantSlabs" / "FWEA23_ChujieLiu"
MTZ_DIR = FIG1 / "MTZ_StagnantSlabs"
LITH_DIR = FIG1 / "Lithospheric thickness"
CACHE = FIG1 / "_fig1_cache"

SAVANI_GRD = LITH_DIR / "savani.l.grd"
GAP_P4_FILE = MTZ_DIR / "GAP_P4" / "GAP_P4" / "GAP_P4"
FWEA_NC = FWEA_DIR / "FWEA23.r0.0.nc"
QUAKE_FILE = MTZ_DIR / "TX2019slab" / "TX2019slab" / "relocated_eq_list"

# ---------------------------------------------------------------------------
# Shared map / type style (edit here to retune the whole figure)
# ---------------------------------------------------------------------------
REGION = [100, 135, 20, 50]
PROJ = "M?"  # fill subplot panel width
FONT_MAP = "8p,Helvetica"
FONT_CBAR = "12p,Helvetica"
GMT_DATA_SERVER = "https://mirrors.ustc.edu.cn/gmtdata"
TOPO_GRID = "@earth_relief_01m"
# geo is hinged at sea level; this window reaches Gongga Shan and the Ryukyu trench.
TOPO_SERIES = [-8000, 8000]

# Subplot size and margins (cm). d and e are placed from the same numbers.
FIG_SIZE = (17.2, 19.6)
FIG_MARGINS = (0.35, 1.15)

# Atlas city marks from the cities variant of Fig. 1. Capitals carry a centred dot.
CITY_HALO = ("c0.20c", "white")
CITY_RING = ("c0.135c", "white", "0.6p,black")
CITY_CAPITAL_DOT = ("c0.055c", "black")
CITIES = [
    # lon, lat, name, capital?, justify, dx_cm, dy_cm
    (116.41, 39.90, "Beijing", True, "MR", -0.16, 0.0),
    (121.47, 31.23, "Shanghai", False, "ML", 0.16, 0.0),
    (113.26, 23.13, "Guangzhou", False, "MR", -0.16, 0.0),
    (126.98, 37.57, "Seoul", True, "ML", 0.16, 0.0),
    (106.92, 47.92, "Ulaanbaatar", True, "ML", 0.16, 0.0),
    (126.53, 45.80, "Harbin", False, "ML", 0.16, 0.0),
    (104.07, 30.67, "Chengdu", False, "ML", 0.16, 0.0),
]
FONT_CITY = "6.5p,Helvetica,black"
HALO_RADIUS_CM = 0.022
HALO_OFFSETS = [
    (1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0),
    (0.7, 0.7), (0.7, -0.7), (-0.7, 0.7), (-0.7, -0.7),
]

# Stepped CPTs: one solid colour per bin. The bin edge is the isoline.
LITH_CPT = (0, 250, 25)
# Panel (c) GAP_P4 extras from plot_mtz_models.py
GAP_DMIN, GAP_DMAX = 410.0, 660.0
GAP_CPT = (-1.5, 1.5, 0.25)
GAP_SPACING = "0.15d"
GAP_TENSION = 0.0
GAP_GAUSS_KM = 180.0

GAP_P4_LAYERS = [
    (29, 51), (51, 78), (78, 110), (110, 148), (148, 190),
    (190, 238), (238, 290), (290, 348), (348, 410), (410, 478),
    (478, 551), (551, 629), (629, 712), (712, 800), (800, 893),
    (893, 991), (991, 1095), (1095, 1203), (1203, 1317), (1317, 1435),
    (1435, 1559), (1559, 1688), (1688, 1821), (1821, 1960), (1960, 2104),
    (2104, 2253), (2253, 2407), (2407, 2566), (2566, 2891),
]

# Panel (d) FWEA23 section. alpha = dVp, beta = dVs (both stored as fractions).
SEC_VAR = "alpha"
SEC_LAT = 40.0
SEC_REGION = [110, 145, 100, 800]  # lon, lon, depth, depth
SEC_HEIGHT = 3.2  # cm
SEC_SPACING = "0.05/2"  # resample step: deg / km
QUAKE_BAND = 1.0  # deg of latitude either side of the profile
SHOW_QUAKES = True
SHOW_PROFILE = True  # trace of d on panel c
PROFILE_LABEL = "Cross section in d"
FONT_PROFILE = "7p,Helvetica,black"  # 8p runs into the Liaodong Bay coast

# Panel e box in the lower-right cell (cm, from the floor of c's cell).
# E_BOTTOM centres e between the foot of d's colourbar label and the foot of
# c's colourbar label (measured on the 400 dpi PNG: 0.30 cm gap each side).
E_HEIGHT = 5.0
E_BOTTOM = -1.22

# Panel (e) sketch. Positions are lon (deg E) and depth (km) on the d line.
E_DEPTH = (-85.0, 720.0)  # top of the sketch (air above the volcanoes), bottom
E_LAB_CRATON = 190.0
E_LAB_THIN = 80.0
E_CRATON_EDGE = (114.4, 116.8)  # lon where the keel base starts / stops rising
E_TRENCH = 143.6
E_SLAB_BEND = (131.3, 572.0)  # corner between the dipping and flat slab (top)
E_SLAB_TIP = 117.6
E_SLAB_THICK = 0.5  # cm
E_SLAB_RADII = (0.4, 0.6)  # cm, top surface at the trench and at the MTZ bend
E_STEM_HALF = 0.055  # cm
# lon, head-centre depth (None = ponded under the LAB), head semi-axes a, b (cm)
E_UPWELLINGS = [
    (119.8, 330.0, 0.17, 0.14),
    (122.7, None, 0.38, 0.16),
    (129.5, None, 0.38, 0.16),
]
E_BLOCK = (126.1, 190.0)  # detached lithosphere: lon, depth of centre
E_BLOCK_SIZE = (0.92, 0.40)  # cm
E_BLOCK_TILT = 14.0  # deg
# Volatile drops around each upwelling root: lon offset, height above slab (km), size (cm)
E_DROP_CLUSTER = [
    (-1.0, 22, 0.11), (1.0, 22, 0.11), (-0.62, 58, 0.09),
    (0.62, 58, 0.09), (-0.4, 92, 0.07), (0.4, 92, 0.07),
]
E_DROP_LOOSE = [(117.8, 30), (121.3, 44), (125.2, 26), (127.1, 42)]  # lon, height (km)
E_ARC = 140.5
E_COL = {
    "um": "#fbf1e4", "mtz": "#f4e2cc", "lm": "#ecd4bb",
    "lith": "#a9c19b", "lith_edge": "#6e8c62",
    "slab": "#3f6fb0", "slab_edge": "#264f8a",
    "vol": "#1f9fd6", "up": "#c4e7f4", "up_edge": "#2a9bcd",
    "melt": "#dc3b26", "melt_edge": "#9e2414", "arc": "#9a9a9a",
    "ink": "#222222", "soft": "#5a5a5a",
}
FONT_E = "6.5p,Helvetica"


def _config():
    return pygmt.config(
        GMT_DATA_SERVER=GMT_DATA_SERVER,
        FONT=FONT_MAP,
        FONT_ANNOT_PRIMARY=FONT_MAP,
        FONT_LABEL=FONT_MAP,
        FONT_TITLE=FONT_MAP,
        MAP_FRAME_TYPE="fancy",
        MAP_TITLE_OFFSET="0p",
    )


def _step_cpt(cmap: str, series: tuple[float, float, float], reverse: bool) -> None:
    """Discrete CPT. continuous is left off so neighbouring bins do not blend."""
    pygmt.makecpt(
        cmap=cmap,
        series=list(series),
        reverse=reverse,
        continuous=False,
        background=True,
    )


def _cbar(fig: pygmt.Figure, frame: list[str]) -> None:
    """Horizontal colourbar; tick numbers and title are 12p."""
    with pygmt.config(FONT_ANNOT_PRIMARY=FONT_CBAR, FONT_LABEL=FONT_CBAR):
        fig.colorbar(position="JBC+w80%/0.28c+h+o0/0.42c", frame=frame)


def _panel_tag(fig: pygmt.Figure, letter: str) -> None:
    fig.text(
        position="TL",
        text=letter,
        font="12p,Helvetica-Bold,black",
        offset="0.12c/-0.18c",
        no_clip=True,
    )


def _recolour(font: str, colour: str) -> str:
    parts = font.split(",")
    parts[-1] = colour
    return ",".join(parts)


def _label(fig, x, y, text, font, justify="CM", dx=0.0, dy=0.0):
    """White halo under the label so it stays readable on the hillshade."""
    white = _recolour(font, "white")
    r = HALO_RADIUS_CM
    for ux, uy in HALO_OFFSETS:
        fig.text(
            x=x, y=y, text=text, font=white, justify=justify,
            offset=f"{dx + ux * r:.4f}c/{dy + uy * r:.4f}c",
        )
    fig.text(
        x=x, y=y, text=text, font=font, justify=justify,
        offset=f"{dx:.4f}c/{dy:.4f}c",
    )


def plot_cities(fig: pygmt.Figure) -> None:
    """Atlas-style city circles; capitals carry a centred dot."""
    lons = [c[0] for c in CITIES]
    lats = [c[1] for c in CITIES]
    style, fill = CITY_HALO
    fig.plot(x=lons, y=lats, style=style, fill=fill)
    style, fill, pen = CITY_RING
    fig.plot(x=lons, y=lats, style=style, fill=fill, pen=pen)
    cap = [(c[0], c[1]) for c in CITIES if c[3]]
    if cap:
        style, fill = CITY_CAPITAL_DOT
        fig.plot(x=[c[0] for c in cap], y=[c[1] for c in cap], style=style, fill=fill)
    for lon, lat, name, _cap, justify, dx, dy in CITIES:
        _label(fig, lon, lat, name, FONT_CITY, justify=justify, dx=dx, dy=dy)


# ---------------------------------------------------------------------------
# Panel a — topography (earth relief)
# ---------------------------------------------------------------------------
def plot_panel_a(fig: pygmt.Figure, frame: str) -> None:
    topo = pygmt.grdcut(TOPO_GRID, region=REGION)
    topo_hi = pygmt.grdsample(
        grid=topo, spacing="01m", region=REGION, registration="gridline"
    )
    # geo fades to near-white at sea level, so the Yellow Sea / ECS shelf
    # (mostly 0 to -200 m) renders as a blank hole. Keep the geo stops and
    # pin the ocean side of 0 m to a light blue.
    CACHE.mkdir(parents=True, exist_ok=True)
    cpt = CACHE / "topo_geo.cpt"
    pygmt.makecpt(
        cmap="geo",
        series=[TOPO_SERIES[0], TOPO_SERIES[1]],
        background=True,
        output=str(cpt),
    )
    text = cpt.read_text(encoding="utf-8")
    old = "245/255/255"
    if old not in text:
        raise RuntimeError("geo CPT no longer ends the ocean ramp at 245/255/255")
    cpt.write_text(text.replace(old, "170/214/236", 1), encoding="utf-8")
    pygmt.makecpt(cmap=str(cpt))
    shade = pygmt.grdgradient(grid=topo_hi, azimuth=315, normalize="t0.8")
    fig.grdimage(
        grid=topo_hi,
        region=REGION,
        projection=PROJ,
        cmap=True,
        shading=shade,
    )
    fig.coast(
        region=REGION,
        projection=PROJ,
        shorelines="1/0.35p,#333333",
    )
    fig.basemap(region=REGION, projection=PROJ, frame=[frame, "af"])
    plot_cities(fig)
    _cbar(fig, ["a4000", "x+lElevation (m)"])
    _panel_tag(fig, "a")


# ---------------------------------------------------------------------------
# Panel b — SB16 SAVANI lithospheric thickness (from plot_lab_comparison.py)
# ---------------------------------------------------------------------------
def plot_panel_b(fig: pygmt.Figure, frame: str) -> None:
    _step_cpt("polar", LITH_CPT, reverse=True)
    grid_smooth = pygmt.grdsample(
        grid=str(SAVANI_GRD),
        region=REGION,
        spacing="0.05",
        registration="gridline",
    )
    fig.grdimage(
        grid=grid_smooth,
        region=REGION,
        projection=PROJ,
        cmap=True,
        interpolation="c",
        nan_transparent=True,
    )
    fig.coast(
        region=REGION,
        projection=PROJ,
        shorelines="1/0.35p,#333333",
        frame=[frame, "af"],
    )
    _cbar(fig, ["a50", "x+lLithosphere Thickness"])
    _panel_tag(fig, "b")


# ---------------------------------------------------------------------------
# Panel c — GAP_P4 410–660 km (from plot_mtz_models.py)
# ---------------------------------------------------------------------------
def wrap_lon(lon: np.ndarray) -> np.ndarray:
    lon = np.asarray(lon, dtype=float)
    return np.mod(lon + 180.0, 360.0) - 180.0


def load_gap_p4(dmin: float, dmax: float):
    """Fortran 10f8.3 file: 576 lon x 288 lat x 29 layers, percent dVp."""
    path = GAP_P4_FILE
    if not path.is_file():
        raise FileNotFoundError(path)
    nlon, nlat, nlay = 576, 288, 29
    nper = nlon * nlat
    vals = np.empty(nper * nlay, dtype=np.float64)
    idx = 0
    with open(path, "r") as f:
        for line in f:
            s = line.rstrip("\n").rstrip("\r")
            for i in range(0, len(s), 8):
                chunk = s[i : i + 8]
                if not chunk.strip():
                    continue
                vals[idx] = float(chunk)
                idx += 1
    if idx != vals.size:
        raise RuntimeError(f"GAP_P4 expected {vals.size} values, got {idx}")
    dlon = 180.0 / nlat
    lon = dlon * (np.arange(nlon) + 0.5)
    lat = 90.0 - dlon * (np.arange(nlat) + 0.5)
    cube = vals.reshape(nlay, nlat, nlon)
    acc = None
    weight = 0.0
    for k, (z0, z1) in enumerate(GAP_P4_LAYERS):
        overlap = max(0.0, min(dmax, z1) - max(dmin, z0))
        if overlap <= 0:
            continue
        if acc is None:
            acc = np.zeros_like(cube[k], dtype=float)
        acc += cube[k] * overlap
        weight += overlap
    if acc is None or weight <= 0:
        raise RuntimeError("no GAP_P4 layers in window")
    acc /= weight
    lon2d, lat2d = np.meshgrid(lon, lat)
    return lon2d.ravel(), lat2d.ravel(), acc.ravel()


def gap_p4_grid() -> Path:
    """Build (or reuse) the smoothed GAP_P4 410–660 km grid."""
    CACHE.mkdir(parents=True, exist_ok=True)
    out = CACHE / "gap_p4_410_660.nc"
    if out.is_file():
        return out
    lon, lat, field = load_gap_p4(GAP_DMIN, GAP_DMAX)
    lon = wrap_lon(lon)
    w, e, s, n = REGION
    buf = [w - 15, e + 15, s - 15, n + 15]
    mask = (
        (lon >= buf[0])
        & (lon <= buf[1])
        & (lat >= buf[2])
        & (lat <= buf[3])
        & np.isfinite(field)
    )
    xyz = np.column_stack((lon[mask], lat[mask], field[mask]))
    grid = pygmt.surface(
        data=xyz,
        region=[float(xyz[:, 0].min()), float(xyz[:, 0].max()),
                float(xyz[:, 1].min()), float(xyz[:, 1].max())],
        spacing=GAP_SPACING,
        tension=GAP_TENSION,
    )
    if hasattr(grid, "gmt"):
        grid.gmt.gtype = 1
    smooth = pygmt.grdfilter(grid, filter=f"g{GAP_GAUSS_KM}", distance=4)
    smooth.to_netcdf(out)
    return out


def plot_panel_c(fig: pygmt.Figure, frame: str) -> None:
    grid = str(gap_p4_grid())
    _step_cpt("polar", GAP_CPT, reverse=True)
    # Resample so each colour bin meets the next along a smooth edge.
    grid_smooth = pygmt.grdsample(
        grid=grid,
        region=REGION,
        spacing="0.05",
        registration="gridline",
    )
    fig.grdimage(
        grid=grid_smooth,
        region=REGION,
        projection=PROJ,
        cmap=True,
        interpolation="c",
        nan_transparent=True,
    )
    fig.coast(
        region=REGION,
        projection=PROJ,
        shorelines="1/0.5p,black",
        frame=[frame, "af"],
    )
    if SHOW_PROFILE:
        # Trace of d; the profile runs on past the east edge to 145E.
        lon = np.linspace(SEC_REGION[0], REGION[1], 60)
        fig.plot(x=lon, y=np.full_like(lon, SEC_LAT), pen="1.2p,black")
        fig.plot(x=[SEC_REGION[0]], y=[SEC_LAT], style="c0.14c", fill="black")
        _label(fig, SEC_REGION[0], SEC_LAT, PROFILE_LABEL, FONT_PROFILE,
               justify="BL", dx=0.05, dy=0.12)
    _cbar(fig, ["a0.5", "x+ldVp (%)"])
    _panel_tag(fig, "c")


# ---------------------------------------------------------------------------
# Panel d — FWEA23 section along 40N
# ---------------------------------------------------------------------------
def fwea23_section() -> Path:
    """Cut (or reuse) the FWEA23 lon–depth slice in percent."""
    CACHE.mkdir(parents=True, exist_ok=True)
    out = CACHE / f"fwea23_{SEC_VAR}_{SEC_LAT:g}N.nc"
    if out.is_file():
        return out
    import xarray as xr

    w, e, top, bottom = SEC_REGION
    with xr.open_dataset(FWEA_NC) as ds:
        sec = ds[SEC_VAR].sel(latitude=SEC_LAT, method="nearest")
        sec = sec.sel(longitude=slice(w, e), depth=slice(top, bottom)).load()
    sec = (sec * 100.0).drop_vars("latitude")
    sec = sec.rename({"longitude": "x", "depth": "y"}).transpose("y", "x")
    # Plain Cartesian grid: drop the CF lon/lat tags so GMT does not treat
    # depth as latitude.
    sec.x.attrs = {}
    sec.y.attrs = {}
    sec.attrs = {}
    sec.name = "z"
    sec.to_netcdf(out)
    return out


def section_quakes() -> tuple[np.ndarray, np.ndarray]:
    """Relocated events within QUAKE_BAND of the profile, inside the section."""
    lat, lon, dep = np.loadtxt(QUAKE_FILE, skiprows=1, usecols=(0, 1, 2), unpack=True)
    lon = wrap_lon(lon)
    w, e, top, bottom = SEC_REGION
    keep = (
        (np.abs(lat - SEC_LAT) <= QUAKE_BAND)
        & (lon >= w) & (lon <= e)
        & (dep >= top) & (dep <= bottom)
    )
    return lon[keep], dep[keep]


def plot_panel_d(fig: pygmt.Figure, width: float) -> None:
    grid = str(fwea23_section())
    _step_cpt("polar", GAP_CPT, reverse=True)
    grid_smooth = pygmt.grdsample(
        grid=grid,
        region=SEC_REGION,
        spacing=SEC_SPACING,
        registration="gridline",
    )
    # d after the width marks x as geographic, so ticks read like the maps.
    proj = f"X{width:.4f}cd/-{SEC_HEIGHT}c"
    with pygmt.config(MAP_FRAME_TYPE="plain", MAP_FRAME_PEN="0.8p,black"):
        fig.grdimage(
            grid=grid_smooth,
            region=SEC_REGION,
            projection=proj,
            cmap=True,
            interpolation="c",
            nan_transparent=True,
        )
        for z in (410, 660):
            fig.plot(x=SEC_REGION[:2], y=[z, z], pen="0.6p,black,4_2:0p")
        if SHOW_QUAKES:
            lon, dep = section_quakes()
            fig.plot(x=lon, y=dep, style="c0.07c", fill="white", pen="0.3p,black")
        fig.basemap(frame=["ENsw", "xa10f5", "ya200f100+lDepth (km)"])
    _cbar(fig, ["a0.5", "x+ldVp (%)"])
    _panel_tag(fig, "d")


# ---------------------------------------------------------------------------
# Panel e — geometric sketch (built in cm, so circles stay round)
# ---------------------------------------------------------------------------
def _fillet(points, radii, n: int = 16) -> np.ndarray:
    """Polyline with each interior corner replaced by a circular arc."""
    pts = [np.asarray(p, dtype=float) for p in points]
    out = [pts[0]]
    for a, b, c, r in zip(pts[:-2], pts[1:-1], pts[2:], radii):
        u1 = (a - b) / np.hypot(*(a - b))
        u2 = (c - b) / np.hypot(*(c - b))
        theta = np.arccos(np.clip(u1 @ u2, -1.0, 1.0))
        bis = (u1 + u2) / np.hypot(*(u1 + u2))
        centre = b + bis * r / np.sin(theta / 2)
        t1 = b + u1 * r / np.tan(theta / 2)
        t2 = b + u2 * r / np.tan(theta / 2)
        a1 = np.arctan2(t1[1] - centre[1], t1[0] - centre[0])
        a2 = np.arctan2(t2[1] - centre[1], t2[0] - centre[0])
        da = (a2 - a1 + np.pi) % (2 * np.pi) - np.pi
        ang = a1 + da * np.linspace(0.0, 1.0, n)
        out.extend(centre + r * np.column_stack((np.cos(ang), np.sin(ang))))
    out.append(pts[-1])
    return np.vstack(out)


def _offset_corners(points, dist: float) -> np.ndarray:
    """Corners of the polyline shifted sideways; positive dist is left of travel.

    Offsetting the straight legs and intersecting them avoids the cusp a
    pointwise offset makes on the inside of a bend tighter than dist.
    """
    p = np.asarray(points, dtype=float)
    seg = np.diff(p, axis=0)
    seg /= np.hypot(seg[:, 0], seg[:, 1])[:, None]
    nrm = np.column_stack((-seg[:, 1], seg[:, 0]))
    out = [p[0] + dist * nrm[0]]
    for i in range(1, len(p) - 1):
        p1 = p[i] + dist * nrm[i - 1]
        p2 = p[i] + dist * nrm[i]
        s, _ = np.linalg.solve(np.column_stack((seg[i - 1], -seg[i])), p2 - p1)
        out.append(p1 + s * seg[i - 1])
    out.append(p[-1] + dist * nrm[-1])
    return np.array(out)


def _ellipse(xc, yc, a, b, n: int = 60) -> np.ndarray:
    t = np.linspace(0.0, 2 * np.pi, n)
    return np.column_stack((xc + a * np.cos(t), yc + b * np.sin(t)))


def _diapir(xc, y_base, y_head, a, b, half_w, flat_top=False, n: int = 60) -> np.ndarray:
    """Stem plus elliptical head as one outline.

    flat_top keeps only the lower half of the head, its top edge at y_head,
    for a head spread under the LAB.
    """
    alpha = np.arccos(np.clip(half_w / a, -1.0, 1.0))
    if flat_top:
        t = np.concatenate((
            np.linspace(np.pi + alpha, np.pi, n // 2),
            np.linspace(2 * np.pi, 2 * np.pi - alpha, n // 2),
        ))
    else:
        t = np.linspace(np.pi + alpha, -alpha, n)
    head = np.column_stack((xc + a * np.cos(t), y_head + b * np.sin(t)))
    return np.vstack(([xc - half_w, y_base], head, [xc + half_w, y_base]))


def _round_rect(xc, yc, w, h, r, angle, n: int = 8) -> np.ndarray:
    corners = [
        (w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90),
        (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270),
    ]
    pts = []
    for cx, cy, a0 in corners:
        ang = np.radians(a0 + np.linspace(0, 90, n))
        pts.append(np.column_stack((cx + r * np.cos(ang), cy + r * np.sin(ang))))
    pts = np.vstack(pts)
    rot = np.radians(angle)
    m = np.array([[np.cos(rot), -np.sin(rot)], [np.sin(rot), np.cos(rot)]])
    return pts @ m.T + [xc, yc]


def _poly(fig: pygmt.Figure, xy: np.ndarray, fill: str, pen: str | None = None) -> None:
    fig.plot(x=xy[:, 0], y=xy[:, 1], fill=fill, pen=pen, close=True)


def _arrow(fig: pygmt.Figure, x, y, angle, length, colour) -> None:
    fig.plot(
        x=[x], y=[y], style="v0.16c+e+a45+h0.4",
        direction=[[angle], [length]], pen=f"0.9p,{colour}", fill=colour,
    )


def plot_panel_e(fig: pygmt.Figure, width: float, height: float) -> None:
    """Volatiles off the stagnant slab -> upwellings -> thinning -> volcanism."""
    c = E_COL
    ztop, zbot = E_DEPTH

    def ex(lon):
        return (np.asarray(lon, dtype=float) - SEC_REGION[0]) * width / (
            SEC_REGION[1] - SEC_REGION[0]
        )

    def ey(z):
        return (zbot - np.asarray(z, dtype=float)) * height / (zbot - ztop)

    def txt(lon, z, text, colour="ink", justify="CM", font=FONT_E, angle=0):
        fig.text(
            x=float(ex(lon)), y=float(ey(z)), text=text, justify=justify,
            font=f"{font},{c.get(colour, colour)}", angle=angle,
        )

    surf = float(ey(0))

    # Mantle layers and the two discontinuities.
    fig.plot(
        x=[0, width, width, 0], y=[surf, surf, ey(410), ey(410)],
        fill=c["um"], close=True,
        region=[0, width, 0, height], projection=f"X{width:.4f}c/{height:.4f}c",
    )
    fig.plot(x=[0, width, width, 0], y=[ey(410), ey(410), ey(660), ey(660)],
             fill=c["mtz"], close=True)
    fig.plot(x=[0, width, width, 0], y=[ey(660), ey(660), 0, 0],
             fill=c["lm"], close=True)
    for z in (410, 660):
        fig.plot(x=[0, width], y=[ey(z), ey(z)], pen=f"0.5p,{c['soft']},3_2:0p")
        txt(110.25, z - 12, f"{z} km", colour="soft", justify="BL", font="6p,Helvetica")

    # Upwellings rise from the slab top; heads either rising or ponded at the LAB.
    slab_top = E_SLAB_BEND[1]
    y_lab = float(ey(E_LAB_THIN))
    heads = []
    for lon, z_head, a, b in E_UPWELLINGS:
        xc = float(ex(lon))
        ponded = z_head is None
        yh = y_lab if ponded else float(ey(z_head))
        heads.append((xc, yh, b, ponded))
        outline = _diapir(xc, float(ey(slab_top + 20)), yh, a, b, E_STEM_HALF, ponded)
        _poly(fig, outline, c["up"], f"0.5p,{c['up_edge']}")

    # Slab: rounded top and base (base bends tighter at the trench, wider at
    # the MTZ bend, as for a bent plate), joined by a round tip.
    corners = [
        (ex(E_TRENCH + 3.0), surf),
        (ex(E_TRENCH), surf),
        (ex(E_SLAB_BEND[0]), ey(E_SLAB_BEND[1])),
        (ex(E_SLAB_TIP), ey(E_SLAB_BEND[1])),
    ]
    r_trench, r_bend = E_SLAB_RADII
    top = _fillet(corners, radii=[r_trench, r_bend])
    base = _fillet(
        _offset_corners(corners, E_SLAB_THICK),
        radii=[max(r_trench - E_SLAB_THICK, 0.03), r_bend + E_SLAB_THICK],
    )
    tip_c = (top[-1] + base[-1]) / 2
    ang = np.radians(np.linspace(90, 270, 25))
    cap = tip_c + E_SLAB_THICK / 2 * np.column_stack((np.cos(ang), np.sin(ang)))
    _poly(fig, np.vstack((top, cap, base[::-1])), c["slab"], f"0.6p,{c['slab_edge']}")

    # Overriding lithosphere: surface, slab top down to the LAB, then the LAB west.
    k = int(np.argmax(top[:, 1] < y_lab))
    f = (top[k - 1, 1] - y_lab) / (top[k - 1, 1] - top[k, 1])
    x_lab = top[k - 1, 0] + f * (top[k, 0] - top[k - 1, 0])
    wedge = top[:k][top[:k, 1] < surf - 1e-6]  # slab top between surface and LAB
    lith = np.vstack((
        [[0, surf], [wedge[0, 0], surf]],
        wedge,
        [[x_lab, y_lab],
         [ex(E_CRATON_EDGE[1]), y_lab],
         [ex(E_CRATON_EDGE[0]), ey(E_LAB_CRATON)],
         [0, ey(E_LAB_CRATON)]],
    ))
    _poly(fig, lith, c["lith"], f"0.6p,{c['lith_edge']}")

    # Detached lithosphere sinking between the ponded heads; the arrow starts
    # just under the block's lower edge on its centre line.
    xb, yb = float(ex(E_BLOCK[0])), float(ey(E_BLOCK[1]))
    bw, bh = E_BLOCK_SIZE
    _poly(fig, _round_rect(xb, yb, bw, bh, bh / 4, E_BLOCK_TILT),
          c["lith"], f"0.6p,{c['lith_edge']}")
    y_foot = yb - bh / 2 / np.cos(np.radians(E_BLOCK_TILT)) - 0.05
    _arrow(fig, xb, y_foot, -90, 0.3, c["ink"])

    # Melt under the LAB, conduits, volcanoes; rising head gets an arrow.
    tri_w, tri_h = 0.12, 0.17
    for xc, yh, b, ponded in heads:
        if not ponded:
            _arrow(fig, xc, yh + b + 0.04, 90, 0.28, c["up_edge"])
            continue
        fig.plot(x=[xc, xc], y=[y_lab, surf], pen=f"0.9p,{c['melt']}")
        lens = _ellipse(xc, y_lab, 0.22, 0.065)
        _poly(fig, lens[lens[:, 1] <= y_lab + 1e-9], c["melt"], f"0.4p,{c['melt_edge']}")
        _poly(fig, np.array([[xc - tri_w, surf], [xc + tri_w, surf], [xc, surf + tri_h]]),
              c["melt"], f"0.4p,{c['melt_edge']}")
    xa = float(ex(E_ARC))
    _poly(fig, np.array([[xa - 0.1, surf], [xa + 0.1, surf], [xa, surf + 0.14]]),
          c["arc"], "0.4p,#666666")

    # Volatiles released from the flat slab top gather into the upwelling roots.
    drops = [
        (ex(lon + dl), ey(slab_top - dz), size)
        for lon, *_ in E_UPWELLINGS
        for dl, dz, size in E_DROP_CLUSTER
    ]
    drops += [(ex(lon), ey(slab_top - dz), 0.08) for lon, dz in E_DROP_LOOSE]
    drops = np.array(drops, dtype=float)
    fig.plot(x=drops[:, 0], y=drops[:, 1], size=drops[:, 2], style="cc",
             fill=c["vol"], pen="0.25p,white")

    # Section outline on top of the fills.
    fig.plot(x=[0, width, width, 0, 0], y=[surf, surf, 0, 0, surf],
             pen=f"0.6p,{c['ink']}")

    # Labels.
    txt(112.2, 118, "Craton")
    txt(134.9, 42, "Thinned lithosphere")
    txt(126.1, -58, "Intraplate volcanism")
    txt(E_ARC, -58, "Arc")
    txt(126.1, 318, "Delamination")
    txt(126.1, 458, "H@-2@-O, CO@-2@-", colour="vol")
    txt(118.6, 318, "Compositional", justify="RM")
    txt(118.6, 350, "upwelling", justify="RM")
    txt(131.4, 100, "Melt", colour="melt", justify="LM")
    txt(134.6, 238, "Big mantle", colour="soft", font="6.5p,Helvetica-Oblique")
    txt(134.6, 268, "wedge", colour="soft", font="6.5p,Helvetica-Oblique")
    txt(123.6, 612, "Stagnant slab", colour="white", font="6.5p,Helvetica-Bold")
    dip = np.degrees(np.arctan2(ey(0) - ey(E_SLAB_BEND[1]), ex(E_TRENCH) - ex(E_SLAB_BEND[0])))
    mid_lon, mid_z = E_TRENCH - 0.55 * (E_TRENCH - E_SLAB_BEND[0]), 0.55 * E_SLAB_BEND[1]
    txt(mid_lon + 0.9, mid_z + 18, "Pacific slab", colour="white",
        font="6.5p,Helvetica-Bold", angle=float(dip))
    _panel_tag(fig, "e")


def _merc_aspect(region) -> float:
    """Height / width of GMT's WGS-84 Mercator map of the region."""
    ecc = 0.0818191908426

    def merc_y(lat):
        p = np.radians(lat)
        es = ecc * np.sin(p)
        return np.log(np.tan(np.pi / 4 + p / 2) * ((1 - es) / (1 + es)) ** (ecc / 2))

    w, e, s, n = region
    return (merc_y(n) - merc_y(s)) / np.radians(e - w)


def main() -> None:
    os.chdir(FIG1)
    fig_w, fig_h = FIG_SIZE
    mx, my = FIG_MARGINS
    # Subplot cell and the map it holds (M? fits the cell, centred).
    cell_w = (fig_w - 2 * mx) / 2
    cell_h = (fig_h - 2 * my) / 2
    map_w = min(cell_w, cell_h / _merc_aspect(REGION))
    map_h = map_w * _merc_aspect(REGION)
    map_x0 = cell_w + 2 * mx + (cell_w - map_w) / 2  # left edge of b, d and e
    map_top = (cell_h + map_h) / 2  # top edge of c, from c's cell floor

    fig = pygmt.Figure()
    with _config():
        with fig.subplot(
            nrows=2,
            ncols=2,
            figsize=(f"{fig_w}c", f"{fig_h}c"),
            margins=[f"{mx}c", f"{my}c"],
            frame="wesn+n",
        ):
            with fig.set_panel(panel=0):
                plot_panel_a(fig, "WNse")
            with fig.set_panel(panel=1):
                plot_panel_b(fig, "ENsw")
            with fig.set_panel(panel=2):
                plot_panel_c(fig, "WNse")

        # The origin is back at the floor of c's cell.
        d_y0 = map_top - SEC_HEIGHT
        fig.shift_origin(xshift=f"{map_x0:.4f}c", yshift=f"{d_y0:.4f}c")
        plot_panel_d(fig, map_w)
        fig.shift_origin(yshift=f"{E_BOTTOM - d_y0:.4f}c")
        plot_panel_e(fig, map_w, E_HEIGHT)

    png = FIG1 / "Fig1_v4.png"
    pdf = FIG1 / "Fig1_v4.pdf"
    fig.savefig(png, dpi=400)
    fig.savefig(pdf)
    print(f"Saved {png}")
    print(f"Saved {pdf}")


if __name__ == "__main__":
    main()
