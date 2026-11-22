# C-H-O-driven mantle upwellings

Data and plotting scripts for:

Gou, Y., Zhu, X. & Liu, M. C-H-O-driven mantle upwellings from stagnant slabs destabilize cratonic lithosphere in East Asia.

https://github.com/YirenGou/GouYR_LiuM_2026_Chemical_Upwellings

## Data availability

Model initial files (`init.t3c`), mode files (`mode.t3c`), the output snapshots used to draw Figs. 2–4 and Extended Data Figs. 2–4, and the scripts that draw those figures and Fig. 1 and Extended Data Fig. 1 are available at https://github.com/YirenGou/GouYR_LiuM_2026_Chemical_Upwellings. Fig. 1 also uses lithospheric thickness derived from SAVANI (Auer et al., 2014; Steinberger and Becker, 2018), the GAP-P4 tomography model (Obayashi et al., 2013), the FWEA23 velocity model (Liu et al., 2024), and relocated earthquakes from the TX2019slab catalogue (Lu et al., 2019). Topography in Fig. 1 is SRTM15+ (Tozer et al., 2019), read at runtime from the Generic Mapping Tools remote grid `earth_relief_01m`. Values plotted in Extended Data Fig. 1 are stored in the accompanying script. Extended Data Fig. 5 is a schematic.

## Code availability

Plotting scripts are in this repository. The I2VIS solver is described by Gerya and Yuen (2003) and Gerya et al. (2021) and is available from the code developers on request. The hydrogen-diffusion routine added to I2VIS is not included here.

## Citation

Gou, Y., Zhu, X. & Liu, M. (2026) Data and plotting scripts for “C-H-O-driven mantle upwellings from stagnant slabs destabilize cratonic lithosphere in East Asia”. *GitHub*. https://github.com/YirenGou/GouYR_LiuM_2026_Chemical_Upwellings

## What is here

Each numerical experiment is the run whose plotted image matches that figure in the manuscript. Run a script from its figure directory. It reads the model folder next to it.

| Manuscript figure | Script | Model folder | Files the script reads |
|---|---|---|---|
| Fig. 1 | `Fig1/plot_fig1_v4.py` | — | `savani.l.grd`; `GAP_P4`; `FWEA23.r0.0.nc`; `relocated_eq_list`. Topography is fetched at runtime from GMT `earth_relief_01m` (SRTM15+). |
| Fig. 2 | `Fig2/plot_fig2_GSR.py` | `Fig2_8000ppm_Moho55km_GSR` | `init.t3c`, `mode.t3c`; `gouc`, `gouz`, `gout`, `gouu` at steps 1, 50, 135, 190 |
| Fig. 3 | `Fig3/plot_fig3_GSR.py` | `Fig3a_Reduced_Moho55km_GSR`, `Fig3b_Oxidized_Moho55km_GSR` | `init.t3c`, `mode.t3c`; `gouc` at steps 0, 70, 130, 180 (reduced) and 0, 80, 160, 360 (oxidized) |
| Fig. 4 | `Fig4/plot_fig4_GSR.py` | `Fig4_C-H_MTZ0.2PhaseChange_0.1MPa0.01WeakML_MinMiu1E19rho3.28_CL100km_8000ppm_CorrectT_GSR` | `init.t3c`, `mode.t3c`; `gouc` and `gouz` at steps 1, 70, 130, 200 |
| Extended Data Fig. 1 | `FigS1/plot_figS1_v2.py` | — | Digitized curves are stored in the script. `RedoxFront_references.md` records their sources. |
| Extended Data Fig. 2 | `FigS2/plot_figS2_GSR.py` | `FigS2_C-H_MTZ0.2PhaseChange_10MPa0.6-0.3WeakML_MinMiu1E19rho3.28_CL100km_Moho55km_8000ppm_GSR` | `init.t3c`, `mode.t3c`; `gouc` and `gouz` at steps 1, 70, 170, 230 |
| Extended Data Fig. 3 | `FigS3/plot_figS3_GSR.py` | `FigS3_PointWaterSource_Moho55km_GSR` | `init.t3c`, `mode.t3c`; `gouc`, `gouz`, `gout`, `gouu` at steps 2, 60, 120 |
| Extended Data Fig. 4 | `FigS4/plot_figS4_GSR.py` | `FigS4_ThermalPlume_Equal3.25rho_Moho55km_GSR` | `init.t3c`, `mode.t3c`; `gouc`, `gout`, `gouu` at steps 2, 70, 150 |

Extended Data Fig. 5 is a schematic of the staggered grid. It has no model file and no plotting script.

`init.t3c` and `mode.t3c` record the experiment setup. Redrawing a figure reads the snapshot files and does not require rerunning I2VIS.

The snapshots are the timesteps drawn in the manuscript.

## File contents

| File | Contents | Units as read by the scripts |
|---|---|---|
| `init.t3c` | I2VIS initial condition | — |
| `mode.t3c` | I2VIS mode file: material properties, boundary conditions, and run controls | — |
| `gouc<step>.txt` | Material field, run-length encoded. The first value is model time. | material index; time in years |
| `gouz<step>.txt` | Node-centred hydrogen. Coordinates in the file are metres. | atomic ppm H/Si. The script converts to wt ppm H₂O with `18.015 / (2 × 146.94)` |
| `gout<step>.txt` | Node-centred temperature. Coordinates are metres. | kelvin in the file; the script plots degrees Celsius (`T − 273`) |
| `gouu<step>.txt` | Node-centred velocity components `ux` and `uz` | as stored by I2VIS; used for arrow direction and relative length |

Material-index legends are in each plotting script (`MATERIAL_LEGEND`).

## Redraw a figure

From the figure directory:

```text
python plot_fig2_GSR.py
```

Use the script name in that directory: `plot_fig1_v4.py`, `plot_fig3_GSR.py`, `plot_fig4_GSR.py`, `plot_figS1_v2.py`, `plot_figS2_GSR.py`, `plot_figS3_GSR.py`, or `plot_figS4_GSR.py`.

Figs. 2–4 and Extended Data Figs. 1–4 use `numpy` and `matplotlib`. Fig. 1 also uses `pygmt`, `xarray`, and a local GMT installation, and it downloads `earth_relief_01m` from the GMT data server. The script sets that server to `https://mirrors.ustc.edu.cn/gmtdata`. Package versions were not pinned.

## Third-party files in Fig. 1

| File | Source |
|---|---|
| `Fig1/Lithospheric thickness/savani.l.grd` | Lithospheric thickness from SAVANI (Auer et al., 2014; Steinberger and Becker, 2018) |
| `Fig1/MTZ_StagnantSlabs/GAP_P4/GAP_P4/GAP_P4` | GAP-P4 P-wave tomography (Obayashi et al., 2013) |
| `Fig1/MTZ_StagnantSlabs/FWEA23_ChujieLiu/FWEA23.r0.0.nc` | FWEA23 (Liu et al., 2024) |
| `Fig1/MTZ_StagnantSlabs/TX2019slab/TX2019slab/relocated_eq_list` | Relocated earthquakes, TX2019slab (Lu et al., 2019) |
| GMT `earth_relief_01m` (downloaded at runtime) | SRTM15+ (Tozer et al., 2019) |

`FWEA23.r0.0.nc` is about 365 MB. A normal GitHub push rejects a file larger than 100 MB. That file needs [Git LFS](https://git-lfs.com) or a separate archive.

These four files were produced by other groups. The MIT Licence of this repository does not replace their original terms.

## Licence

Plotting scripts and model files generated for this study are released under the MIT Licence. Copyright (c) 2026 Yiren Gou. See [LICENSE](LICENSE).
