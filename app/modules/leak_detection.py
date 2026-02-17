# leak detection

import json
from app.core.k2_client import call_k2
from app.modules.logical_audit import extract_json

def run_leak_detection(scenario, baseline, logical_audit):
    structured_input = {
        "energy_mix": scenario.energy_mix,
        "production_output": scenario.production_output,
        "energy_intensity_kwh_per_unit": scenario.energy_intensity_kwh_per_unit,
        "transport": {
            "distance_km": scenario.transport.distance_km,
            "fuel_liters": scenario.transport.fuel_liters
        },
        "reported_co2_tons": scenario.reported_co2_tons,
        "baseline_result": baseline,
        "logical_audit_result": logical_audit
    }

    messages = [
        {
            "role": "system",
            "content": """
You are a carbon leakage detection engine.

Rules:
1. Return STRICT JSON only. 
2. NO conversational text (e.g. "Here is the analysis").
3. NO internal monologue or planning steps.
4. Limit lists to the TOP 5 most critical items to avoid loops.

Output format:
{
  "potential_leaks": ["Item 1", "Item 2"...],
  "scope_gaps": ["Item 1", "Item 2"...],
  "leakage_risk_score": 0,
  "leakage_summary": "Concise summary."
}
"""
        },
        {
            "role": "user",
            "content": f"""
Analyze potential carbon leakage in this scenario:

{json.dumps(structured_input, indent=2)}
"""
        }
    ]

    raw_response = call_k2(messages)
    json_block = extract_json(raw_response)

    if json_block:
        try:
            return json.loads(json_block)
        except Exception:
            return {"error": "Leak JSON parsing failed", "raw_output": raw_response}

    return {"error": "No JSON detected", "raw_output": raw_response}
