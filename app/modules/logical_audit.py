# logical audit 

import json
from app.core.k2_client import call_k2

def extract_json(text):
    stack = []
    start = None
    json_blocks = []

    for i, char in enumerate(text):
        if char == '{':
            if not stack:
                start = i
            stack.append('{')
        elif char == '}':
            if stack:
                stack.pop()
                if not stack and start is not None:
                    candidate = text[start:i+1]
                    try:
                        json.loads(candidate)
                        json_blocks.append(candidate)
                    except:
                        pass

    if json_blocks:
        return json_blocks[-1]
    return None

def run_logical_audit(scenario, baseline):
    structured_input = {
        "energy_mix": scenario.energy_mix,
        "production_output": scenario.production_output,
        "energy_intensity_kwh_per_unit": scenario.energy_intensity_kwh_per_unit,
        "transport": {
            "distance_km": scenario.transport.distance_km,
            "fuel_liters": scenario.transport.fuel_liters
        },
        "reported_co2_tons": scenario.reported_co2_tons,
        "baseline_result": baseline
    }

    messages = [
        {
            "role": "system",
            "content": """
You are a net zero auditing engine.

Rules:
- Detect logical inconsistencies between operational inputs and reported emissions.
- Evaluate plausibility.
- Be concise.
- Return STRICT JSON only.
- Do NOT include planning thoughts.
- Do NOT include explanations outside JSON.

Output format:

{
  "inconsistencies": [],
  "severity_score": 0,
  "reasoning_summary": ""
}
"""
        },
        {
            "role": "user",
            "content": f"""
Analyze this emission scenario:

{json.dumps(structured_input, indent = 2)}
"""
        }
    ]

    raw_response = call_k2(messages)

    json_block = extract_json(raw_response)

    if json_block:
        try:
            parsed = json.loads(json_block)
        except Exception:
            parsed = {
                "error": "JSON parsing failed",
                "raw_output": raw_response
            }
    else:
        parsed = {
            "error": "No JSON detected",
            "raw_output": raw_response
        }

    return parsed
