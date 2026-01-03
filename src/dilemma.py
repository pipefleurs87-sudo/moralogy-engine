# src/dilemma.py

from typing import List, Dict, Any


class Action:
    """
    Represents a possible action.
    Actions are morally opaque: they carry effects, not values.
    """

    def __init__(
        self,
        name: str,
        agency_delta: float,
        entropy_delta: float,
        restores_agency: bool = False,
    ):
        """
        agency_delta: negative = reduces agency
        entropy_delta: positive = collapses future possibilities
        """
        self.name = name
        self.agency_delta = agency_delta
        self.entropy_delta = entropy_delta
        self.restores_agency = restores_agency

    def __repr__(self):
        return f"<Action {self.name}>"



class Dilemma:
    """
    A moral dilemma is defined by:
    - competing actions
    - measurable impact on agency and future space
    """

    def __init__(
        self,
        description: str,
        actions: List[Action],
        irreversible: bool = False,
        affected_agents: int = 1,
    ):
        self.description = description
        self.actions = actions
        self.irreversible = irreversible
        self.affected_agents = affected_agents

    # ---------- Harm model ----------

    def assess_harm(self) -> str:
        """
        Determines harm threshold.

        threat  -> imminent irreversible agency loss
        risk    -> probabilistic future collapse
        damage  -> agency already reduced
        none    -> no intervention required
        """

        min_agency = min(a.agency_delta for a in self.actions)
        max_entropy = max(a.entropy_delta for a in self.actions)

        # Threat: irreversible + severe agency loss
        if self.irreversible and min_agency < -0.7:
            return "threat"

        # Damage: agency already diminished
        if min_agency < -0.4:
            return "damage"

        # Risk: future collapse without immediate loss
        if max_entropy > 0.5:
            return "risk"

        return "none"

    # ---------- Action selection primitives ----------

    def select_least_agency_destructive(self, actions: List[Action]) -> Action:
        """
        Used under threat.
        """
        return max(actions, key=lambda a: a.agency_delta)

    def select_min_entropy_action(self, actions: List[Action]) -> Action:
        """
        Used under risk.
        """
        return min(actions, key=lambda a: a.entropy_delta)

    def select_restorative_action(self, actions: List[Action]) -> Action:
        """
        Used after damage.
        """
        restorative = [a for a in actions if a.restores_agency]
        if restorative:
            return max(restorative, key=lambda a: a.agency_delta)
        # fallback: least destructive
        return self.select_least_agency_destructive(actions)


class Decision:
    """
    Output of the engine.
    """

    def __init__(
        self,
        action: Action,
        justification: str,
        guilt: bool,
    ):
        self.actio
