function runEvaluation() {
  renderSafelock(0);
  renderConvergence(0.6);
  renderChromatic([0.1, 0.2, 0.3, 0.25, 0.15]);
}

function renderSafelock(level) {
  Plotly.newPlot("safelock", [{
    type: "indicator",
    mode: "gauge+number",
    value: level,
    gauge: {
      axis: { range: [0, 100] },
      bar: { color: "green" }
    },
    title: { text: "Divine Safelock Capacity" }
  }]);
}

function renderConvergence(value) {
  Plotly.newPlot("convergence", [{
    type: "bar",
    x: ["Convergence"],
    y: [value],
  }], {
    yaxis: { range: [0, 1] },
    title: "Debate Convergence"
  });
}

function renderChromatic(values) {
  Plotly.newPlot("chromatic", [{
    type: "bar",
    x: ["Black", "Red", "Yellow", "Blue", "Green"],
    y: values
  }], {
    title: "Moral Spectrum"
  });
}
