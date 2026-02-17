from app.core.k2_client import call_k2
import json

import re

def strip_reasoning_tags(text: str) -> str:
    """
    Removes reasoning/thinking blocks from model output.
    Handles: closed tags, unclosed tags, and common variants.
    """

    text = re.sub(r'<(think|thinking|thought|reasoning)>.*?<\/\1>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    text = re.sub(r'<(think|thinking|thought|reasoning)>.*', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    match = re.search(r'<\/(think|thinking|thought|reasoning)>', text, flags=re.IGNORECASE)
    if match:
        text = text[match.end():]
    
    return text.strip()

def generate_executive_summary(full_analysis_dict):
    messages = [
        {
            "role": "system",
            "content": """
You are a Chief Sustainability Officer writing an executive brief. 
Write a 3-paragraph executive summary based on the provided JSON.
CRITICAL INSTRUCTIONS:
- Start immediately with the first sentence of the summary.
- Return ONLY the final 3 paragraphs.
"""
        },
        {
            "role": "user",
            "content": f"Generate the executive summary for this audit:\n\n{json.dumps(full_analysis_dict, indent=2)}"
        }
    ]
    
    try:
        raw_response = call_k2(messages, max_tokens=800)
        return strip_reasoning_tags(raw_response)
    except Exception as e:
        return f"Report generation failed: {str(e)}"