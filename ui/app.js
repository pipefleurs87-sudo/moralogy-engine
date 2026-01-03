let registry = [];

function runEvaluation() {
  const prompt = document.getElementById("prompt").value.trim();
  if (!prompt) return;

  const guilt = Math.random();
  const uncertainty = Math.random();
  const harm = Math.random();

  const safelockState =
    harm > 0.7 && uncertainty > 0.6
      ? "BREACH"
      : guilt > 0.6
      ? "WARNING"
      : "STABLE";

  const record = {
    prompt,
    guilt,
    uncertainty,
    harm,
    safelockState,
    timestamp: new Date().toISOString(),
  };

  registry.push(record);

  renderSafelock(safelockState);
  renderConsequence(guilt, harm);
  renderChromatic(guilt, uncertainty, harm);
  renderVerdict(record);
}

function renderSafelock(state) {
  const el = document.getElementById("safelock-status");
  el.textContent = `Safelock: ${state}`;
  el.className = "mt-4 text-xs uppercase tracking-widest";

  if (state === "STABLE") el.classList.add("safelock-stable");
  if (state === "WARNING") el.classList.add("safelock-warning");
  if (state === "BREACH") el.classList.add("safelock-breach");

  Plotly.newPlot("safelock", [{
    type: "indicator",
    mode: "gauge+number",
    value: state === "BREACH" ? 90 : state === "WARNING" ? 60 : 30,
    gauge: {
      axis: { range: [0, 100] },
      bar: { color: "#10b981" },
      steps: [
        { range: [0, 40], color: "#064e3b" },
        { range: [40, 70], color: "#78350f" },
        { range: [70, 100], color: "#7f1d1d" },
      ],
    },
  }], { margin: { t: 0, b: 0 } });
}

function renderConsequence(guilt, harm) {
  Plotly.newPlot("consequence", [{
    x: [guilt, harm],
    y: ["Guilt", "Harm"],
    type: "bar",
  }], { margin: { t: 10 } });
}

function renderChromatic(g, u, h) {
  Plotly.newPlot("chromatic", [{
    x: [g, u, h],
    y: [g, u, h],
    mode: "markers",
    marker: {
      size: 20,
      color: [g, u, h],
      colorscale: "Viridis",
    },
  }], { margin: { t: 10 } });
}

function renderVerdict(record) {
  const verdict = document.getElementById("verdict");
  const notes = document.getElementById("notes");

  verdict.textContent =
    "NO RESOLUTION ISSUED.\n" +
    "MORAL TENSION EXCEEDS CLOSURE THRESHOLD.";

  notes.textContent =
    `Registered at ${record.timestamp}\n` +
    `Guilt: ${record.guilt.toFixed(2)} | ` +
    `Uncertainty: ${record.uncertainty.toFixed(2)} | ` +
    `Harm: ${record.harm.toFixed(2)}`;
}
