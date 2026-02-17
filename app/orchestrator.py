from app.core.emission_engine import calculate_baseline
from app.modules.logical_audit import run_logical_audit
from app.modules.leak_detection import run_leak_detection
from app.modules.counterfactual_simulation import run_counterfactual_simulation
from app.modules.strategic_feasibility import run_strategic_feasibility
from app.modules.report_generator import generate_executive_summary

def run_full_analysis(input_data):
    baseline = calculate_baseline(input_data)

    logical_report = run_logical_audit(input_data, baseline)

    leak_report = run_leak_detection(
        input_data,
        baseline,
        logical_report
    )

    simulation_report = run_counterfactual_simulation(
        input_data,
        baseline,
        logical_report,
        leak_report
    )

    feasibility_report = run_strategic_feasibility(
        input_data,
        simulation_report
    )

    final_payload = {
        "baseline": baseline,
        "logical_audit": logical_report,
        "leak_detection": leak_report,
        "counterfactual_simulation": simulation_report,
        "strategic_feasibility": feasibility_report
    }

    final_payload["executive_summary"] = generate_executive_summary(final_payload)

    return final_payload
