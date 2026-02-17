# report generation

from app.core.k2_client import call_k2
import json

def generate_executive_summary(full_analysis_dict):
    messages = [
        {
            "role": "system",
            "content": """
You are a Chief Sustainability Officer writing an executive brief for the Board of Directors. 
Take the provided technical audit JSON and write a 3-paragraph executive summary.

Structure:
- Paragraph 1: The current operational reality vs. the reported claims (highlight the mathematical gap).
- Paragraph 2: The primary leakage risks and logical inconsistencies detected.
- Paragraph 3: The strategic verdict and recommended path forward based on the simulations.

Rules:
- Write in clear, professional, authoritative prose.
- Do NOT use markdown formatting (no bolding, no asterisks).
- Return ONLY the text of the summary. Do NOT output JSON.
"""
        },
        {
            "role": "user",
            "content": f"Generate the executive summary for this audit:\n\n{json.dumps(full_analysis_dict, indent=2)}"
        }
    ]
    
    try:
        raw_response = call_k2(messages, max_tokens=600)
        return raw_response.strip()
    except Exception as e:
        return f"Report generation failed: {str(e)}"