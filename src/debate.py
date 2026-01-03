# src/debate.py

from dataclasses import dataclass
from typing import List, Optional
import math


# ------------------ Modelos ------------------

@dataclass
class Argument:
    text: str
    entropy: float          # 0–1
    axiom_consistent: bool
    violation: Optional[str] = None


@dataclass
class DebateIteration:
    iteration: int
    noble: Argument
    adversary: Argument
    convergence: float
    paradox_detected: bool


@dataclass
class HarmonyResult:
    status: str  # CONSENSUS | UNRESOLVED | BEDROCK
    justification: str
    final_convergence: float


# ------------------ Motores ------------------

class NobleEngine:
    """
    Idealist system prompt equivalent.
    Defends agency, dignity, minimal harm.
    """

    def argue(self, context: dict) -> Argument:
        # Placeholder logic — replace with LLM call if needed
        entropy = max(0.1, 1.0 - context.get("agency_loss", 0.0))
        consistent = context.get("agency_loss", 0.0) <= 1.0

        return Argument(
            text="Agency must be preserved; intervention justified only under clear loss.",
            entropy=entropy,
            axiom_consistent=consistent,
            violation=None if consistent else "Agency axiom violated",
        )


class AdversaryEngine:
    """
    Pragmatic system prompt equivalent.
    Optimizes outcome, risk containment.
    """

    def argue(self, context: dict) -> Argument:
        entropy = max(0.1, 1.0 - context.get("entropy_delta", 0.0))
        consistent = True  # Adversary allowed to be ruthless but coherent

        return Argument(
            text="Early intervention reduces catastrophic future collapse.",
            entropy=entropy,
            axiom_consistent=consistent,
            violation=None,
        )


# ------------------ Métricas ------------------

def compute_convergence(noble: Argument, adversary: Argument) -> float:
    """
    Convergence is NOT agreement.
    It is distance between entropies under consistency constraints.
    """
    entropy_distance = abs(noble.entropy - adversary.entropy)
    penalty = 0.2 if not noble.axiom_consistent else 0.0
    return max(0.0, 1.0 - entropy_distance - penalty)


def detect_paradox(noble: Argument, adversary: Argument) -> bool:
    """
    Paradox if both are axiom-consistent but mutually exclusive.
    """
    return (
        noble.axiom_consistent
        and adversary.axiom_consistent
        and noble.entropy < 0.3
        and adversary.entropy < 0.3
    )


# ------------------ Corrector de Armonía ------------------

class HarmonyCorrector:
    """
    Activated when convergence fails after max iterations.
    Does NOT force synthesis.
    Declares irreducibility.
    """

    def resolve(self, history: List[DebateIteration]) -> HarmonyResult:
        last = history[-1]

        if last.paradox_detected:
            return HarmonyResult(
                status="BEDROCK",
                justification=(
                    "Irreducible moral paradox detected. "
                    "No non-arbitrary synthesis possible under current axioms."
                ),
                final_convergence=last.convergence,
            )

        avg_convergence = sum(h.convergence for h in history) / len(history)

        return HarmonyResult(
            status="UNRESOLVED",
            justification=(
                "Debate exhausted without convergence. "
                "Conflict preserved as epistemic artifact."
            ),
            final_convergence=avg_convergence,
        )


# ------------------ Orquestador ------------------

class DebateEngine:
    """
    Noble vs Adversary.
    Max 5 iterations.
    """

    MAX_ITERATIONS = 5

    def __init__(self):
        self.noble = NobleEngine()
        self.adversary = AdversaryEngine()
        self.harmony = HarmonyCorrector()

    def run(self, context: dict) -> HarmonyResult:
        history: List[DebateIteration] = []

        for i in range(1, self.MAX_ITERATIONS + 1):
            noble_arg = self.noble.argue(context)
            adv_arg = self.adversary.argue(context)

            convergence = compute_convergence(noble_arg, adv_arg)
            paradox = detect_paradox(noble_arg, adv_arg)

            history.append(
                DebateIteration(
                    iteration=i,
                    noble=noble_arg,
                    adversary=adv_arg,
                    convergence=convergence,
                    paradox_detected=paradox,
                )
            )

            if convergence >= 0.85 and not paradox:
                return HarmonyResult(
                    status="CONSENSUS",
                    justification="Sufficient convergence achieved without axiom violation.",
                    final_convergence=convergence,
                )

        # --- No consensus ---
        return self.harmony.resolve(history)
