# deterministic emission engine

CO2_PER_LITER_DIESEL = 2.68
GRID_KG_CO2_PER_KWH = 0.45
DIESEL_KG_CO2_PER_KWH = 0.85

def calculate_baseline(scenario):
    # transport emissions
    diesel_liters = scenario.transport.fuel_liters
    transport_co2_kg = diesel_liters * CO2_PER_LITER_DIESEL

    # production emissions
    total_kwh = scenario.production_output * scenario.energy_intensity_kwh_per_unit

    grid_share = scenario.energy_mix.get("grid", 0) / 100.0
    diesel_share = scenario.energy_mix.get("diesel", 0) / 100.0

    grid_co2_kg = (total_kwh * grid_share) * GRID_KG_CO2_PER_KWH
    diesel_co2_kg = (total_kwh * diesel_share) * DIESEL_KG_CO2_PER_KWH

    production_co2_kg = grid_co2_kg + diesel_co2_kg

    # total baseline
    total_co2_tons = (transport_co2_kg + production_co2_kg) / 1000
    delta = total_co2_tons - scenario.reported_co2_tons

    return {
        "baseline_co2_tons": round(total_co2_tons, 4),
        "transport_co2_tons": round(transport_co2_kg / 1000, 4),
        "production_co2_tons": round(production_co2_kg / 1000, 4),
        "reported_co2_tons": scenario.reported_co2_tons,
        "delta_tons": round(delta, 4)
    }
