const metricsGrid = document.getElementById("metricsGrid");
const taskStream = document.getElementById("taskStream");
const seuGrid = document.getElementById("seuGrid");
const apiBaseInput = document.getElementById("apiBase");
const taskCount = document.getElementById("taskCount");
const seuCount = document.getElementById("seuCount");

const decisionLabels = {
  representative: "representative task",
  exact_structural_hash: "collapsed by exact structural hash",
  semantic_similarity: "collapsed by semantic overlap",
  exact_only_task_type: "kept separate by exact-only safety rule",
  similar_but_below_threshold: "kept separate below overlap threshold",
  no_candidate: "no pending SEU candidate",
  new_seu: "new shared execution unit created",
};

function apiBase() {
  return apiBaseInput.value.replace(/\/$/, "");
}

async function call(path, options = {}) {
  const response = await fetch(`${apiBase()}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  return response.json();
}

function renderMetrics(metrics) {
  const entries = [
    ["Tasks received", metrics.total_tasks_received],
    ["SEUs created", metrics.unique_seus_created],
    ["Collapsed tasks", metrics.collapsed_tasks],
    ["Executions saved", metrics.executions_saved],
    ["Dedup multiplier", metrics.deduplication_multiplier],
    ["Safety rejections", metrics.false_collapse_rejections],
    ["Mean latency (ms)", metrics.latency_mean_ms],
    ["Saved backend work (ms)", metrics.estimated_backend_work_saved_ms],
  ];
  metricsGrid.innerHTML = entries.map(([label, value]) => `
    <article class="metric-card">
      <span>${label}</span>
      <strong>${value}</strong>
    </article>
  `).join("");
}

function renderTasks(tasks) {
  taskCount.textContent = `${tasks.length} tasks`;
  taskStream.innerHTML = tasks.slice().reverse().map(task => `
    <article class="task-card">
      <div class="panel-head">
        <strong>${task.task_id}</strong>
        <span class="pill">${task.task_type}</span>
      </div>
      <div class="meta">${task.agent_id} · ${task.branch_id} · ${task.resource_hint}</div>
      <div class="decision">decision: ${decisionLabels[task.collapse_reason] || task.collapse_reason}</div>
      <pre>${JSON.stringify(task.payload, null, 2)}</pre>
    </article>
  `).join("");
}

function renderSeus(seus) {
  seuCount.textContent = `${seus.length} SEUs`;
  const now = Date.now();
  seuGrid.innerHTML = seus.slice().reverse().map(seu => {
    const deadline = new Date(seu.admission_deadline).getTime();
    const created = new Date(seu.created_at).getTime();
    const totalWindow = Math.max(deadline - created, 1);
    const remaining = Math.max(deadline - now, 0);
    const width = seu.status === "PENDING" ? Math.max((remaining / totalWindow) * 100, 0) : 0;
    const reasons = Object.entries(seu.collapse_reasons)
      .map(([taskId, reason]) => `${taskId} -> ${decisionLabels[reason] || reason}`)
      .join(" | ");
    const subscriberCount = seu.subscriber_details.length;
    return `
      <article class="seu-card">
        <div class="panel-head">
          <div>
            <strong>${seu.seu_id}</strong>
            <div class="meta">${seu.task_type} · ${seu.canonical_key}</div>
          </div>
          <span class="pill status-${seu.status}">${seu.status}</span>
        </div>
        <div class="meta">representative: ${seu.representative_task_id} · subscribers: ${subscriberCount}</div>
        <div class="decision">why collapsed: ${reasons}</div>
        <div class="countdown" title="Admission window remaining">
          <div style="width:${width}%"></div>
        </div>
        <div class="subscribers">
          ${seu.subscriber_details.map(sub => `<div class="subscriber"><strong>${sub.task_id}</strong><br /><small>${sub.agent_id} · ${sub.branch_id}</small></div>`).join("")}
        </div>
        <pre>${JSON.stringify(seu.result || { note: "Awaiting execution or still in flight." }, null, 2)}</pre>
      </article>
    `;
  }).join("");
}

async function refresh() {
  try {
    const state = await call("/state");
    renderMetrics(state.metrics);
    renderTasks(state.tasks);
    renderSeus(state.seus);
  } catch (error) {
    metricsGrid.innerHTML = `<article class="metric-card"><span>Runtime status</span><strong>offline</strong></article>`;
  }
}

document.querySelectorAll("[data-scenario]").forEach(button => {
  button.addEventListener("click", async () => {
    await call(`/demo/${button.dataset.scenario}`, { method: "POST" });
    await refresh();
  });
});

document.getElementById("resetBtn").addEventListener("click", async () => {
  await call("/reset", { method: "POST" });
  await refresh();
});

refresh();
setInterval(refresh, 1200);
