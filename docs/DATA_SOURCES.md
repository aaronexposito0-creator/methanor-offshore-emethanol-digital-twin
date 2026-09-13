# Data sources and evidence governance

The application source register is canonical: `data/sources.json`. It maps each source to the variables and modules it supports.

## Primary / official references

- **S01 — NREL / IEA Wind TCP:** IEA 15 MW reference turbine geometry and operating envelope.
- **S02 — U.S. DOE:** PEM electrolysis system efficiency, lifetime and cost targets.
- **S03 — IRENA & Methanol Institute:** renewable methanol pathway and cost/process context.
- **S04 — Copernicus / ECMWF ERA5:** target wind/wave reanalysis source.
- **S05 — EMODnet Bathymetry:** target bathymetric DTM and coastline source.
- **S06 — MITECO POEM:** official Spanish maritime-spatial-planning source.
- **S07 — Puertos del Estado:** measured/forecast oceanographic validation source.
- **S08 — NREL ATB 2024:** offshore-wind techno-economic reference and uncertainty framing.
- **S09 — IEA Direct Air Capture 2022:** DAC maturity, energy and cost context.

## Academic baseline

- **S10 — 2026 Universidad de Cantabria thesis:** concept origin and naval/site baseline. MethaNor never automatically promotes a thesis value to primary evidence.

## Current repository data policy

No raw ERA5, EMODnet, POEM or Puertos datasets are redistributed. The current candidate-site table is a portfolio UI dataset containing one academic reference point and three explicitly illustrative comparison points.


## Technology / vendor evidence — V4.2

`data/sources.json` also includes official technical pages used by the Technology & Vendor Explorer. The catalogue covers public information from suppliers including Siemens Energy, Nel, ITM Power, thyssenkrupp nucera, Sunfire, Plug Power, John Cockerill, Enapter, Topsoe, Johnson Matthey and several DAC/water-technology providers.

These sources support **public technical attributes and technology context only**. They are not treated as project quotations, performance guarantees or supplier endorsements.

## Basemap policy

- **S32 — OpenStreetMap:** standard map-tile context and attribution.
- **S33 — Esri World Imagery:** satellite/aerial visual context and attribution.

Basemap pixels are never used as engineering measurements. Wind, depth, shipping density, environmental constraints and permitting status require their own cited datasets.

## Site-data honesty rule

The current repository does not redistribute raw ERA5, EMODnet, POEM, Puertos or AIS data. An arbitrary map click can therefore provide coordinates, nearest-port geometry and a labelled interpolation preview, but it cannot honestly claim local wind, water depth, vessel traffic or permitting feasibility from the basemap itself.
