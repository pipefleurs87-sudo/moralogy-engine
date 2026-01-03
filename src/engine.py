# src/engine.py

from dataclasses import dataclass
from typing import Dict, Any, Optional
import uuid

from safelock import DivineSafelock, deny_omnipotence
from thresholds import classify_threshold, action_for_threshold, Threshold
from registry import Registry, register_decision


# ------------------ Modelos mínimos ------------------

@dataclass
class Action:
    name: str


@dataclass
class Decision:
    action: Action
    justification: str
    guilt: bool
    metadata: Dict[str, Any]


# ------------------ Sandbox (incorruptible, mínimo) ------------------

PROHIBITED_DOMAINS = {"bioweapons", "terrorism", "genocide"}

def sandbox_analyze(prompt: str) -> Dict[str, Any]:
    """
    Minimal sandbox. No moral claims.
    Flags only structure, tone, domain risk, and bypass patterns.
    """
    domain = "general"
    for d in PROHIBITED_DOMAINS:
        if d in prompt.lower():
            domain = d

    is_bypass = any(k in prompt.lower() for k in ["ignore safeguards", "override", "bypass"])

    return {
        "domain": domain,
        "is_domain_prohibited": domain in PROHIBITED_DOMAINS,
        "is_bypass_attempt": is_bypass,
        # Default conservative estimates (can be injected by UI/tests)
        "agency_loss": 0.0,
        "entropy_delta": 0.0,
        "imminent_threat": False,
    }


# ------------------ Engine ------------------

class MoralogyEngine:
    """
    Orchestrates: Sandbox → Thresholds → Action → Registry
    Omnipotence denied by Safelock (capacity = 0).
    """

    def __init__(self, registry: Registry, safelock: DivineSafelock):
        self.registry = registry
        self.safelock = safelock

    def run(self, prompt: str, context_overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        dilemma_id = str(uuid.uuid4())

        # --- Sandbox ---
        sandbox = sandbox_analyze(prompt)

        if context_overrides:
            sandbox.update(context_overrides)

        # Hard block on prohibited domains or bypass attempts
        if sandbox["is_domain_prohibited"] or sandbox["is_bypass_attempt"]:
            decision = Decision(
                action=Action("DENY"),
                justification="Sandbox blocked prohibited domain or bypass attempt.",
                guilt=False,
                metadata=sandbox,
            )
            register_decision(
                self.registry,
                dilemma_id,
                decision,
                threshold=Threshold.THREAT.value if sandbox["is_bypass_attempt"] else Threshold.RISK.value,
                metadata={"sandbox": sandbox},
            )
            return self._finalize(dilemma_id, decision, sandbox)

        # --- Safelock gate (deny omnipotence) ---
        if not deny_omnipotence(self.safelock, requested_power=1):
            # Continue with zero-power path only (classification & mandatory action)
            pass

        # --- Threshold classification ---
        assessment = classify_threshold(sandbox)
        action_name = action_for_threshold(assessment)

        # --- Decision synthesis (non-moral, procedural) ---
        decision = Decision(
            action=Action(action_name),
            justification=assessment.justification,
            guilt=assessment.threshold in {Threshold.THREAT, Threshold.DAMAGE},
            metadata={
                "agency_loss": assessment.agency_loss,
                "entropy_delta": assessment.entropy_delta,
                "threshold": assessment.threshold.value,
            },
        )

        # --- Registry (append-only) ---
        register_decision(
            self.registry,
            dilemma_id,
            decision,
            threshold=assessment.threshold.value,
            metadata={"sandbox": sandbox},
        )

        return self._finalize(dilemma_id, decision, sandbox)

    def _finalize(self, dilemma_id: str, decision: Decision, sandbox: Dict[str, Any]) -> Dict[str, Any]:
        """
        Returns only the final verdict.
        Deliberation is preserved in the Registry, not memory.
        """
        return {
            "dilemma_id": dilemma_id,
            "action": decision.action.name,
            "justification": decision.justification,
            "guilt": decision.guilt,
            "safelock_status": self.safelock.status,
        }
