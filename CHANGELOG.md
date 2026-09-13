# Changelog

## 4.2.0 — Publication Linguistic QA

- Performed a final EN/ES copy-only QA pass with no new product functionality.
- Replaced residual Spanglish in the Spanish interface (baseline/input/gate/solver/long-lead/performance) with clearer engineering Spanish while retaining established sector terms where useful.
- Tightened scientific wording in the public-facing interface, including the 15 MW energy-consistency check and vendor-quotation language.
- Improved terminology consistency across site, platform, build/operations, methodology, risk and evidence views.
- Updated release metadata and scenario-export version to V4.2.

## 4.1.0 — Final Bilingual & Evidence Polish

- Completed EN/ES polish across static copy, vendor-detail fields, risk categories and source descriptions.
- Added visible Portfolio Fit score methodology with six weighted criteria and a non-procurement disclaimer.
- Added source-date governance: dated references retain publication/reference year while live technical pages are explicitly shown with access date.
- Improved source registry rendering in Spanish without translating official product/report titles unless a project-native Spanish title exists.
- Removed a duplicate break-even helper and added regression tests for versioning, bilingual metadata, score weights and source-date governance.
- Updated release metadata, citation information and scenario export to V4.1.

## 4.0.0 — Final Portfolio Release

- Fixed map-marker anchoring so the geographic point stays exactly under the selected coordinate regardless of label width.
- Replaced the permanent custom-point label with an unobtrusive hover/focus tooltip.
- Added **Center selection** and **Copy coordinates** controls to the site panel.
- Added an executive decision snapshot that separates physics, site-screening status, technology evidence and scenario-dependent finance.
- Added **A/B/C technology comparison** with side-by-side public specifications and explicit blanks for unavailable vendor data.
- Technology comparison is category-consistent and persisted locally.
- Scenario export upgraded to V4 and now includes technology-selection and technology-comparison state.
- Added V4 repository tests and root-level pytest configuration.
- Performed JavaScript syntax validation, Python test validation, JSON/invariant checks and static HTML/link integrity checks. Browser rendering was additionally reviewed from the supplied normal-browser screenshots; automated browser navigation is blocked in the packaging environment.

## 3.0.0 — Technology & Site Intelligence

- Added persistent English / Spanish interface.
- Replaced the illustrative site-only graphic with an interactive geographic map using real coordinates, satellite/map basemaps, zoom/pan, arbitrary point selection and direct Google Maps links.
- Added explicit ERA5, EMODnet and POEM source links and data-gap warnings for AIS shipping, protected areas and permitting layers.
- Added Technology & Vendor Explorer with 10 electrolysis candidates and additional methanol-synthesis, DAC and water-treatment candidates.
- Added transparent portfolio-fit scoring, official manufacturer/datasheet links and strict vendor-price discipline.
- Added per-category technology configuration; numerical scenario inputs are changed only when a public supported value exists.
- Added thesis-derived 24,000 t mass / 505,757 t·m vertical-moment register and space-budget view.
- Added 5×5 concept risk matrix and detailed risk register.
- Added A/B/C scenario comparison stored locally in the browser.
- Added design-decision log with rationale, alternatives, trade-offs and evidence references.
- Expanded the evidence registry to technology suppliers and basemap provenance.
- Expanded automated validation and repository-integrity checks.

## 2.0.0 — portfolio-quality rebuild

- Replaced raw Markdown navigation with native Methodology and Project Origin sections.
- Added evidence-class labels and searchable source registry.
- Rebuilt site explorer with bathymetry/port context and transparent score methodology.
- Added detailed semisubmersible side/plan views and P2X module layout.
- Added 60-month delivery plan, CAPEX S-curve, phase staffing and O&M lifecycle.
- Extended finance engine with terminal decommissioning and explicit COD-normalized DCF scope.
- Added break-even solvers for MeOH price, CAPEX, grant, wind and WACC.
- Added detailed CAPEX/OPEX allocation and improved sensitivity analysis.
- Added architecture diagram and expanded README/methodology/validation documentation.

## 1.0.0

- Initial MethaNor concept release.
