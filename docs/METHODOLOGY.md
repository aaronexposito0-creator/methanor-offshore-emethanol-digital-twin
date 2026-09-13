# MethaNor methodology — V4.2

The web application contains a native visual Methodology section; this file is the repository-readable equivalent.

## 1. Scope and evidence rule

MethaNor is a **conceptual / pre-FEED screening model**. Inputs are tagged as primary/official evidence, academic baseline, scenario assumption or derived result. A scenario value is never silently presented as measured data.

It does not replace class calculations, CFD/RAO analysis, FEA, detailed process simulation, vendor guarantees, environmental assessment, HAZOP, permitting or project-finance due diligence.

## 2. Wind climate

The baseline preserves the thesis mean wind at 150 m (`8.63 m/s`) and Weibull shape factor `k = 2.2` as **academic baseline values**. The scale parameter is recovered from the mean:

```text
c = v_mean / Gamma(1 + 1/k)
```

A production-quality upgrade should ingest multi-year hourly ERA5 data (`S04`) and quantify interannual variability rather than relying on one stationary Weibull fit.

## 3. IEA 15 MW screening power curve

Reference operating envelope (`S01`):

```text
rated power   = 15 MW
rotor         = 240 m
hub height    = 150 m
cut-in        = 3.00 m/s
rated speed   = 10.59 m/s
cut-out       = 25.00 m/s
```

Between cut-in and rated speed MethaNor uses a transparent cubic interpolation in wind power. It is deliberately labelled a screening curve, not OpenFAST/aeroelastic simulation.

```text
E_wind = N_turbines × P_rated × 8760 × CF × availability
```

## 4. Stoichiometric methanol balance

```text
CO2 + 3 H2 -> CH3OH + H2O
```

Molar masses give approximately:

```text
H2 requirement   = 188.75 kg H2 / t MeOH
CO2 requirement  = 1.374 t CO2 / t MeOH
reaction water   = 0.562 t H2O / t MeOH
```

The engine derives these ratios rather than hard-coding a production yield.

## 5. Process electricity / electric-equivalent intensity

Baseline screening values:

```text
PEM                    52.0 kWh/kg H2   [S02 benchmark]
DAC                     0.55 MWh/t CO2  [scenario; S09 context]
MeOH synthesis          0.70 MWh/t MeOH [scenario; S03 context]
Water treatment         0.02 MWh/t MeOH [scenario]
Balance of plant          6% gross demand [scenario]
```

```text
I_total = (I_PEM + I_DAC + I_synthesis + I_water) / (1 - BoP_fraction)
MeOH_annual = E_wind / I_total
```

This energy-limited formulation is the central physical constraint in MethaNor.

## 6. Scientific correction to the thesis

A 15 MW source has an absolute annual electricity ceiling:

```text
15 MW × 8760 h = 131.4 GWh/y
```

At 52 kWh/kg H2, electrolysis stoichiometry alone requires about 9.82 MWh/t-MeOH. Even before DAC, synthesis, water treatment and availability losses, 51,058 t/y is therefore impossible from a single 15 MW electrical source.

MethaNor preserves the **15 MW semisubmersible unit** as the engineering reference and moves commercial ~50 kt/y scale to a **multi-unit / ~150 MW hub**.

## 7. Naval baseline

Inherited thesis values (`S10`) are design-reference inputs, not class-validated values:

```text
Displacement        24,000 t
Operating draft      22.0 m
Main-deck air gap     24.5 m
GMeff                  3.13 m
Academic Hs,50         11.0 m
```

Hub height is additionally supported by the IEA/NREL reference turbine (`S01`). Site-specific metocean should be refreshed from ERA5 / Puertos del Estado and bathymetry from EMODnet before engineering use.

## 8. Finance model

Base scenario:

```text
Gross CAPEX             1,000 M€
Annual OPEX                 33 M€/y
Methanol price            1,200 €/t
CAPEX grant                  40%
WACC                          8%
Operating life               25 y
Annual production decay      0.5%
Terminal decommissioning       3% of gross CAPEX
```

The DCF is intentionally **COD-normalized** for screening: net CAPEX is placed at year 0 rather than pretending the conceptual 60-month construction schedule is already a bankable financing drawdown.

```text
CAPEX_net = CAPEX_gross × (1 - grant)
Production_y = Production_1 × (1 - degradation)^(y-1)
FCF_y = Production_y × price - OPEX
FCF_25 = FCF_25 - decommissioning allowance
NPV = -CAPEX_net + sum(FCF_y / (1 + WACC)^y)
```

IRR is solved numerically by bisection. Simple payback uses undiscounted cumulative cashflow and interpolates within the crossing year.

## 9. LCOeM

```text
LCOeM = [CAPEX_net + PV(OPEX) + PV(decommissioning)] / PV(MeOH production)
```

Taxes, debt sculpting, working capital, replacement reserves, oxygen revenues and detailed inflation/escalation are outside this screening model.

## 10. Break-even solver

MethaNor V4.2 solves `NPV(x) = 0` by bisection for:

- methanol price;
- maximum gross CAPEX;
- minimum CAPEX grant;
- mean wind resource, if a root exists inside the tested domain;
- maximum WACC.

If the chosen variable alone cannot make the project cross zero in a physically/reasonably bounded search interval, the solver returns **not reachable** rather than extrapolating a fictitious value.

## 11. Build & operations

The 60-month Gantt, CAPEX S-curve, phase staffing, operating roles, salary values, two planned campaign windows and remote-first operating concept are **author scenario assumptions** for portfolio demonstration. They are deliberately not represented as vendor, yard or operator quotations.

## 12. Site-intelligence upgrade path

The bundled map is a screening UI, not a GIS permitting product.

- ERA5 (`S04`) → hourly wind and wave time series.
- EMODnet Bathymetry (`S05`) → depth, DTM and coastline.
- MITECO POEM (`S06`) → official maritime spatial-planning intersection.
- Puertos del Estado (`S07`) → measured/forecast Spanish metocean validation.

No current candidate score is a permitting conclusion.


## 13. Technology & Vendor Explorer

The V4.2 technology catalogue is a **screening shortlist**, not a procurement recommendation. Public manufacturer information is normalized into a common structure for electrolysis, methanol synthesis, direct-air capture and water treatment.

The portfolio-fit score is intentionally transparent and bounded to 0–100. It combines normalized sub-scores for:

```text
scale / modularity
operational dynamics
commercial maturity
integration / offshore suitability
pressure or process-integration relevance
quality of public evidence
```

The exact component weights are stored with each candidate in `data/technology_catalog.json`. A high score therefore means “fits this conceptual portfolio architecture under the visible criteria”, not “best supplier in the market”.

**Commercial discipline:** public product pages are not interpreted as quotations. If a supplier does not publish a project price, the UI states `vendor quote required`. Literature CAPEX ranges, when used elsewhere, remain separate scenario assumptions.

A candidate can always be selected for **configuration traceability**. A numerical model input is altered only when a compatible public value is actually present. The current release allows a public electrolyzer specific-energy value to update the PEM intensity; unsupported methanol/DAC performance numbers are deliberately not invented.

## 14. Interactive geographic screening

The V4.2 map uses real WGS84 coordinates and Web-Mercator basemap tiles. Basemaps are **visual context only**.

For known candidate points, the UI displays the provenance-labelled values stored in `data/sites.json`. For an arbitrary map click, MethaNor computes only:

- the clicked latitude/longitude;
- great-circle distance to the bundled reference ports;
- an explicitly labelled inverse-distance preview of bundled anchor values for UI exploration.

That preview is **not** ERA5, EMODnet or a permitting result. The interface links directly to ERA5, EMODnet, POEM and Google Maps so the user can trace what would be required for a professional refresh.

No statement such as “shipping traffic is excessive”, “protected area conflict” or “site is impossible” is produced unless the corresponding GIS/AIS evidence is actually embedded.

## 15. Mass & space budget

`data/mass_space.json` reconstructs the academic thesis weight register. The registered values close to:

```text
Total mass              24,000 t
Vertical moment        505,757 t·m
Derived KG              21.073 m
```

This is an **academic mass model**, not a class-approved lightweight/deadweight report. Known thesis equipment footprints are also exposed against reference deck envelopes so technology choices remain visibly connected to naval integration.

## 16. Concept risk register

The 5×5 matrix uses:

```text
Risk score = probability (1…5) × impact (1…5)
```

It is a portfolio prioritization tool, **not a HAZID/HAZOP**. Risks carry bilingual descriptions, owners, mitigations and evidence status. Several scores respond to current scenario choices only where the directional relationship is defensible.

## 17. Scenario comparison and design decisions

A/B/C snapshots are stored in browser local storage and compare the current physical/economic outputs without changing the core equations. The design-decision log records rationale, alternatives, trade-offs and evidence IDs for the major architectural choices. Together, these features turn the app from a one-output calculator into a traceable concept-selection tool.
