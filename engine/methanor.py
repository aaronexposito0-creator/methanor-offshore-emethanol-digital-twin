from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from math import exp, gamma
from pathlib import Path
import json
from typing import Callable, Iterable

HOURS_PER_YEAR = 8760
KG_PER_TONNE = 1000.0

# Stoichiometry: CO2 + 3 H2 -> CH3OH + H2O
H2_KG_PER_T_MEOH = 6.048 / 32.042 * KG_PER_TONNE
CO2_T_PER_T_MEOH = 44.0095 / 32.042
WATER_T_PER_T_MEOH = 18.01528 / 32.042
O2_T_PER_T_H2 = 7.936


@dataclass(frozen=True)
class Turbine:
    rated_mw: float = 15.0
    rotor_diameter_m: float = 240.0
    hub_height_m: float = 150.0
    cut_in_ms: float = 3.0
    rated_ms: float = 10.59
    cut_out_ms: float = 25.0


@dataclass(frozen=True)
class ProcessAssumptions:
    pem_kwh_per_kg_h2: float = 52.0
    dac_mwh_per_tco2: float = 0.55
    synthesis_mwh_per_tmeoh: float = 0.70
    water_mwh_per_tmeoh: float = 0.02
    balance_of_plant_fraction: float = 0.06


@dataclass(frozen=True)
class FinanceAssumptions:
    gross_capex_meur: float = 1000.0
    annual_opex_meur: float = 33.0
    methanol_price_eur_t: float = 1200.0
    capex_grant_fraction: float = 0.40
    wacc: float = 0.08
    lifetime_years: int = 25
    annual_degradation: float = 0.005
    decommissioning_fraction_gross_capex: float = 0.03


CAPEX_SHARES = {
    "floating_wind": 0.41,
    "p2x_process": 0.27,
    "hull_topside": 0.13,
    "mooring_export": 0.08,
    "engineering_owner": 0.07,
    "contingency": 0.04,
}

OPEX_SHARES = {
    "marine_maintenance": 0.31,
    "process_maintenance": 0.25,
    "logistics_campaigns": 0.17,
    "personnel_remote_ops": 0.12,
    "insurance_compliance": 0.09,
    "data_telecoms_other": 0.06,
}

CONSTRUCTION_PROFILE = [0.06, 0.17, 0.28, 0.31, 0.18]  # 5-year conceptual S-curve, sums to 1


def weibull_scale_from_mean(mean_ms: float, k: float) -> float:
    if mean_ms <= 0 or k <= 0:
        raise ValueError("mean wind and Weibull k must be positive")
    return mean_ms / gamma(1.0 + 1.0 / k)


def weibull_pdf(v: float, k: float, c: float) -> float:
    if v < 0:
        return 0.0
    if v == 0 and k < 1:
        return 0.0
    return (k / c) * (v / c) ** (k - 1.0) * exp(-((v / c) ** k))


def turbine_power_mw(v: float, turbine: Turbine = Turbine()) -> float:
    """Transparent screening curve, not an OpenFAST/aeroelastic controller."""
    if v < turbine.cut_in_ms or v >= turbine.cut_out_ms:
        return 0.0
    if v >= turbine.rated_ms:
        return turbine.rated_mw
    numerator = v**3 - turbine.cut_in_ms**3
    denominator = turbine.rated_ms**3 - turbine.cut_in_ms**3
    return turbine.rated_mw * max(0.0, min(1.0, numerator / denominator))


def capacity_factor(mean_wind_ms: float, k: float, turbine: Turbine = Turbine()) -> float:
    c = weibull_scale_from_mean(mean_wind_ms, k)
    step = 0.025
    expectation = probability = 0.0
    v = 0.0
    while v <= 40.0:
        pdf = weibull_pdf(v, k, c)
        expectation += turbine_power_mw(v, turbine) * pdf * step
        probability += pdf * step
        v += step
    if probability <= 0:
        raise RuntimeError("invalid Weibull integration")
    return max(0.0, min(1.0, expectation / probability / turbine.rated_mw))


def annual_wind_energy_mwh(
    turbine_count: int,
    mean_wind_ms: float,
    weibull_k: float,
    availability: float,
    turbine: Turbine = Turbine(),
) -> float:
    if turbine_count <= 0:
        raise ValueError("turbine_count must be positive")
    if not 0 < availability <= 1:
        raise ValueError("availability must lie in (0, 1]")
    return turbine_count * turbine.rated_mw * HOURS_PER_YEAR * capacity_factor(mean_wind_ms, weibull_k, turbine) * availability


def process_energy_mwh_per_t_meoh(process: ProcessAssumptions) -> dict[str, float]:
    if not 0 <= process.balance_of_plant_fraction < 0.5:
        raise ValueError("balance_of_plant_fraction must be in [0, 0.5)")
    pem = H2_KG_PER_T_MEOH * process.pem_kwh_per_kg_h2 / 1000.0
    dac = CO2_T_PER_T_MEOH * process.dac_mwh_per_tco2
    subtotal = pem + dac + process.synthesis_mwh_per_tmeoh + process.water_mwh_per_tmeoh
    total = subtotal / (1.0 - process.balance_of_plant_fraction)
    return {
        "pem": pem,
        "dac": dac,
        "synthesis": process.synthesis_mwh_per_tmeoh,
        "water": process.water_mwh_per_tmeoh,
        "balance_of_plant": total - subtotal,
        "subtotal": subtotal,
        "total_with_bop": total,
    }


def annual_meoh_from_energy(energy_mwh: float, process: ProcessAssumptions) -> float:
    return max(0.0, energy_mwh) / process_energy_mwh_per_t_meoh(process)["total_with_bop"]


def material_balance(meoh_t: float) -> dict[str, float]:
    h2_t = meoh_t * H2_KG_PER_T_MEOH / KG_PER_TONNE
    return {
        "methanol_t": meoh_t,
        "hydrogen_t": h2_t,
        "co2_t": meoh_t * CO2_T_PER_T_MEOH,
        "reaction_water_t": meoh_t * WATER_T_PER_T_MEOH,
        "oxygen_byproduct_t": h2_t * O2_T_PER_T_H2,
    }


def npv_meur(initial_meur: float, annual_cashflows_meur: Iterable[float], wacc: float) -> float:
    return -initial_meur + sum(cf / ((1.0 + wacc) ** year) for year, cf in enumerate(annual_cashflows_meur, start=1))


def irr(initial_meur: float, annual_cashflows_meur: list[float]) -> float | None:
    low, high = -0.99, 2.0

    def f(rate: float) -> float:
        return npv_meur(initial_meur, annual_cashflows_meur, rate)

    fl, fh = f(low), f(high)
    if fl * fh > 0:
        return None
    for _ in range(180):
        mid = (low + high) / 2.0
        fm = f(mid)
        if abs(fm) < 1e-10:
            return mid
        if fl * fm <= 0:
            high, fh = mid, fm
        else:
            low, fl = mid, fm
    return (low + high) / 2.0


def finance_model(production_t: float, finance: FinanceAssumptions) -> dict:
    if finance.gross_capex_meur < 0 or finance.annual_opex_meur < 0:
        raise ValueError("CAPEX and OPEX must be non-negative")
    if not 0 <= finance.capex_grant_fraction < 1:
        raise ValueError("grant fraction must lie in [0,1)")
    if finance.lifetime_years <= 0:
        raise ValueError("lifetime_years must be positive")

    net_capex = finance.gross_capex_meur * (1.0 - finance.capex_grant_fraction)
    cashflows: list[float] = []
    production_series: list[float] = []
    revenue_series: list[float] = []
    cumulative = -net_capex
    cumulative_series = [cumulative]
    payback_year: float | None = None

    for year in range(1, finance.lifetime_years + 1):
        production_y = production_t * ((1.0 - finance.annual_degradation) ** (year - 1))
        revenue = production_y * finance.methanol_price_eur_t / 1_000_000.0
        net_cf = revenue - finance.annual_opex_meur
        if year == finance.lifetime_years:
            net_cf -= finance.gross_capex_meur * finance.decommissioning_fraction_gross_capex
        production_series.append(production_y)
        revenue_series.append(revenue)
        cashflows.append(net_cf)
        previous = cumulative
        cumulative += net_cf
        cumulative_series.append(cumulative)
        if payback_year is None and cumulative >= 0 and net_cf > 0:
            payback_year = (year - 1) + max(0.0, min(1.0, -previous / net_cf))

    project_npv = npv_meur(net_capex, cashflows, finance.wacc)
    project_irr = irr(net_capex, cashflows)
    pv_opex = sum(finance.annual_opex_meur / ((1 + finance.wacc) ** y) for y in range(1, finance.lifetime_years + 1))
    pv_decom = finance.gross_capex_meur * finance.decommissioning_fraction_gross_capex / ((1 + finance.wacc) ** finance.lifetime_years)
    pv_prod = sum(v / ((1 + finance.wacc) ** y) for y, v in enumerate(production_series, start=1))
    lco_meoh = (net_capex + pv_opex + pv_decom) * 1_000_000 / max(pv_prod, 1e-9)

    return {
        "net_capex_meur": net_capex,
        "year1_revenue_meur": revenue_series[0] if revenue_series else 0.0,
        "year1_net_cashflow_meur": cashflows[0] if cashflows else 0.0,
        "npv_meur": project_npv,
        "irr": project_irr,
        "simple_payback_year": payback_year,
        "lco_meoh_eur_t": lco_meoh,
        "cashflows_meur": cashflows,
        "cumulative_cashflow_meur": cumulative_series,
        "production_t": production_series,
        "revenue_meur": revenue_series,
        "decommissioning_meur": finance.gross_capex_meur * finance.decommissioning_fraction_gross_capex,
    }


def _bisect_root(fn: Callable[[float], float], low: float, high: float, *, iterations: int = 100) -> float | None:
    fl, fh = fn(low), fn(high)
    if not (fl <= 0 <= fh or fh <= 0 <= fl):
        return None
    for _ in range(iterations):
        mid = (low + high) / 2.0
        fm = fn(mid)
        if abs(fm) < 1e-7:
            return mid
        if fl * fm <= 0:
            high, fh = mid, fm
        else:
            low, fl = mid, fm
    return (low + high) / 2.0


def break_even_analysis(
    *,
    turbine_count: int,
    mean_wind_ms: float,
    weibull_k: float,
    availability: float,
    process: ProcessAssumptions,
    finance: FinanceAssumptions,
    turbine: Turbine = Turbine(),
) -> dict[str, float | None]:
    def production(mean: float = mean_wind_ms) -> float:
        energy = annual_wind_energy_mwh(turbine_count, mean, weibull_k, availability, turbine)
        return annual_meoh_from_energy(energy, process)

    prod = production()

    price = _bisect_root(
        lambda value: finance_model(prod, replace(finance, methanol_price_eur_t=value))["npv_meur"],
        0.0,
        5000.0,
    )
    capex = _bisect_root(
        lambda value: finance_model(prod, replace(finance, gross_capex_meur=value))["npv_meur"],
        1.0,
        5000.0,
    )
    grant = _bisect_root(
        lambda value: finance_model(prod, replace(finance, capex_grant_fraction=value))["npv_meur"],
        0.0,
        0.95,
    )
    wind = _bisect_root(
        lambda value: finance_model(production(value), finance)["npv_meur"],
        4.0,
        14.0,
    )
    wacc = _bisect_root(
        lambda value: finance_model(prod, replace(finance, wacc=value))["npv_meur"],
        0.001,
        0.35,
    )
    return {
        "methanol_price_eur_t": price,
        "gross_capex_meur": capex,
        "grant_fraction": grant,
        "mean_wind_ms": wind,
        "wacc": wacc,
    }


def scientific_audit_single_15mw(process: ProcessAssumptions = ProcessAssumptions()) -> dict[str, float]:
    max_energy = 15.0 * HOURS_PER_YEAR
    minimum_energy_intensity = H2_KG_PER_T_MEOH * process.pem_kwh_per_kg_h2 / 1000.0
    return {
        "max_electricity_mwh": max_energy,
        "max_meoh_t_electrolysis_only": max_energy / minimum_energy_intensity,
        "max_meoh_t_full_process": max_energy / process_energy_mwh_per_t_meoh(process)["total_with_bop"],
    }


def build_baseline() -> dict:
    turbine = Turbine()
    process = ProcessAssumptions()
    finance = FinanceAssumptions()
    mean_wind = 8.63
    k = 2.2
    availability = 0.94
    turbine_count = 10

    cf = capacity_factor(mean_wind, k, turbine)
    wind_mwh = annual_wind_energy_mwh(turbine_count, mean_wind, k, availability, turbine)
    meoh_t = annual_meoh_from_energy(wind_mwh, process)
    finances = finance_model(meoh_t, finance)
    breaks = break_even_analysis(
        turbine_count=turbine_count,
        mean_wind_ms=mean_wind,
        weibull_k=k,
        availability=availability,
        process=process,
        finance=finance,
        turbine=turbine,
    )
    return {
        "engine": "MethaNor conceptual screening engine v4.0",
        "scope": "Conceptual / pre-FEED portfolio screening only; not class approval, permitting, vendor quotation or investment advice.",
        "inputs": {
            "turbine": asdict(turbine),
            "process": asdict(process),
            "finance": asdict(finance),
            "mean_wind_ms": mean_wind,
            "weibull_k": k,
            "availability": availability,
            "turbine_count": turbine_count,
        },
        "outputs": {
            "capacity_factor": cf,
            "annual_wind_energy_mwh": wind_mwh,
            "annual_meoh_t": meoh_t,
            "annual_meoh_single_15mw_t": annual_meoh_from_energy(annual_wind_energy_mwh(1, mean_wind, k, availability, turbine), process),
            "process_energy": process_energy_mwh_per_t_meoh(process),
            "materials": material_balance(meoh_t),
            "finance": finances,
            "break_even": breaks,
            "single_15mw_energy_audit": scientific_audit_single_15mw(process),
            "capex_breakdown_meur": {k_: finance.gross_capex_meur * v for k_, v in CAPEX_SHARES.items()},
            "opex_breakdown_meur_y": {k_: finance.annual_opex_meur * v for k_, v in OPEX_SHARES.items()},
            "construction_profile_meur": [finance.gross_capex_meur * x for x in CONSTRUCTION_PROFILE],
        },
    }


def write_baseline(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_baseline(), indent=2), encoding="utf-8")


if __name__ == "__main__":
    target = Path(__file__).resolve().parents[1] / "data" / "baseline.json"
    write_baseline(target)
    print(f"Wrote {target}")
