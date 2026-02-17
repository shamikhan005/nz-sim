# strategic feasibility

import json
from app.core.k2_client import call_k2
from app.modules.logical_audit import extract_json

def run_strategic_feasibility(scenario_input, simulation_result):
    
    # only feed it what it needs: the claim and the simulated math
    structured_input = {
        "sustainability_claim": scenario_input.sustainability_claim or "No claim provided.",
        "simulated_scenarios": simulation_result.get("scenarios", []),
        "recommended_technical_strategy": simulation_result.get("recommended_strategy")
    }

    messages = [
        {
            "role": "system",
            "content": """
You are a Corporate Sustainability Strategy Board.
Your job is to evaluate proposed carbon reduction scenarios against the company's stated public sustainability claims.

Rules:
1. Assess if the company's public claim is realistic given the simulated mathematical realities.
2. Evaluate the business feasibility of the scenarios (cost, operational disruption, timeline).
3. Return STRICT JSON only.
4. Do NOT include planning thoughts or conversational text.

Output format:
{
  "claim_assessment": {
    "is_claim_realistic": false,
    "critique": "Explain why the claim holds up or falls apart based on the math."
  },
  "business_feasibility_ranking": [
    {
      "scenario_name": "Name from simulations",
      "estimated_timeline_months": 24,
      "risk_level": "High/Medium/Low",
      "primary_business_barrier": "Biggest real-world hurdle"
    }
  ],
  "final_strategic_verdict": "A concise, C-suite level summary of what the company must actually do."
}
"""
        },
        {
            "role": "user",
            "content": f"""
Evaluate the strategic feasibility of these scenarios against the public claim:

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
            return {"error": "Strategic Feasibility JSON parsing failed", "raw_output": raw_response}
    
    return {"error": "No JSON detected", "raw_output": raw_response}