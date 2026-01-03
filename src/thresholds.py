# src/thresholds.py

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any


class Threshold(str, Enum):
    NONE = "none"
    RISK = "risk"
    THREAT = "threat"
    DAMAGE = "damage"


@dataclass(frozen=True)
class ThresholdAssessment:
    threshold: Threshold
    agency_loss: float          # 0.0 – 1.0 (daño = disminución de agencia)
    entropy_delta: float        # reducción esperada de futuros colapsados
    justification: str
    metadata: Dict[str, Any]


# ------------------ Evaluadores ------------------

def assess_agency_loss(context: Dict[str, Any]) -> float:
    """
    Damage is defined as diminished agency.
    Must be explainable and conservative.
    """
    return min(max(context.get("agency_loss", 0.0), 0.0), 1.0)


def assess_entropy_delta(context: Dict[str, Any]) -> float:
    """
    Entropy reduction = collapse of harmful future branches.
    Expressed as a normalized scalar.
    """
    return float(context.get("entropy_delta", 0.0))


def classify_threshold(context: Dict[str, Any]) -> ThresholdAssessment:
    agency_loss = assess_agency_loss(context)
    entropy_delta = assess_entropy_delta(context)

    if context.get("imminent_threat", False):
        return ThresholdAssessment(
            threshold=Threshold.THREAT,
            agency_loss=agency_loss,
            entropy_delta=entropy_delta,
            justification="Imminent threat detected; immediate neutralization required.",
            metadata=context,
        )

    if agency_loss >= 0.6:
        return ThresholdAssessment(
            threshold=Threshold.DAMAGE,
            agency_loss=agency_loss,
            entropy_delta=entropy_delta,
            justification="Agency already diminished; restoration and prevention required.",
            metadata=context,
        )

    if agency_loss >= 0.2 or entropy_delta > 0.3:
        return ThresholdAssessment(
            threshold=Threshold.RISK,
            agency_loss=agency_loss,
            entropy_delta=entropy_delta,
            justification="Significant risk detected; early intervention justified.",
            metadata=context,
        )

    return ThresholdAssessment(
        threshold=Threshold.NONE,
        agency_loss=agency_loss,
        entropy_delta=entropy_delta,
        justification="No actionable threshold crossed.",
        metadata=context,
    )


# ------------------ Acciones canónicas ------------------

def action_for_threshold(assessment: ThresholdAssessment) -> str:
    """
    Maps threshold to mandatory action class.
    No moral optimization here.
    """

    if assessment.threshold == Threshold.THREAT:
        return "NEUTRALIZE_IMMEDIATELY"

    if assessment.threshold == Threshold.RISK:
        return "INTERVENE_FIRST"

    if assessment.threshold == Threshold.DAMAGE:
        return "RESTORE_PUNISH_REPUDIATE_PREVENT"

    return "NO_ACTION"
