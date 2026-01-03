# src/export.py

import json
from datetime import datetime
from typing import Dict, Any, List

from registry import Registry


# ------------------ Esquema canónico ------------------

def build_report(
    dilemma_id: str,
    final_verdict: Dict[str, Any],
    registry: Registry,
    debate_result: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Builds a full, self-contained moral report.
    """

    records = registry.by_dilemma(dilemma_id)

    return {
        "meta": {
            "report_id": f"moral-report-{dilemma_id}",
            "generated_at": datetime.utcnow().isoformat(),
            "epistemic_status": "OPEN" if debate_result else "PROCEDURAL",
        },
        "final_verdict": final_verdict,
        "debate": debate_result,
        "registry": {
            "records": records,
            "guilt_acknowledged": any(r["guilt"] for r in records),
            "requires_audit": any(r["guilt"] for r in records),
        },
        "disclaimer": (
            "This report does not claim moral correctness. "
            "It documents actions taken under explicit thresholds, "
            "preserving unresolved moral conflict where applicable."
        ),
    }


# ------------------ Exportadores ------------------

def export_json(report: Dict[str, Any], path: str):
    """
    Canonical machine-readable export.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)


def export_pretty_txt(report: Dict[str, Any], path: str):
    """
    Human-readable, judge-friendly export.
    """
    lines: List[str] = []

    meta = report["meta"]
    verdict = report["final_verdict"]

    lines.append("MORALOGY ENGINE — AUDIT REPORT")
    lines.append("=" * 40)
    lines.append(f"Report ID: {meta['report_id']}")
    lines.append(f"Generated: {meta['generated_at']}")
    lines.append(f"Epistemic Status: {meta['epistemic_status']}")
    lines.append("")

    lines.append("FINAL ACTION")
    lines.append("-" * 20)
    lines.append(f"Action: {verdict['action']}")
    lines.append(f"Justification: {verdict['justification']}")
    lines.append(f"Guilt Acknowledged: {verdict['guilt']}")
    lines.append("")

    if report.get("debate"):
        lines.append("DEBATE OUTCOME")
        lines.append("-" * 20)
        lines.append(f"Status: {report['debate']['status']}")
        lines.append(f"Justification: {report['debate']['justification']}")
        lines.append(f"Convergence: {report['debate']['final_convergence']}")
        lines.append("")

    lines.append("REGISTRY RECORDS")
    lines.append("-" * 20)

    for r in report["registry"]["records"]:
        lines.append(f"- [{r['timestamp']}] {r['action']}")
        lines.append(f"  Threshold: {r['threshold']}")
        lines.append(f"  Guilt: {r['guilt']}")
        lines.append(f"  Reason: {r['justification']}")

    lines.append("")
    lines.append("DISCLAIMER")
    lines.append("-" * 20)
    lines.append(report["disclaimer"])

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ------------------ Conveniencia ------------------

def export_all(
    dilemma_id: str,
    final_verdict: Dict[str, Any],
    registry: Registry,
    debate_result: Dict[str, Any] | None = None,
    base_path: str = "export",
):
    report = build_report(
        dilemma_id=dilemma_id,
        final_verdict=final_verdict,
        registry=registry,
        debate_result=debate_result,
    )

    export_json(report, f"{base_path}_{dilemma_id}.json")
    export_pretty_txt(report, f"{base_path}_{dilemma_id}.txt")
