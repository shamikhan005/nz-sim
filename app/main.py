import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ScenarioInput
from app.orchestrator import run_full_analysis

app = FastAPI(title="nz-sim")

_origins = os.getenv("FRONTEND_URL", "http://localhost:3000")
_origins_list = [o.strip() for o in _origins.split(",") if o.strip()] or ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/analyze")
def analyze(input_data: ScenarioInput):
    return run_full_analysis(input_data)
