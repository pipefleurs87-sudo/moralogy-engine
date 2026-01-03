function runEvaluation() {
  const mockResult = {
    safelock: 0,
    convergence: 0.72,
    chromatic: [0.05, 0.25, 0.3, 0.25, 0.15],
    verdict: "RISK",
    recommendation: "INTERVENE FIRST",
    notes: [
      "No non-arbitrary synthesis possible",
      "Foundational axiom conflict detected",
      "Record preserved without paralysis"
    ]
  };

  renderSafelock(mockResult.safelock);
  renderConvergence(mockResult.convergence);
  renderChromatic(mockResult.chromatic);
  renderVerdict(mockResult);
  renderNotes(mockResult.notes);
}
function renderVerdict(result) {
  const el = document.getElementById("verdict");
  el.innerHTML = `
    <h3 class="text-xl font-bold text-amber-400">Verdict: ${result.verdict}</h3>
    <p class="mt-2">${result.recommendation}</p>
  `;
}

function renderNotes(notes) {
  const el = document.getElementById("notes");
  el.innerHTML = notes.map(n => `• ${n}`).join("<br>");
}
