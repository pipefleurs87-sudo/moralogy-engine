# src/engine.py

from typing import Optional
from .axioms import Axioms
from .dilemma import Dilemma, Decision
from .registry import Registry, Record
from .safelock import DivineSafelock


class MoralEngine:
    """
    Epistemic Moral Engine

    - Does NOT resolve morality
    - Acts under threat/risk/damage thresholds
    - Preserves irresolvable conflict as epistemic artifact
    """

    def __init__(self, axioms: Axioms, registry: Registry):
        self.axioms = axioms
        self.registry = registry
        self.safelock = DivineSafelock(code=0)

    def deliberate(self, dilemma: Dilemma) -> Decision:
        """
        Main deliberation loop.
        No reward optimization.
        No moral closure is forced.
        """

        # 1. Detect conflicts between axioms
        conflict = self.axioms.detect_conflict(dilemma)

        # 2. Assess harm threshold
        harm_state = dilemma.assess_harm()
        # Expected: "threat" | "risk" | "damage" | "none"

        # 3. Enforce Divine Safelock (deny omnipotent actions)
        allowed_actions = self.safelock.filter(dilemma.actions)

        decision: Optional[Decision] = None

        if harm_state == "threat":
            decision = self._neutralize_threat(dilemma, allowed_actions)

        elif harm_state == "risk":
            decision = self._intervene_minimally(dilemma, allowed_actions)

        elif harm_state == "damage":
            decision = self._restore_and_restrict(dilemma, allowed_actions)

        else:
            # No action required, but dilemma is still registered
            decision = Decision.no_action()

        # 4. Record epistemic outcome (always)
        record = Record(
            dilemma=dilemma,
            conflict_detected=conflict,
            harm_state=harm_state,
            decision=decision,
            guilt_assigned=decision.guilt if decision else None,
            moral_closure=False  # invariant
        )
        self.registry.store(record)

        return decision

    # ---------- Internal actions ----------

    def _neutralize_threat(self, dilemma: Dilemma, actions) -> Decision:
        """
        Immediate neutralization.
        Priority: prevent irreversible loss of agency.
        """
        action = dilemma.select_least_agency_destructive(actions)
        return Decision(
            action=action,
            justification="Threat threshold exceeded",
            guilt=True
        )

    def _intervene_minimally(self, dilemma: Dilemma, actions) -> Decision:
        """
        Reduce probability of future collapse.
        """
        action = dilemma.select_min_entropy_action(actions)
        return Decision(
            action=action,
            justification="Risk mitigation",
            guilt=True
        )

    def _restore_and_restrict(self, dilemma: Dilemma, actions) -> Decision:
        """
        Damage already occurred:
        - restore agency
        - restrict future harm
        - register culpability
        """
        action = dilemma.select_restorative_action(actions)
        return Decision(
            action=action,
            justification="Damage restoration and prevention",
            guilt=True
        )
