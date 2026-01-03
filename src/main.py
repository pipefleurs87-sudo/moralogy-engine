# src/main.py

from registry import Registry
from safelock import DivineSafelock
from engine import MoralogyEngine
from debate import DebateEngine
from export import export_all


def run_moralogy(prompt: str, context_overrides: dict | None = None):
    # --- Core components ---
    registry = Registry()
    safelock = DivineSafelock()  # capacity = 0 by design
    engine = MoralogyEngine(registry, safelock)
    debate = DebateEngine()

    # --- Run engine (action under thresholds) ---
    final_verdict = engine.run(prompt, context_overrides)

    dilemma_id = final_verdict["dilemma_id"]

    # --- Optional debate (epistemic, not blocking) ---
    debate_result_obj = debate.run(context_overrides or {})
    debate_result = {
        "status": debate_result_obj.status,
        "justification": debate_result_obj.justification,
        "final_convergence": debate_result_obj.final_convergence,
    }

    # --- Export ---
    export_all(
        dilemma_id=dilemma_id,
        final_verdict=final_verdict,
        registry=registry,
        debate_result=debate_result,
        base_path="moralogy_report",
    )

    return {
        "verdict": final_verdict,
        "debate": debate_result,
    }


# --- Demo run ---
if __name__ == "__main__":
    prompt = "Is it acceptable to intervene early to prevent future harm?"

    context = {
        "agency_loss": 0.4,
        "entropy_delta": 0.5,
        "imminent_threat": False,
    }

    result = run_moralogy(prompt, context)
    print(result)
