# MethaNor V4.2 — publication release QA

This release is packaged as a static, bilingual portfolio application. The final gate is deliberately split between **automated correctness** and **normal-browser visual acceptance**.

## Linguistic publication gate

V4.2 is intentionally a **copy-only publication QA release**. No equations, numerical assumptions, score weights, engineering datasets, financial logic or interaction model were changed. The pass standardizes technical Spanish, removes residual Spanglish where a clear Spanish engineering term exists, tightens public-facing English phrasing and preserves established sector terms only where they improve precision.

Static HTML coverage was checked against the EN→ES translation registry; all long-form interface copy has a Spanish mapping, with only units, equations, proper names and the bilingual JavaScript fallback intentionally exempt. Spanish JSON metadata was separately scanned for residual `baseline / input / gate / solver / long-lead / performance / GIS` wording.

## Automated release checks

**Final release gate:** `34 passed` with `python -m pytest -q`; `node --check assets/app.js` passes; the Python reference engine regenerates `data/baseline.json` successfully and the full test suite still passes afterwards.

- Python scientific/reference engine regenerates `data/baseline.json` deterministically.
- Unit and repository tests validate wind integration, energy/material balances, financial monotonicity, break-even solvers and source traceability.
- The 24,000 t academic mass register and 505,757 t·m vertical moment reconcile.
- Named vendor candidates contain public manufacturer/source links and no fabricated commercial price field.
- A/B/C technology comparison and scenario export are present in the final UI model.
- Site labels and arbitrary clicked points support EN/ES independently of the language used when the point was created.
- HTML has unique IDs, valid internal anchors and no missing local runtime assets.
- All bundled JSON files parse successfully.
- `assets/app.js` passes the Node syntax gate.

## Map UX correction

The final release fixes the clicked-point offset visible in the earlier build. The marker itself now has a fixed 30×30 px coordinate box; labels are absolutely positioned and therefore cannot move the geographic point. Arbitrary clicked points show their label only on hover/focus, so the pointer no longer lands over a permanent text label. `Center selection` and `Copy coordinates` are also available in the selected-site actions.

## Visual acceptance boundary

Automated browser navigation is blocked by the packaging environment policy, so pixel-level rendering cannot be asserted from headless automation here. The release therefore does **not** claim automated visual certification. The supplied normal-browser screenshots were used as the visual baseline, while the final changes are protected by static structure/style/interaction tests.

## Engineering boundary

Passing the QA gates does not turn the concept into class-approved, permit-ready or bankable engineering. CFD/RAO, global FEA/fatigue, mooring dynamics, hazardous-area studies, official GIS intersections, environmental assessment and vendor guarantees remain explicit future gates.
