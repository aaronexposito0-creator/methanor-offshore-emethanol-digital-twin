# Interview cheat sheet

## 30-second explanation

“MethaNor is a software evolution of my Marine Engineering thesis. I rebuilt the offshore e-methanol concept as an auditable digital twin so every physical and financial assumption is executable. The most important result was actually a correction: an energy audit showed that the original 51 kt/y production could not belong to one 15 MW turbine. I separated the 15 MW engineering unit from a 150 MW commercial hub, closed the mass and energy balances, rebuilt the project-finance model and exposed the assumptions through an interactive scenario lab.”

## What demonstrates engineering maturity

- Energy conservation before presentation.
- Explicit stoichiometry and process intensity.
- Separation of sourced evidence from assumptions.
- No claim of FEED/class validity.
- Site screening is not confused with permitting.
- Financial outputs are recalculated from the physical model.

## What demonstrates data/software maturity

- Independent Python and browser implementations.
- Unit tests for physics and finance monotonicity.
- Source registry and assumption governance.
- Portable static frontend with no web-framework dependency.
- Bilingual UI and exportable scenarios.
- Real-coordinate interactive map with explicit GIS data gaps instead of fabricated conclusions.
- Technology/vendor explorer that separates public specifications from commercial quotations.
- Thesis-derived mass budget, concept risk matrix and A/B/C decision comparison.

## Known limitations

- No real ERA5 ingestion bundled yet; arbitrary-point wind/depth previews are explicitly interpolation-only.
- No POEM polygon intersection or licensed AIS-density layer bundled yet.
- No RAO/CFD/FEA or mooring dynamics.
- No detailed tax/debt/offtake model.
- CAPEX/OPEX are screening values, not vendor bids.

Being able to state those limitations clearly is part of the project, not a weakness to hide.


## Portfolio talking point — technology selection

“I deliberately did not create a fake ‘top ten best suppliers’ table. The app ranks fit against visible criteria and links to official technical pages. If a public value is robust enough, it can update the scenario; otherwise the supplier is only recorded as a configuration choice. Vendor price always remains ‘quote required’ unless there is a real public quotation.”

## Portfolio talking point — map

“The map is geographic, but I separate basemap context from engineering data. Clicking a coordinate can calculate geometry such as nearest-port distance, while wind, bathymetry, POEM, AIS and environmental constraints remain explicit upgrade layers. I preferred an honest data gap over pretending satellite imagery proves site feasibility.”
