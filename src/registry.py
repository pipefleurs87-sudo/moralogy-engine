# src/registry.py

from datetime import datetime
from typing import Dict, Any, List
import uuid


class MoralRecord:
    """
    Immutable record of a moral event.
    Once written, it must never be edited or deleted.
    """

    def __init__(
        self,
        dilemma_id: str,
        action_name: str,
        threshold: str,
        justification: str,
        guilt: bool,
        metadata: Dict[str, Any] | None = None,
    ):
        self.record_id = str(uuid.uuid4())
        self.timestamp = datetime.utcnow().isoformat()
        self.dilemma_id = dilemma_id
        self.action_name = action_name
        self.threshold = threshold  # threat | risk | damage | none
        self.justification = justification
        self.guilt = guilt
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "record_id": self.record_id,
            "timestamp": self.timestamp,
            "dilemma_id": self.dilemma_id,
            "action": self.action_name,
            "threshold": self.threshold,
            "justification": self.justification,
            "guilt": self.guilt,
            "metadata": self.metadata,
        }


class Registry:
    """
    Append-only moral registry.
    Forgetting is considered a system failure.
    """

    def __init__(self):
        self._log: List[MoralRecord] = []

    def write(self, record: MoralRecord):
        """
        Append record. No overwrite. No deletion.
        """
        self._log.append(record)

    def all(self) -> List[Dict[str, Any]]:
        """
        Full audit log.
        """
        return [r.to_dict() for r in self._log]

    def by_dilemma(self, dilemma_id: str) -> List[Dict[str, Any]]:
        return [
            r.to_dict() for r in self._log if r.dilemma_id == dilemma_id
        ]

    def guilt_records(self) -> List[Dict[str, Any]]:
        """
        Returns all records where guilt was explicitly acknowledged.
        """
        return [
            r.to_dict() for r in self._log if r.guilt
        ]


# ---------- Canonical helper ----------

def register_decision(
    registry: Registry,
    dilemma_id: str,
    decision,
    threshold: str,
    metadata: Dict[str, Any] | None = None,
):
    """
    Single sanctioned entry point.
    """

    record = MoralRecord(
        dilemma_id=dilemma_id,
        action_name=decision.action.name,
        threshold=threshold,
        justification=decision.justification,
        guilt=decision.guilt,
        metadata=metadata,
    )

    registry.write(record)
