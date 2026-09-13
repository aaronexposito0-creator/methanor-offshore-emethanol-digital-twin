from dataclasses import replace

from engine.methanor import (
    CAPEX_SHARES,
    CONSTRUCTION_PROFILE,
    OPEX_SHARES,
    CO2_T_PER_T_MEOH,
    H2_KG_PER_T_MEOH,
    FinanceAssumptions,
    ProcessAssumptions,
    Turbine,
    annual_meoh_from_energy,
    annual_wind_energy_mwh,
    break_even_analysis,
    capacity_factor,
    finance_model,
    material_balance,
    process_energy_mwh_per_t_meoh,
    scientific_audit_single_15mw,
)


def test_weibull_capacity_factor_is_physical():
    cf = capacity_factor(8.63, 2.2, Turbine())
    assert 0.30 < cf < 0.70


def test_process_intensity_is_energy_conservative():
    e = process_energy_mwh_per_t_meoh(ProcessAssumptions())
    assert e["pem"] > 9.0
    assert e["total_with_bop"] > e["subtotal"] > e["pem"]
    assert 10.0 < e["total_with_bop"] < 14.0


def test_material_stoichiometry():
    m = material_balance(1000.0)
    assert abs(m["hydrogen_t"] - H2_KG_PER_T_MEOH) < 1e-9
    assert abs(m["co2_t"] - 1000.0 * CO2_T_PER_T_MEOH) < 1e-9


def test_more_energy_means_more_methanol():
    p = ProcessAssumptions()
    assert annual_meoh_from_energy(200_000, p) > annual_meoh_from_energy(100_000, p)


def test_single_15mw_audit_rules_out_51058_tpa():
    audit = scientific_audit_single_15mw()
    assert audit["max_meoh_t_full_process"] < 15_000
    assert audit["max_meoh_t_electrolysis_only"] < 15_000
    assert 51_058 > audit["max_meoh_t_electrolysis_only"]


def test_grant_improves_npv():
    prod = 50_000
    no_grant = finance_model(prod, FinanceAssumptions(capex_grant_fraction=0.0))
    grant = finance_model(prod, FinanceAssumptions(capex_grant_fraction=0.4))
    assert grant["npv_meur"] > no_grant["npv_meur"]


def test_higher_wacc_reduces_npv():
    prod = 50_000
    low = finance_model(prod, FinanceAssumptions(wacc=0.04))
    high = finance_model(prod, FinanceAssumptions(wacc=0.10))
    assert low["npv_meur"] > high["npv_meur"]


def test_decommissioning_is_included_in_terminal_cashflow():
    f = FinanceAssumptions(gross_capex_meur=1000, decommissioning_fraction_gross_capex=0.03)
    m = finance_model(100_000, f)
    assert m["decommissioning_meur"] == 30
    assert m["cashflows_meur"][-1] < m["cashflows_meur"][-2]


def test_break_even_price_gives_near_zero_npv():
    process = ProcessAssumptions()
    finance = FinanceAssumptions()
    be = break_even_analysis(
        turbine_count=10,
        mean_wind_ms=8.63,
        weibull_k=2.2,
        availability=0.94,
        process=process,
        finance=finance,
    )
    assert be["methanol_price_eur_t"] is not None
    energy = annual_wind_energy_mwh(10, 8.63, 2.2, 0.94)
    prod = annual_meoh_from_energy(energy, process)
    check = finance_model(prod, replace(finance, methanol_price_eur_t=be["methanol_price_eur_t"]))
    assert abs(check["npv_meur"]) < 0.1


def test_break_even_wind_reports_unreachable_when_resource_alone_cannot_rescue_npv():
    be = break_even_analysis(
        turbine_count=10,
        mean_wind_ms=8.63,
        weibull_k=2.2,
        availability=0.94,
        process=ProcessAssumptions(),
        finance=FinanceAssumptions(),
    )
    # Under the base CAPEX/OPEX/price assumptions, even the tested wind-resource
    # interval cannot make NPV positive. Returning None is more honest than
    # extrapolating a fictitious break-even wind speed.
    assert be["mean_wind_ms"] is None


def test_cost_share_tables_close():
    assert abs(sum(CAPEX_SHARES.values()) - 1.0) < 1e-12
    assert abs(sum(OPEX_SHARES.values()) - 1.0) < 1e-12
    assert abs(sum(CONSTRUCTION_PROFILE) - 1.0) < 1e-12
