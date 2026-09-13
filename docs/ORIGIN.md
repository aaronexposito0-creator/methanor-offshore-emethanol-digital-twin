# Academic origin — MethaNor

The web application contains a native **Project Origin** section so portfolio visitors are never sent to raw Markdown. This file preserves the same story for repository readers.

MethaNor is an independent software evolution of the 2026 BSc Marine Engineering thesis by **Aarón Expósito Monar**, Universidad de Cantabria:

**“Diseño conceptual multidisciplinar y viabilidad tecno-económica de una plataforma semisumergible P2X de 15 MW para la síntesis de e-Metanol en el Mar Cantábrico.”**

## Preserved concept

The original academic work combined:

- a Cantabrian offshore reference location;
- the IEA/NREL 15 MW offshore reference turbine;
- PEM electrolysis, direct-air capture, water treatment and methanol synthesis;
- an 8,760-hour P2X concept;
- a semisubmersible baseline with 24,000 t displacement, 22 m draft, 24.5 m air gap and GMeff 3.13 m;
- a multi-unit commercial hub framing;
- CAPEX/OPEX and 25-year financial scenarios.

## Why the software version is not a copy of the thesis

MethaNor treats the thesis as a **starting hypothesis**, not as professional engineering. Every inherited value is re-labelled by evidence quality and key equations are recomputed independently.

### What changed

1. Energy conservation is enforced before e-methanol production is calculated.
2. The 15 MW engineering unit and 150 MW commercial hub are explicitly separated.
3. Financial results are regenerated from the current physical scenario rather than copied from thesis headline values.
4. Site inputs are provenance-labelled and linked to an ERA5/EMODnet/POEM/Puertos upgrade path.
5. Construction, O&M and commercial values are openly labelled as scenario assumptions.
6. The same conceptual equations are implemented independently in Python and browser JavaScript.
7. Automated tests cover physical bounds, finance monotonicity, break-even behaviour and repository integrity.
8. Methodology and origin are native app sections rather than raw-document links.

## Key scientific correction

A single 15 MW source has a maximum of 131.4 GWh/y at 100% capacity factor. The hydrogen required by 51,058 t/y of methanol alone exceeds that electrical budget under the PEM intensity used in the project. MethaNor therefore keeps the 15 MW naval unit but assigns ~50 kt/y commercial production to the multi-unit hub.

The correction is not presented as criticism of the academic concept. It is the reason the portfolio project is valuable: it shows how a concept can be revisited, audited and improved when new engineering/data skills are applied.
