# Assumption governance

MethaNor uses a deliberately strict assumption policy.

## Evidence classes

### A — Primary / official
Values anchored to a technical report, government target, official observation or official spatial dataset.

### B — Academic baseline
Values inherited from the original thesis. They are useful as a design reference but must survive an independent engineering audit before being upgraded to Class A.

### C — Scenario assumption
Editable commercial, organisational or planning values used to explore sensitivity. They are never presented as observed facts.

## Base scenario

| Variable | Base | Class | Note |
|---|---:|:---:|---|
| Turbine | 15 MW | A | IEA/NREL reference |
| Mean wind at hub | 8.63 m/s | B | thesis baseline; refresh from ERA5 |
| Weibull k | 2.2 | B | thesis/model assumption |
| Availability | 94% | C | screening scenario |
| PEM intensity | 52 kWh/kg H2 | A/C | DOE target anchor, editable |
| DAC energy equivalent | 0.55 MWh/tCO2 | C | screening assumption |
| Synthesis electricity | 0.70 MWh/tMeOH | C | screening assumption |
| BoP fraction | 6% | C | screening assumption |
| Gross hub CAPEX | 1,000 M€ | B/C | thesis hub baseline, high uncertainty |
| Hub OPEX | 33 M€/y | B/C | thesis baseline, high uncertainty |
| MeOH sale price | 1,200 €/t | C | offtake scenario |
| Grant | 40% | C | policy scenario |
| WACC | 8% | C | finance scenario |
| Life | 25 y | B/C | thesis / offshore design framing |

The UI makes the high-uncertainty values easy to change because the correct scientific behaviour is sensitivity, not false precision.
