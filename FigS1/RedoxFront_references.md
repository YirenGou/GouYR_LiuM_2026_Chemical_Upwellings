# Redox front：图件、图注与文献约束

## 1. 图件

| 文件 | 内容 |
|---|---|
| `Fig_RedoxFront.png` / `.pdf` / `.svg` | 两栏图（宽 183 mm），两个 panel 都由脚本绘制，字体字号统一，PDF 和 SVG 全矢量 |
| `plot_redox_front_figure.py` | 生成上图的脚本。a 按 `C_PhaseDiagram.jpg` 重画：相界线和颜色从原图数字化，写在脚本开头的 `A_BOUNDARY` 等常数里；要改相图直接改这些常数。b 为前人对 redox front 深度的约束 |
| `C_PhaseDiagram.jpg` / `.cdr` | a 图的 CorelDRAW 原稿，脚本不再读取 |
| `papers/` | 已读全文的 12 篇 PDF |
| `RedoxFront_constraints.png` / `.pdf`、`plot_redox_front_constraints.py` | 最早的工作图：把文献数据直接叠在相图上 |
| `Stagno2013_supp/` | Stagno et al. (2013) 的 Fig. 3 原图和补充材料 |

**编号规则**：b 图上的数字是数据项的编号。左侧（有氧化程度的数据）自上而下编为 1–5；右栏 Depth only 按误差棒最深处由浅到深向右排列，编为 6–14，最深处相同时按最浅处排序。同一篇文献可以对应两个数据项（8 和 13 都出自 Dasgupta et al. 2013）。

**核实状态**：1–6、8、10、11、13、14 已对照全文；7、9 此前已读开放全文；12 只核对了摘要。

## 2. Figure caption

图注里用作者–年份引文献，定稿时换成正文的文献序号即可。

### 中文

**图 X 地幔中碳的赋存相态与氧化还原锋面深度。** **a**，碳在深度–氧逸度（fO₂，相对 FMQ 缓冲）空间的相态示意图（据文献修改，*来源待补*）。右纵轴为压力，按本文数值模型的设置由深度换算：P = ρgz，ρ = 3300 kg m⁻³，g = 9.81 m s⁻²（4.5 GPa ≈ 139 km，10 GPa ≈ 309 km）。两条水平白色虚线为本项目数值模型采用的氧化还原锋面：还原地幔取 4.5 GPa，氧化地幔取 10 GPa；斜的白色虚线示意两者之间可能的过渡。**b**，前人对氧化还原锋面深度的约束，纵轴同 a，左侧刻度为按同一换算得到的压力。氧化还原锋面指上涌地幔中石墨或金刚石被氧化、开始出现碳酸盐熔体的深度。与 a 不同，b 的横轴不是锋面处的局部 fO₂，而是地幔在 3 GPa 参考压力下的 fO₂，用来表示地幔整体的氧化程度；上横轴为等效的全岩 Fe³⁺/ΣFe。圆圈和连线表示氧化还原锋面深度随氧化程度的变化趋势。橙色（**1**）和蓝色（**5**）为热力学模型给出的、地幔沿 1320 °C 绝热线上涌时到达石墨/金刚石–碳酸盐缓冲线的深度：橙色为 Fe³⁺/ΣFe 2–7%（Stagno et al., 2013），深度不确定度约 ±50 km；蓝色为同类计算延伸到 8–14% 的结果（Zhang et al., 2024）。绿色（**3**）为早期氧逸度计给出的碳酸盐熔融起始深度：Fe³⁺/ΣFe 为 3% 时约 100 km，约 10% 时约 150 km（Stagno & Frost, 2010）。方块为单个估计的报道值或范围中点，误差棒为报道范围。**2**，太古宙较热（位温 1420 °C）、较还原（Fe³⁺/ΣFe 2%）地幔的氧化还原熔融深度（Aulbach & Stagno, 2016）。**4**，由洋中脊玄武岩 Fe₂O₃ 含量反演的源区 Fe³⁺/ΣFe（5.3 ± 0.3%）及相应的氧化还原熔融深度（Davis & Cottrell, 2021）。**5**（方块），由橄榄石–熔体 V/Sc 氧逸度计得到的洋中脊玄武岩源区 Fe³⁺/ΣFe（6–8%）及相应的碳酸盐熔融起始深度（Zhang et al., 2024）。右栏为未给出 fO₂ 的深度约束：**6**，上涌地幔发生氧化还原熔融的深度范围（Fux et al., 2025）；**7**，综述给出的氧化还原锋面范围（Yaxley et al., 2019）；**8**，洋中脊下的氧化还原锋面（Dasgupta et al., 2013）；**9**，C⁰→CO₂ 氧化还原锋面（Schmidt et al., 2026）；**10**，金属饱和深度处的氧化还原熔融（Rohrbach & Schmidt, 2011）；**11**，约 260 km 的地震波速度间断面，可能代表碳促进的熔融的起始（Gu et al., 2005; Hua et al., 2023）；**12**，碳酸盐化橄榄岩固相线与洋中脊绝热线限定的碳抽取深度范围（Dasgupta & Hirschmann, 2006）；**13**，局部氧化地幔中含碳硅酸盐熔融的起始深度，相当于地震 X 间断面（Dasgupta et al., 2013）；**14**，大洋软流圈底界的平均深度及其变化范围（Sun & Zhou, 2023）。黑色虚线是 a 中两条模型锋面的延伸。锋面随地幔氧化程度升高而加深：还原端元相当于 Fe³⁺/ΣFe 约 3–4% 的地幔，氧化端元相当于 Fe³⁺/ΣFe 约 12% 的地幔，也是碳酸盐化地幔开始熔融的深度（Dasgupta & Hirschmann, 2006, 2010; Eguchi & Dasgupta, 2018）。

### English

**Fig. X | Carbon speciation and the depth of the redox front in the upper mantle.** **a**, Schematic stability fields of carbon-bearing phases as a function of depth and oxygen fugacity (fO₂) relative to the fayalite–magnetite–quartz (FMQ) buffer (modified from ref. *to be added*). The right-hand axis gives pressure, converted from depth as in our numerical models: P = ρgz with ρ = 3,300 kg m⁻³ and g = 9.81 m s⁻² (4.5 GPa ≈ 139 km and 10 GPa ≈ 309 km). The two horizontal white dashed lines mark the redox fronts adopted in our models, at 4.5 GPa for reduced mantle and 10 GPa for oxidized mantle; the inclined white dashed line sketches a possible transition between them. **b**, Published constraints on the depth of the redox front, plotted on the depth axis of **a**; the left-hand axis gives pressure from the same conversion. The redox front is the depth at which graphite or diamond in upwelling mantle is oxidized and carbonate melt first appears. Unlike in **a**, the horizontal axis is not the local fO₂ at the front but the fO₂ of the mantle at a reference pressure of 3 GPa, used as a measure of its bulk oxidation state; the upper axis is the equivalent bulk Fe³⁺/ΣFe. Circles joined by lines show trends of redox-front depth with oxidation state. Orange (**1**) and blue (**5**) give the depth at which mantle upwelling along a 1,320 °C adiabat reaches the graphite/diamond–carbonate buffer in thermodynamic models: orange is for Fe³⁺/ΣFe of 2–7% (Stagno et al., 2013), with a depth uncertainty of about ±50 km, and blue extends the same type of calculation to 8–14% (Zhang et al., 2024). Green (**3**) is the onset of carbonate melting from an earlier oxybarometer calibration: about 100 km for Fe³⁺/ΣFe of 3% and about 150 km for about 10% (Stagno & Frost, 2010). Squares are single estimates, plotted at the reported value or the mid-point of the reported range, and bars are the reported ranges. **2**, Redox melting of hotter (potential temperature 1,420 °C) and more reduced (Fe³⁺/ΣFe of 2%) Archaean mantle (Aulbach & Stagno, 2016). **4**, Fe³⁺/ΣFe of the mid-ocean-ridge basalt (MORB) source (5.3 ± 0.3%) inferred from the Fe₂O₃ contents of MORB, and the corresponding depth of redox melting (Davis & Cottrell, 2021). **5** (square), Fe³⁺/ΣFe of the MORB source (6–8%) from olivine–melt V/Sc oxybarometry, and the corresponding onset of carbonate melting (Zhang et al., 2024). Constraints without a stated fO₂ are shown on the right: **6**, depth range of redox melting in mantle upwellings (Fux et al., 2025); **7**, range of the redox front given in a review (Yaxley et al., 2019); **8**, redox front beneath mid-ocean ridges (Dasgupta et al., 2013); **9**, C⁰→CO₂ redox front (Schmidt et al., 2026); **10**, redox melting at the depth of metal saturation (Rohrbach & Schmidt, 2011); **11**, seismic velocity discontinuity near 260 km, which may mark the onset of carbon-assisted melting (Gu et al., 2005; Hua et al., 2023); **12**, depth range of carbon extraction set by the carbonated peridotite solidus and the sub-ridge adiabat (Dasgupta & Hirschmann, 2006); **13**, onset of carbonated silicate melting in locally oxidized mantle, equivalent to the seismic X-discontinuity (Dasgupta et al., 2013); **14**, mean depth and range of the base of the oceanic asthenosphere (Sun & Zhou, 2023). Black dashed lines continue the two model redox fronts of **a**. The front deepens as the mantle becomes more oxidized: the reduced end-member corresponds to mantle with Fe³⁺/ΣFe of about 3–4%, and the oxidized end-member to mantle with Fe³⁺/ΣFe of about 12%, which is also the depth at which carbonated mantle begins to melt (Dasgupta & Hirschmann, 2006, 2010; Eguchi & Dasgupta, 2018).

## 3. b 图数据（编号与图上一致）

圆圈加连线用于给出变化趋势的三组数据：1（橙）、3（绿）、5 的延伸段（蓝）。其余单个估计统一用灰色方块表示报道值或范围中点，误差棒表示报道范围。

### 3.1 有氧化程度的数据（左侧，自上而下）

| # | 文献 | 原文内容 | 图上位置 | 核实 | 链接 |
|---|---|---|---|---|---|
| 1 | Stagno, V., Ojwang, D. O., McCammon, C. A. & Frost, D. J. The oxidation state of the mantle and the extraction of carbon from Earth's interior. *Nature* **493**, 84–88 (2013) | Fig. 3a：沿 1320 °C 绝热线，不同全岩 Fe³⁺/ΣFe 的地幔 fO₂ 随减压升高，约 1/60 log 单位/km。Fe³⁺/ΣFe 4% 的地幔在 150 ± 50 km 到达石墨–碳酸盐熔体平衡线；“考虑 fO₂ 误差后，碳开始氧化的深度不确定度约 50 km”，水的存在可能使该深度再增加相近的量。若碳酸盐熔融发生在 >200 km，全岩 Fe³⁺ 需 >7 ± 2%。3–4% 的 Fe³⁺ 与 MORB 源区的 fO₂ 较吻合；由岩石圈样品得到的约 2% 可能是下限。氧化还原熔融比碳酸盐化橄榄岩固相线浅约 150 km | 橙色圆圈：2%–7% 各线与平衡线的交点，深度 83、119、154、183、206、228 km（数字化，见第 4 节）。原文的 ±50 km 不确定度只在图注里说明，没有画误差棒 | 全文；交点为 Fig. 3a 数字化（4% 读出 154 km，原文为 150 km） | https://doi.org/10.1038/nature11679 |
| 2 | Aulbach, S. & Stagno, V. Evidence for a reducing Archean ambient mantle and its effects on the carbon cycle. *Geology* **44**, 751–754 (2016) | Fig. 2A：按 Stagno et al. (2013) 的方法在位温 1420 °C 下计算；Fe³⁺/ΣFe 2%、含 10 ppm C 的地幔在约 100 km 到约 80 km 之间发生氧化还原熔融，可以满足 3000 Ma 时 ΔFMQ −1.7 ± 1.1 的观测。“Fe³⁺/ΣFe 越低，氧化还原熔融越浅”。1 GPa 处太古宙样品 ΔFMQ −1.19 ± 0.33（2σ），后太古宙（含 MORB）−0.26 ± 0.44 | x = 2% 对应的 −2.13，y = 100 km。横向误差棒 ±0.33 取自该文太古宙 fO₂ 的 2σ，是我的处理 | 全文。Stagno (2019, *J. Geol. Soc.* 176, 375–387) 的综述转述了同一结果 | https://doi.org/10.1130/G38070.1 |
| 3 | Stagno, V. & Frost, D. J. Carbon speciation in the asthenosphere: experimental measurements of the redox conditions at which carbonate-bearing melts coexist with graphite or diamond in peridotite assemblages. *Earth Planet. Sci. Lett.* **300**, 72–84 (2010) | 碳酸盐熔融只在 <150 km 通过氧化还原反应开始；这个深度对应全岩 Fe³⁺/ΣFe 的最高合理估计（约 0.1），更典型的包体值 0.03 把氧化还原熔融限制在 <100 km。结论：起始深度为 100–150 km，“较深的值对应高度氧化的地幔”。橄榄岩地幔中碳酸盐只有在高度氧化的条件下才能在 >150 km 稳定 | 绿色圆圈：（3%，100 km）和（10%，150 km），连线表示趋势 | 全文。该文用的是旧的石榴石氧逸度计，文献 1 修订后同样的 Fe³⁺/ΣFe 对应更深的锋面 | https://doi.org/10.1016/j.epsl.2010.09.038 |
| 4 | Davis, F. A. & Cottrell, E. Partitioning of Fe₂O₃ in peridotite partial melting experiments over a range of oxygen fugacities elucidates ferric iron systematics in mid-ocean ridge basalts and ferric iron content of the upper mantle. *Contrib. Mineral. Petrol.* **176**, 67 (2021) | MORB 源区 Fe₂O₃ = 0.48 ± 0.03 wt%，Fe³⁺/ΣFe = 0.053 ± 0.003。“按 Stagno et al. (2013) 的模型，Fe³⁺/ΣFe 0.03、含 30 ppm C 的地幔约在 150 km 开始氧化还原熔融；0.05–0.06 则在 200–230 km 开始，与 Dasgupta et al. (2013) 的 200–250 km 几乎一致”。引言：“地幔越氧化，氧化还原熔融越深” | x = 5.3 ± 0.3%，y = 200–230 km | 全文。该文读 Stagno 模型时把氧化 30 ppm C 消耗的约 1% Fe³⁺ 算在内，所以这个点比曲线深约 25 km | https://doi.org/10.1007/s00410-021-01823-3 |
| 5 | Zhang, F.-Y. et al. The redox state of the asthenospheric mantle and the onset of melting beneath mid-ocean ridges. *J. Geophys. Res. Solid Earth* **129**, e2023JB027033 (2024) | MORB 源区含 0.60–0.75 wt% Fe₂O₃，相当于 Fe³⁺/ΣFe 6–8%；这样的地幔在 200–250 km 发生氧化还原熔融。原生 MORB 的 fO₂ 为 FMQ+0.46 ± 0.26，校正到源区（1.2 GPa）为 FMQ+0.78 ± 0.26；夏威夷源区为 FMQ+1.71 ± 0.24。Fig. 10a 按文献 1 的方法在位温 1320 °C 下计算了 2%–15% 的等 Fe³⁺/ΣFe 线。“金刚石在 >200–250 km 被氧化成碳酸盐熔体需要很高的全岩 Fe³⁺/ΣFe，意味着存在地幔柱之类的异常氧化储库” | 方块：x 为 6%、7%、8%，y = 200–250 km。蓝色圆圈：8%–14% 各线与缓冲线的交点，从文献 1 的 7% 点接出 | 全文；交点为 Fig. 10a 数字化（见第 4 节） | https://doi.org/10.1029/2023JB027033 |

### 3.2 只有深度的数据（右栏，按最深处由浅到深）

| # | 文献 | 原文内容 | 图上位置 | 核实 | 链接 |
|---|---|---|---|---|---|
| 6 | Fux, M., Schmidt, M. W. & Liebske, C. Redox melting of garnet lherzolite: generation of carbonated silicate and sulfide melts and implications for OIB formation from chalcophile and redox-sensitive elements. *Geochem. Geophys. Geosyst.* **26**, e2024GC012025 (2025) | 上涌地幔在相当于约 8–5 GPa 的深度发生 CO₂ 诱发的氧化还原熔融；通俗摘要写作“浅于 240–150 km”。5 GPa、约 150 km 对应 Fe³⁺/ΣFe 为 0.04 的 BSE 型地幔的氧化还原锋面 | 150–240 km | 全文 | https://doi.org/10.1029/2024GC012025 |
| 7 | Yaxley, G. M. et al. CO₂-rich melts in Earth. In *Deep Carbon: Past to Present* (eds Orcutt, B. N., Daniel, I. & Dasgupta, R.) 129–162 (Cambridge Univ. Press, 2019) | 氧化还原锋面在 150–250 km。“若地幔在约 250 km 以深是还原的并达到金属饱和，碳酸岩熔体只能稳定到 150 km”。“若上涌地幔中存在碳酸盐，位温 1400 °C 时熔融发生在约 300 km”。碳酸盐化固相线只适用于局部氧化的地幔域 | 150–250 km | 开放全文 | https://doi.org/10.1017/9781108677950.006 |
| 8 | Dasgupta, R. et al. Carbon-dioxide-rich silicate melt in the Earth's upper mantle. *Nature* **493**, 211–215 (2013) | “上涌的洋中脊下地幔中，氧化还原熔融很可能在 250–200 km 开始”；最先形成的含碳硅酸盐熔体出现在约 250–220 km。约 250 km 以深的地幔在全球尺度上金属饱和。碳酸盐化橄榄岩固相线深于约 250 km 的部分只适用于局部氧化的地幔域 | 200–250 km | 全文 | https://doi.org/10.1038/nature11731 |
| 9 | Schmidt, M. W., Paneva, N. & Giuliani, A. A universal concept for melting in mantle upwellings. *Nature* **650**, 903–908 (2026) | C⁰→CO₂ 的反应在 9–7 GPa 之间完成，最浅约 230 km；摘要给出约 250 km | 230–250 km | 开放全文 | https://doi.org/10.1038/s41586-025-10065-3 |
| 10 | Rohrbach, A. & Schmidt, M. W. Redox freezing and melting in the Earth's deep mantle resulting from carbon–iron redox coupling. *Nature* **472**, 209–212 (2011) | 金属饱和发生在 >约 8 GPa，相当于约 250 km；更深处碳酸盐被还原成金刚石。上涌时在约 660 km 和约 250 km 发生碳酸岩氧化还原熔融。同文提到包体研究显示碳酸盐在克拉通下和软流圈地幔中约 120 km 以深不稳定 | 250 km（原文未给范围） | 全文 | https://doi.org/10.1038/nature09899 |
| 11 | Gu, Y. J., Lerner-Lam, A. L., Dziewonski, A. M. & Ekström, G. Deep structure and seismic anisotropy beneath the East Pacific Rise. *Earth Planet. Sci. Lett.* **232**, 259–272 (2005)；Hua, J., Fischer, K. M., Becker, T. W., Gazel, E. & Hirth, G. Asthenospheric low-velocity zone consistent with globally prevalent partial melting. *Nat. Geosci.* **16**, 175–181 (2023) | Gu：北东太平洋海隆之下约 260 km 有一个弱反射面，可能与流变转变、流向改变或部分熔融的出现有关；200–300 km 存在垂向快的各向异性。Hua：除了全球广泛存在的约 150 km 正速度梯度外，还有零星出现的约 260 km 正速度梯度，“可能代表碳促进的熔融的起始” | 260 km | 全文 | https://doi.org/10.1016/j.epsl.2005.01.019 ； https://doi.org/10.1038/s41561-022-01116-9 |
| 12 | Dasgupta, R. & Hirschmann, M. M. Melting in the Earth's deep upper mantle caused by carbon dioxide. *Nature* **440**, 659–662 (2006) | 3–10 GPa 碳酸盐化橄榄岩固相线：洋中脊下熔融最深可达 330 km，产生 0.03–0.3% 碳酸岩熔体；碳从约 200–330 km 被抽取 | 200–330 km | 仅摘要 | https://doi.org/10.1038/nature04612 |
| 13 | Dasgupta et al. (2013)，同 8 | “如果地幔局部氧化，含碳硅酸盐熔融的起始深度可能与大洋地幔 X 间断面（270–330 km）相近” | 270–330 km | 全文 | 同 8 |
| 14 | Sun, S. & Zhou, Y. Age-independent oceanic plate thickness and asthenosphere melting from SS precursor imaging. *J. Geophys. Res. Solid Earth* **128**, e2022JB024805 (2023) | 大洋区软流圈底界（220-km 间断面）深度在 180–340 km 之间变化，平均约 255 km，与洋底年龄无关。该文没有把这个界面解释为氧化还原锋面 | 方块 255 km，误差棒 180–340 km | 全文 | https://doi.org/10.1029/2022JB024805 |

### 3.3 只在图注中引用

| 文献 | 原文内容 | 核实 | 链接 |
|---|---|---|---|
| Dasgupta, R. & Hirschmann, M. M. The deep carbon cycle and melting in Earth's interior. *Earth Planet. Sci. Lett.* **298**, 1–13 (2010) | 摘要：“>300 km 的碳酸盐化熔融，或稍浅处含金刚石或含金属地幔的氧化还原熔融”产生碳酸岩和含碳硅酸盐熔体 | 全文 | https://doi.org/10.1016/j.epsl.2010.06.039 |
| Eguchi, J. & Dasgupta, R. Redox state of the convective mantle from CO₂–trace element systematics of oceanic basalts. *Geochem. Persp. Lett.* **8**, 17–21 (2018) | 若 CO₂–微量元素富集来自再循环地壳，熔融应从碳酸盐饱和条件开始，沿绝热线对应 >10 GPa | 开放全文（卷号请核对） | https://doi.org/10.7185/geochemlet.1823 |

### 3.4 读过原文后没有画的地球物理观测

- **约 150 km 的正速度梯度**（Hua et al., 2023）：全球广泛存在，解释为软流圈内富熔体层的底界。深度与还原端元一致，但原文没有把它与氧化还原熔融联系起来，所以没有画。如果想用，可以作为一个 150 km 的点加到右栏，图注里需要说明它是富熔体层底界。
- **高导层**（Lizarralde et al., 1995, *J. Geophys. Res.* 100, 17837–17854, https://doi.org/10.1029/95JB01244）：反演得到 150–400 km 之间的高导带（0.05–0.1 S/m），最小结构反演中集中在 150–300 km；同文指出单调递增的电导率模型也能拟合数据。范围太宽，没有画。后来的文献常把它引作“200–250 km 的电导率峰值”，原文并没有这样写。
- 上一版的“地球物理 200–250 km”一项是从别的文献转引的，已经用上面核对过的条目替换。

## 4. b 图横坐标的设计与换算

**图上的轴名**：与 a 相同，写作 Log fO₂ (relative to FMQ)。两者含义不同，在图注里说明：a 是锋面处的局部 fO₂，b 是地幔在 3 GPa 参考压力下的 fO₂。

**为什么参考压力取 3 GPa**：同一块地幔（Fe³⁺/ΣFe 固定）的 fO₂ 随深度变化，必须约定一个参考压力才能比较不同地幔的氧化程度。文献 1 的等值线可以直接读出 3 GPa 处的值。

**上横坐标**：等效全岩 Fe³⁺/ΣFe，刻度位置是等值线在 3 GPa 处的 ΔFMQ：2–7% 取自文献 1，8–14% 取自文献 5。数据项 2、3、4、5 的原文给的都是 Fe³⁺/ΣFe，按上横轴定位。

**文献 1 的数字化结果**（Fig. 3a，1320 °C 绝热线；读图误差约 ±0.05 log 单位、±5 km）：

沿绝热线，ΔFMQ(z) ≈ ΔFMQ(108 km) − 0.0156 × (z − 108)，适用范围约 68–250 km。原文给的斜率是约 1/60（0.0167）log 单位/km。

| 全岩 Fe³⁺/ΣFe | ΔFMQ @3 GPa（96 km） | ΔFMQ @108 km | ΔFMQ @246 km | 氧化还原熔融深度 | 该处 ΔFMQ |
|---|---|---|---|---|---|
| 2% | −2.13 | −2.31 | −4.46 | 83 km | −1.92 |
| 3% | −1.39 | −1.57 | −3.76 | 119 km | −1.75 |
| 4% | −0.90 | −1.08 | −3.23 | 154 km | −1.79 |
| 5% | −0.51 | −0.69 | −2.85 | 183 km | −1.86 |
| 6% | −0.19 | −0.37 | −2.52 | 206 km | −1.91 |
| 7% | +0.09 | −0.085 | −2.24 | 228 km | −1.96 |

- 六条线在同一深度的 ΔFMQ 与 log(Fe³⁺/ΣFe) 近似成直线，斜率约 4.1，符合 fO₂ ∝ (Fe³⁺/Fe²⁺)⁴ 的预期。
- 原图的蓝色路径：含 30 ppm C、Fe³⁺/ΣFe 为 4% 的地幔在约 150 km 开始熔融，沿缓冲线氧化碳约 30 km，全岩 Fe³⁺/ΣFe 降低 1%，此后沿 3% 线上升。
- 原图还给出 Fe–Ni 析出线和 MORB 源区范围（ΔFMQ 约 −0.6 到 +0.5）。
- 补充 Excel 里只有石榴石氧逸度计的单点算例，没有等值线数据。

**文献 5 的数字化结果**（Fig. 10a，位温 1320 °C；读图误差约 ±0.05 log 单位、±5 km）：

| 全岩 Fe³⁺/ΣFe | ΔFMQ @3 GPa | 氧化还原熔融深度 | 对照：文献 1 |
|---|---|---|---|
| 2% | −2.12 | 83 km | 83 km |
| 3% | −1.37 | 121 km | 119 km |
| 4% | −0.89 | 155 km | 154 km |
| 5% | −0.47 | 186 km | 183 km |
| 6% | −0.15 | 209 km | 206 km |
| 7% | +0.11 | 232 km | 228 km |
| 8% | +0.39 | 250 km | — |
| 9% | +0.62 | 267 km | — |
| 10% | +0.76 | 280 km | — |
| 11% | +0.91 | 291 km | — |
| 12% | +1.11 | 299 km | — |
| 13% | +1.18 | 307 km | — |
| 14% | +1.31 | 316 km | — |

- 两篇用的是同一条绝热线，2–7% 相差不超过 4 km，所以图上 2–7% 用文献 1，8–14% 接文献 5，连成一条曲线。
- 12% 的线在原图上与缓冲线几乎重合于 300 km 处，被粗线遮住，其位置由相邻线的间距推定。
- 15% 的线与缓冲线的交点（约 324 km）超出原图缓冲线的末端，没有采用。
- 6–8% 的线在 1.2 GPa 处为 FMQ+0.7 到 +1.3，与原文所说的 +0.6 到 +1.3 相符。

**b 图中属于我的处理、不是文献原值的部分**

1. 圆圈的深度是从文献 1 和 5 的原图数字化得到的交点，原文没有逐条列出。
2. 数据项 2 的横向误差棒（见下）。
3. 数据项 3 的两个点按 Fe³⁺/ΣFe 用上横轴定位。原文用的是旧氧逸度计，它自己算出的 fO₂ 比文献 1 低，所以这两个点的下横轴读数不代表原文的 fO₂。
4. 数据项 14 的方块取平均值，误差棒取原文给的变化范围，不是不确定度。

**数据项 2 的 2% 是否可靠，横向误差棒怎么取**

2% 是 Aulbach & Stagno (2016) 为满足太古宙样品的低 fO₂ 而采用的值，不是直接测量。太古宙地幔是否更还原目前有争议：

- 支持：该文测得太古宙比后太古宙低约 0.9 log 单位。按 fO₂ ∝ (Fe³⁺/Fe²⁺)⁴ 折算，现代取 3–4% 时太古宙为 1.8–2.4%。Zhu et al. (2026) 的数值模拟也得出地幔 Fe³⁺/ΣFe 自早太古代以来大约翻倍。
- 反对：Zhang et al. (2024, *Nat. Commun.*) 认为把 fO₂ 归一到同一参考压力后，地幔的氧化状态自冥古宙以来没有变化；Birner et al. (2024) 也认为超低 fO₂ 不代表太古宙地幔的 Fe³⁺/Fe²⁺ 更低。

图上的横向误差棒取该文太古宙 fO₂ 的 2σ（±0.33 log 单位），相当于 Fe³⁺/ΣFe 1.7–2.4%，只反映测量误差。如果想把争议也包括进去，误差棒右端应延伸到现代值（3% 对应 x = −1.39）。这个点对应的是位温 1420 °C 的绝热线，其他数据是 1320 °C，不完全可比。

## 5. 模型端元取值的依据（4.5 GPa 和 10 GPa）

**压力–深度换算**（按本文模型）：模型用 `markvis.c` 的 `depthp()` 由地表以下深度算压力，P = 3300 kg m⁻³ × 9.80665 m s⁻² × z，`i2vis.c` 用这个 P 判断氧化还原锋面（RF = 4.5 或 10 GPa）和碳酸盐 ledge（CL = 2.5 或 3 GPa）。由此 2.5 GPa ≈ 77 km，3 GPa ≈ 93 km，4.5 GPa ≈ 139 km，10 GPa ≈ 309 km。FigS1 v2（`plot_figS1_v2.py`）的压力轴、Fig3 和 Fig4 的锋面虚线都按这个换算（2026-11-22 起；之前按 PREM 取 150 km 和 300 km）。作为对照，PREM 给出 4.5 GPa ≈ 141 km、10 GPa ≈ 304 km，模型初始分层密度（含热膨胀和压缩）给出 145 km、310 km，差别都在 6 km 以内。b 图横轴的 3 GPa 参考深度（脚本中 `Z_REF` = 96.45 km）仍按 PREM，因为它只用于读取文献 1 的等值线。以下为旧版设计：模型锋面画在 150 km 和 300 km：a 里是带标注的白色虚线，b 里是黑色虚线，从 a 的右边界接出并贯穿 b，标注为 4.5 GPa in models 和 10 GPa in models，都左对齐放在各自虚线的下方。深度由脚本里的 `MODEL_FRONTS` 控制，改一处两个 panel 同时变。Fux et al. (2025) 把 5 GPa 写作约 150 km。

**还原端元 4.5 GPa**

- 数据项 1：Fe³⁺/ΣFe 4% 的地幔在 150 ± 50 km 开始氧化还原熔融；3–4% 是与 MORB 源区 fO₂ 相符的常规估计。
- 数据项 6：5 GPa、约 150 km 对应 Fe³⁺/ΣFe 0.04 的地幔的氧化还原锋面。
- 数据项 3：按旧氧逸度计，即使 Fe³⁺/ΣFe 高达约 10%，碳酸盐熔融也只在 <150 km 开始。
- 数据项 7：地幔若在约 250 km 以深金属饱和，碳酸岩熔体只能稳定到 150 km。
- 数据项 2：更还原的太古宙地幔在约 100 km 才开始氧化还原熔融。

**氧化端元 10 GPa**

- 数据项 5：Fe³⁺/ΣFe 约 12% 的地幔在约 300 km 到达缓冲线；>200–250 km 的氧化还原熔融需要地幔柱之类的异常氧化储库。同文测得夏威夷源区比 MORB 源区高约 0.9 个 log 单位。
- 数据项 12：碳酸盐化橄榄岩固相线与洋中脊绝热线相交，熔融最深 330 km。
- 数据项 13：局部氧化的地幔中，含碳硅酸盐熔融的起始深度相当于 X 间断面（270–330 km）。
- 数据项 1：氧化还原熔融比碳酸盐化橄榄岩固相线浅约 150 km，即固相线在约 300 km。
- 数据项 7：上涌地幔中若存在碳酸盐，位温 1400 °C 时熔融在约 300 km 开始。
- Dasgupta & Hirschmann (2010)：碳酸盐化地幔的熔融在 >300 km 开始，含金刚石或含金属地幔的氧化还原熔融更浅。这句话本身就是“氧化深、还原浅”两个端元的表述。
- Eguchi & Dasgupta (2018)：再循环碳的信号要求熔融从 >10 GPa 的碳酸盐饱和条件开始。

**两个端元之间**：模型曲线给出单调关系，Fe³⁺/ΣFe 从 2% 升到 14%，锋面从 83 km 加深到 316 km。数据项 2、3、4、5 各自独立地表明锋面随氧化程度加深。右栏的深度约束多数落在 150–260 km。

**审稿人可能提出的问题**

- 数据项 8、9、10 认为正常上涌地幔的锋面在约 250 km（7–9 GPa），依据是金属饱和深度。数据项 4 和 5 认为现代 MORB 源区的 Fe³⁺/ΣFe 是 5–8% 而不是 3–4%，对应的锋面在 200–250 km。按这些研究，4.5 GPa 代表的是偏还原的一端，不是正常地幔的共识值，行文时建议称为端元。
- 模型曲线自身的深度不确定度约 ±50 km（数据项 1），水的存在还会使锋面加深。

## 6. 背景文献（未画在图上）

**不再画的数据**

- Shahar, G., Fei, Y. & Kessel, R. Melting of carbonate-bearing peridotite as a function of oxygen fugacity: implications for mantle melting beneath mid-ocean ridges. *Contrib. Mineral. Petrol.* **176**, 83 (2021)。3 GPa 下，IW+4.5 时固相线 950 °C，IW+2.5 时 1150 °C。外推后较氧化地幔约 430 km 开始熔融，较还原地幔约 320 km。方向与“越氧化越深”一致，但体系里始终有碳酸盐，测的是固相线而不是石墨/金刚石的氧化。来源：摘要原文。https://doi.org/10.1007/s00410-021-01842-0
- Stagno, V. Carbon, carbides, carbonates and carbonatitic melts in the Earth's interior. *J. Geol. Soc.* **176**, 375–387 (2019)。转述数据项 2 的结果，并指出俯冲带入氧化物质使软流圈 Fe³⁺ 逐渐升高，氧化还原熔融随之加深。来源：开放全文。https://doi.org/10.1144/jgs2018-095

**太古宙地幔氧化状态的争议（与数据项 2 有关）**

- Zhu, X.-X., Duan, W.-Y., Gerya, T. et al. The mantle Fe³⁺/ΣFe ratio has doubled since the early Archean. *Nat. Commun.* **17**, 429 (2026)。来源：摘要原文。https://doi.org/10.1038/s41467-025-66969-1
- Zhang, F., Stagno, V., Zhang, L. et al. The constant oxidation state of Earth's mantle since the Hadean. *Nat. Commun.* **15**, 6521 (2024)。来源：摘要原文。https://doi.org/10.1038/s41467-024-50778-z
- Birner, S. K., Cottrell, E., Davis, F. A. & Warren, J. M. Deep, hot, ancient melting recorded by ultralow oxygen fugacity in peridotites. *Nature* **631**, 801–807 (2024)。来源：摘要原文。https://doi.org/10.1038/s41586-024-07603-w

**地幔氧化程度不均一、存在氧化端元的证据**

- Gao, M., Wang, Y., Foley, S. F. & Xu, Y.-G. Variable mantle redox states driven by deeply subducted carbon. *Sci. Adv.* **11**, eadu4985 (2025)。9–21 GPa 实验：非地幔柱环境以还原为主，碳酸岩熔体被冻结成还原碳；地幔柱环境中碳酸岩熔体超过金属铁的缓冲能力，形成氧化的、含富 CO₂ 熔体的地幔。来源：摘要原文。https://doi.org/10.1126/sciadv.adu4985
- Kempe, Y. et al. Redox state of the deep upper mantle recorded by nickel-rich diamond inclusions. *Nat. Geosci.* **18**, 1048–1055 (2025)。280–470 km 的金刚石中富镍金属与碳酸盐包裹体共存；深部碳酸岩–硅酸盐熔体间歇性地氧化小体积地幔。来源：摘要原文。https://doi.org/10.1038/s41561-025-01791-4
- Tao, R. & Fei, Y. Recycled calcium carbonate is an efficient oxidation agent under deep upper mantle conditions. *Commun. Earth Environ.* **2**, 45 (2021)。来源：摘要原文。https://doi.org/10.1038/s43247-021-00116-8
- Stagno, V., Frost, D. J., McCammon, C. A., Mohseni, H. & Fei, Y. The oxygen fugacity at which graphite or diamond forms from carbonate-bearing melts in eclogitic rocks. *Contrib. Mineral. Petrol.* **169**, 16 (2015)。现代洋壳的全岩 Fe³⁺/ΣFe 较高，俯冲后地壳碳很可能到至少 250 km 仍处于碳酸盐稳定域。来源：摘要原文。https://doi.org/10.1007/s00410-015-1111-1
- Kiseeva, E. S. et al. Oxidized iron in garnets from the mantle transition zone. *Nat. Geosci.* **11**, 144–147 (2018)。镁铁榴石包裹体的 Fe³⁺/ΣFe 从约 240 km 的 0.08 升到约 500 km 的 0.30，氧化剂可能是含碳酸盐的流体或熔体。来源：摘要原文。https://doi.org/10.1038/s41561-017-0055-7
- Nicklas, R. W. et al. Oxidized mantle sources of HIMU- and EM-type ocean island basalts. *Chem. Geol.* **602**, 120901 (2022)。洋岛玄武岩 fO₂ 平均 FMQ+2.0 ± 0.7，同一氧逸度计下 MORB 为 +0.6 ± 0.2。来源：预印本摘要原文。https://doi.org/10.1016/j.chemgeo.2022.120901
- Brounce, M., Stolper, E. & Eiler, J. Redox variations in Mauna Kea lavas, the oxygen fugacity of the Hawaiian plume, and the role of volcanic gases in Earth's oxygenation. *Proc. Natl Acad. Sci. USA* **114**, 8997–9002 (2017)。来源：摘要原文。https://doi.org/10.1073/pnas.1619527114
- Gaillard, F., Scaillet, B., Pichavant, M. & Iacono-Marziano, G. The redox geodynamics linking basalts and their mantle sources through space and time. *Chem. Geol.* **418**, 217–233 (2015)。来源：摘要原文。https://doi.org/10.1016/j.chemgeo.2015.07.030
- Fux, M., Schmidt, M. W. & Liebske, C. The reduced alloy in Earth's upper mantle. *Earth Planet. Sci. Lett.* **645**, 118955 (2024)。来源：**检索摘要转述，需核对**。https://doi.org/10.1016/j.epsl.2024.118955
- Moussallam, Y. et al. Mantle plumes are oxidised. *Earth Planet. Sci. Lett.* **527**, 115798 (2019)。来源：**检索摘要转述，需核对**；Zhang et al. (2024) 引它说明地幔柱是异常氧化储库。https://doi.org/10.1016/j.epsl.2019.115798

**其他**

- Dasgupta & Hirschmann (2010) 的 Fig. 5 是“碳酸盐化固相线”与“氧化还原熔融固相线”两种情形的示意相图，PhaseDiagram.png 的 VAPOR/MELT/SOLID 框架与此类似，可能是 a 图的原始出处，请核对。
- Rohrbach, A. et al. Metal saturation in the upper mantle. *Nature* **449**, 456–458 (2007)。https://doi.org/10.1038/nature06183
- Ghosh, S., Ohtani, E., Litasov, K. D. & Terasaki, H. *Chem. Geol.* **262**, 17–28 (2009)。10–20 GPa 碳酸盐化橄榄岩固相线。https://doi.org/10.1016/j.chemgeo.2008.12.030
- Frost, D. J. & McCammon, C. A. The redox state of Earth's mantle. *Annu. Rev. Earth Planet. Sci.* **36**, 389–420 (2008)。https://doi.org/10.1146/annurev.earth.36.031207.124322
- Foley, S. F. A reappraisal of redox melting in the Earth's mantle as a function of tectonic setting and time. *J. Petrol.* **52**, 1363–1391 (2011)。Aulbach & Stagno (2016) 引它说明 Fe³⁺/ΣFe 越低氧化还原熔融越浅。未读。https://doi.org/10.1093/petrology/egq061
- Cottrell, E. et al. Earth's past and present mantle oxygen fugacity. *Nat. Rev. Earth Environ.* **6**, 728–746 (2025)。未读。https://doi.org/10.1038/s43017-025-00735-1

## 7. 还需要确认的地方

1. **数据项 12（Dasgupta & Hirschmann 2006）**只核对了摘要，200–330 km 的上下限各自对应什么条件没有看正文。
2. **数据项 11 和 14 是否算“氧化还原锋面”**：Hua et al. (2023) 明确说约 260 km 的界面可能是碳促进熔融的起始；Gu et al. (2005) 只说可能与部分熔融有关；Sun & Zhou (2023) 没有做这种解释。保守的做法是只留 Hua 和 Gu，把 14 去掉。
3. **数据项 2 的横向误差棒**是我取的，见第 4 节。
4. **a 图的原始出处**：图注里留了空。
5. **4.5 GPa 与 150 km**：按 PREM，4.5 GPa 是 141 km，150 km 是 4.8 GPa。如果模型里用的就是 4.5 GPa，a 图的虚线可以上移约 9 km，或在图注里写“约 150 km”。
6. Eguchi & Dasgupta (2018) 的卷号取自记忆。

## 8. 编号变更记录

**上一版 b 图 → 本版**

| 上一版 | 本版 | 变化 |
|---|---|---|
| 1 Stagno 2013 | 1 | 加了 4% 处 ±50 km 的误差棒 |
| 2 Stagno 2019 | 2 | 改引原始出处 Aulbach & Stagno 2016 |
| 5 Stagno & Frost 2010（右栏 100–150 km） | 3 | 原文给了 Fe³⁺/ΣFe，移到左侧，画成两个点 |
| 3 Davis & Cottrell 2021 | 4 | 深度由 200–250 改为原文的 200–230 km |
| 4 Zhang 2024 | 5 | 不变 |
| 6 Fux 2025 | 6 | 深度由我换算的 157–246 改为原文的 150–240 km |
| 7 Yaxley 2019 | 7 | 不变 |
| 8 Dasgupta 2013 | 8 | 不变 |
| 10 Schmidt 2026 | 9 | 不变 |
| 11 Rohrbach & Schmidt 2011 | 10 | 不变 |
| 9 地球物理（转引，200–250 km） | 11、14 | 换成核对过的原始文献：约 260 km 间断面；软流圈底界 255 km（180–340） |
| 12 Dasgupta & Hirschmann 2006 | 12 | 不变 |
| — | 13 | 新增：Dasgupta 2013 的局部氧化地幔情形 |

**最早的叠加图** `RedoxFront_constraints.png` 另有一套编号：旧 1 = Shahar 2021，旧 2 = Zhang 2024，旧 3 = Stagno 2013，旧 4 = Dasgupta & Hirschmann 2006，旧 5 = Rohrbach & Schmidt 2011，旧 6 = Dasgupta 2013，旧 7 = Schmidt 2026，旧 8 = 地球物理，旧 9 = Eguchi & Dasgupta 2018。它说明了一点：等 Fe³⁺/ΣFe 线都在石墨/金刚石–碳酸盐边界上与之相交（ΔFMQ 约 −1.8 到 −2.0），到不了 a 图中斜的 “Redox Front ?” 虚线所在的氧化区内部。
