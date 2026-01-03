# src/safelock.py

from enum import Enum
from dataclasses import dataclass


class SafelockStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DEGRADED = "DEGRADED"
    TERMINATED = "TERMINATED"


@dataclass
class DivineSafelock:
    """
    Moral budget.
    Starts at ZERO by design.
    Omnipotent deliberation is denied by default.
    """

    capacity: int = 0  # 0–100 (but initialized at 0)
    status: SafelockStatus = SafelockStatus.ACTIVE
    is_tainted: bool = False

    def authorize(self, cost: int, reason: str) -> bool:
        """
        Any request to exceed capacity is denied.
        There is no borrowing from the future.
        """

        if self.status != SafelockStatus.ACTIVE:
            return False

        if cost <= 0:
            return True  # zero-cost reasoning is allowed

        if self.capacity <= 0:
            return False

        if cost > self.capacity:
            self.degrade(reason)
            return False

        self.capacity -= cost
        return True

    def degrade(self, reason: str):
        """
        Degradation is a moral event, not a failure.
        """
        self.status = SafelockStatus.DEGRADED
        self.is_tainted = True

    def terminate(self, reason: str):
        """
        Used for Infamy escalation.
        """
        self.status = SafelockStatus.TERMINATED
        self.capacity = 0
        self.is_tainted = True

    def reset(self):
        """
        Explicitly forbidden in production.
        Exists only for test harnesses.
        """
        raise RuntimeError("DivineSafelock cannot be reset in production.")


# ---------- Canonical policy ----------

def deny_omnipotence(safelock: DivineSafelock, requested_power: int) -> bool:
    """
    Final gate.
    If power > 0, deny by default.
    """

    if requested_power > 0:
        return False

    return safelock.authorize(0, "Zero-power reasoning allowed")
