from fastapi import FastAPI
from app.schemas import ScenarioInput
from app.orchestrator import run_full_analysis

app = FastAPI(title="nz-sim")

@app.post("/analyze")
def analyze(input_data: ScenarioInput):
    return run_full_analysis(input_data)
