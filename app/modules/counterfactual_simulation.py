# counterfactual simulation

import json
from app.core.k2_client import call_k2
from app.modules.logical_audit import extract_json

# VALIDATION LAYER
def validate_simulation(simulation, baseline):

    # hard structure guard
    if not isinstance(simulation, dict):
        return {
            "structure_error": "Invalid JSON object",
            "validation_passed": False,
            "dominant_scenario": None,
            "recommended_strategy": None,
            "system_confidence": 0.2
        }

    if "scenarios" not in simulation or not isinstance(simulation["scenarios"], list):
        return {
            "structure_error": "Missing scenarios array",
            "validation_passed": False,
            "dominant_scenario": None,
            "recommended_strategy": None,
            "system_confidence": 0.3
        }

    baseline_value = baseline.get("baseline_co2_tons")

    if baseline_value is None:
        simulation["validation_passed"] = False
        simulation["system_confidence"] = 0.2
        return simulation

    scenarios = simulation["scenarios"]

    if len(scenarios) != 3:
        simulation["structure_error"] = "Exactly 3 scenarios required"

    energy_mix_modified = False
    transport_modified = False
    all_valid = True
    dominant_candidate = None
    best_score = -1


    for scenario in scenarios:

        scenario["calculation_error"] = False
        adjustments = scenario.get("adjustments", {})

        new_value = scenario.get("estimated_new_co2_tons", 0)
        reported_reduction = scenario.get("reduction_from_baseline_tons", 0)
        feasibility = scenario.get("feasibility_score", 0)

        # feasibility normalization
        if 0 < feasibility <= 1:
            feasibility *= 100

        feasibility = max(0, min(100, feasibility))
        scenario["feasibility_score"] = feasibility

        # negative emission guard
        if new_value < 0:
            scenario["calculation_error"] = True
            scenario["error_reason"] = "Negative emissions not allowed"
            all_valid = False
            continue

        # reduction consistency check
        expected_reduction = round(baseline_value - new_value, 6)

        if abs(expected_reduction - reported_reduction) > 0.0001:
            scenario["calculation_error"] = True
            scenario["error_reason"] = "Reduction mismatch"
            all_valid = False

        # energy mix validation
        energy_mix = adjustments.get("energy_mix")
        if energy_mix:
            energy_mix_modified = True

            total = sum(energy_mix.values())

            if abs(total - 100) > 0.01:
                scenario["calculation_error"] = True
                scenario["error_reason"] = "Energy mix must sum to 100"
                all_valid = False

            if "transport" not in adjustments:
                scenario["conceptual_warning"] = (
                    "Energy mix change does not automatically reduce transport fuel."
                )

        # transport modification detection
        if "transport" in adjustments:
            transport_modified = True

        # offset sanity check
        offsets = None

        if "carbon_offsets" in adjustments:
            offsets = adjustments.get("carbon_offsets")

        elif "offsets_tons" in adjustments:
            offsets = adjustments.get("offsets_tons")

        elif "offsets" in adjustments:
            nested = adjustments.get("offsets")
            if isinstance(nested, dict):
                offsets = nested.get("offset_tons")

        if offsets is not None:

            if offsets < 0:
                scenario["calculation_error"] = True
                scenario["error_reason"] = "Negative offsets not allowed"
                all_valid = False

            if offsets > reported_reduction:
                scenario["calculation_error"] = True
                scenario["error_reason"] = "Offsets exceed reduction"
                all_valid = False

        # bottleneck requirement
        if not scenario.get("bottlenecks"):
            scenario["calculation_error"] = True
            scenario["error_reason"] = "Missing bottlenecks"
            all_valid = False

        # dominance scoring
        if not scenario["calculation_error"] and feasibility > 0:

            reduction_ratio = (
                reported_reduction / baseline_value
                if baseline_value > 0 else 0
            )

            feasibility_ratio = feasibility / 100

            score = reduction_ratio * 0.7 + feasibility_ratio * 0.3

            name = (scenario.get("name") or "").lower()

            if "offset" in name:
                score *= 0.8 

            if score > best_score:
                best_score = score
                dominant_candidate = scenario.get("name")

    # structural enforcement
    if not energy_mix_modified:
        simulation["structure_warning"] = "At least one scenario must modify energy_mix"

    if not transport_modified:
        simulation["structure_warning_transport"] = "At least one scenario must modify transport"

    simulation["validation_passed"] = (
        len(scenarios) == 3 and all_valid
    )

    simulation["dominant_scenario"] = dominant_candidate
    simulation["recommended_strategy"] = dominant_candidate

    simulation["system_confidence"] = (
        0.95 if simulation["validation_passed"] else 0.4
    )

    return simulation

# EXECUTION LAYER
def run_counterfactual_simulation(scenario, baseline, logical_audit, leak_detection):

    structured_input = {
        "original_scenario": {
            "energy_mix": scenario.energy_mix,
            "production_output": scenario.production_output,
            "energy_intensity_kwh_per_unit": scenario.energy_intensity_kwh_per_unit,
            "transport": {
                "distance_km": scenario.transport.distance_km,
                "fuel_liters": scenario.transport.fuel_liters
            },
            "reported_co2_tons": scenario.reported_co2_tons,
        },
        "baseline_co2_tons": baseline.get("baseline_co2_tons"),
        "logical_summary": logical_audit.get("reasoning_summary", ""),
        "leak_summary": leak_detection.get("leakage_summary", ""),
        "assumptions": {
            "diesel_emission_factor_kg_per_liter": 2.68,
            "grid_kg_co2_per_kwh": 0.45,
            "diesel_kg_co2_per_kwh": 0.85
        }
    }

    messages = [
        {
            "role": "system",
            "content": """
You are a counterfactual emissions simulation engine.

CRITICAL MATH RULES:
- When using percentages from 'energy_mix', ALWAYS convert to decimals (e.g., 80% = 0.80, not 80).
- Production Emissions Formula: 
  (Total_kWh * (grid_percent / 100) * 0.45) + (Total_kWh * (diesel_percent / 100) * 0.85) / 1000
- Transport Emissions Formula: 
  (fuel_liters * 2.68) / 1000

CRITICAL STRUCTURE:
Return EXACTLY this top-level JSON structure:

{
  "scenarios": [
    {
      "name": "Scenario Name",
      "adjustments": {
        "energy_mix": {"grid": 80, "diesel": 20}, 
        "transport": {"distance_km": 1500, "fuel_liters": 100},
        "carbon_offsets": 0.1
      },
      "estimated_new_co2_tons": 0.0,
      "reduction_from_baseline_tons": 0.0,
      "calculation_trace": "Step-by-step math showing decimal conversion...",
      "bottlenecks": "Identified constraints...",
      "feasibility_score": 85
    }
  ],
  "recommended_strategy": "Name of best scenario",
  "simulation_summary": "Overall summary..."
}

Rules:
- Generate EXACTLY 3 scenarios.
- Scenario 1 MUST include "energy_mix" inside "adjustments" (values must sum to 100).
- Scenario 2 MUST include "transport" inside "adjustments".
- Scenario 3 MAY include "carbon_offsets" inside "adjustments".
- baseline_co2_tons - estimated_new_co2_tons MUST EXACTLY equal reduction_from_baseline_tons.
- Do NOT allow negative emissions.
Return STRICT JSON only.
"""
        },
        {
            "role": "user",
            "content": f"""
Simulate mitigation strategies for this scenario:

{json.dumps(structured_input, indent=2)}
"""
        }
    ]

    raw_response = call_k2(messages)
    json_block = extract_json(raw_response)

    if not json_block:
        return {
            "structure_error": "No JSON detected",
            "validation_passed": False,
            "system_confidence": 0.2
        }

    try:
        parsed = json.loads(json_block)
        validated = validate_simulation(parsed, baseline)

        if not validated.get("validation_passed", False):

            messages.insert(1, {
                "role": "system",
                "content": f"Previous output violated structure. Errors: {json.dumps(validated)}. Return EXACTLY 3 fully compliant scenarios using the strict schema."
            })

            retry_response = call_k2(messages)
            retry_block = extract_json(retry_response)

            if retry_block:
                retry_parsed = json.loads(retry_block)
                return validate_simulation(retry_parsed, baseline)

        return validated

    except Exception:
        return {
            "structure_error": "Simulation JSON parsing failed",
            "validation_passed": False,
            "system_confidence": 0.2
        }