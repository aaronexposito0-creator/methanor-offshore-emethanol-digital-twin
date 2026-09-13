# Scientific audit — the 15 MW / 51 kt-y correction

## Finding

The original thesis reported a P50 production of **51,058 t/y e-methanol** while the concept title and primary generator referred to a **15 MW wind turbine**.

MethaNor flags this as an energy-conservation inconsistency.

## First-principles check

Absolute electrical ceiling of one 15 MW turbine:

```text
15 MW × 8,760 h = 131,400 MWh/y
```

For the reaction `CO2 + 3H2 → CH3OH + H2O`, one tonne of methanol requires about **188.75 kg H2**.

At the MethaNor base PEM assumption of 52 kWh/kg H2:

```text
188.75 × 52 ≈ 9.82 MWh electricity / t MeOH
```

That means that even the impossible best case of:

- 100% turbine capacity factor,
- 100% availability,
- no DAC demand,
- no synthesis demand,
- no water treatment,
- no balance-of-plant consumption,

would be limited to roughly:

```text
131,400 / 9.82 ≈ 13,400 t/y MeOH
```

Adding DAC, synthesis, water treatment, balance of plant, realistic wind distribution and availability lowers the expected 15 MW output further. Under the MethaNor base scenario it is approximately **5–6 kt/y**, depending on the exact wind and process inputs.

## Resolution

MethaNor separates two scales:

### Engineering unit

- 1 × IEA 15 MW turbine
- one conceptual semisubmersible platform
- naval architecture baseline
- output scale ≈ 5–6 kt/y in the base model

### Commercial hub

- 10 × 15 MW = 150 MW floating wind
- centralised P2X / storage concept
- output scale ≈ 50+ kt/y in the base model

This lets the original physical idea survive while removing the internal energy contradiction.

## Why this matters

This correction is one of the main reasons for rebuilding the thesis as software: conservation laws, cash-flow consistency and sensitivity tests are easier to audit when equations are executable and unit-tested.
