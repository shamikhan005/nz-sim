from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ScenarioInput
from app.orchestrator import run_full_analysis

app = FastAPI(title="nz-sim")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/analyze")
def analyze(input_data: ScenarioInput):
    return run_full_analysis(input_data)
