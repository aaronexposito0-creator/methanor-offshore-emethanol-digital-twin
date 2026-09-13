# Validation report — MethaNor V4.2

Validation is intentionally split into four layers.

## 1. Physics / calculation tests

`tests/test_engine.py` checks:

- physical Weibull capacity-factor range;
- process-energy conservation;
- stoichiometric mass balance;
- production monotonicity with available energy;
- the 15 MW / 51,058 t/y impossibility bound;
- grant and WACC finance monotonicity;
- terminal decommissioning treatment;
- break-even price reproducing NPV ≈ 0;
- honest `None` when wind-resource improvement alone cannot reach NPV = 0 inside the tested domain;
- CAPEX/OPEX/construction share closure.

## 2. Repository integrity

`tests/test_repository.py` checks required files, source-traceability fields, native app links for Methodology/Origin and zero external runtime-CDN dependencies.

## 3. Browser parity

The JavaScript engine mirrors the Python equations for:

- Weibull wind integration;
- process intensity;
- stoichiometric mass balance;
- 25-year DCF;
- LCOeM;
- IRR and payback;
- break-even solvers.

`node --check assets/app.js` is used as a syntax gate.

## 4. V4.2 data / UI integrity

`tests/test_v4.py` checks the final catalogue, map controls, technology comparison and thesis-derived integration data, including:

- technology-category coverage and ten electrolysis candidates;
- official manufacturer/source-link presence;
- strict absence of fabricated vendor price fields;
- 24,000 t mass closure and 505,757 t·m vertical-moment closure;
- derived KG consistency;
- risk-register structure and 1–5 probability/impact bounds;
- required V4.2 DOM anchors and language/map/technology features.

A static HTML parse also checks for duplicate IDs and required application anchors. `node --check assets/app.js` is the JavaScript syntax gate. Visual acceptance should still be performed in a normal desktop/mobile browser because pixel-level rendering is browser/environment dependent.

## Boundary

Passing these tests does **not** validate class, CFD/RAO, FEA, detailed process simulation, GIS permitting or vendor performance. Those remain explicit pre-FEED/FEED upgrade gates.


## Current V4.2 validation target

The final V4.2 package passes the Python test suite, JavaScript syntax validation, JSON parsing/invariants, HTML duplicate-ID checks, internal-anchor checks and local-asset integrity checks. Pixel-level rendering remains a normal-browser acceptance step because the execution environment used for packaging blocks automated browser navigation by policy.

For the final packaging checklist and the map-offset correction, see [`FINAL_QA.md`](FINAL_QA.md).
