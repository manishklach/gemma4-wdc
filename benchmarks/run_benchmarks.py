from __future__ import annotations

import asyncio
import json
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
BACKEND_ROOT = REPO_ROOT / "runtime" / "shared_execution" / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.core.runtime import SharedExecutionRuntime
from app.models.task import TaskSubmission

RESULTS_PATH = ROOT / "results" / "latest_summary.json"
SUMMARY_PATH = ROOT / "results" / "summary.md"


def load_scenario(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def task_from_dict(task: dict[str, Any]) -> TaskSubmission:
    payload = deepcopy(task)
    if "created_at" not in payload:
        payload["created_at"] = datetime.now(timezone.utc).isoformat()
    return TaskSubmission.model_validate(payload)


async def run_shared(tasks: list[dict[str, Any]]) -> dict[str, Any]:
    runtime = SharedExecutionRuntime()
    for task in tasks:
        await runtime.submit_task(task_from_dict(task))
    await asyncio.sleep(1.6)
    state = await runtime.state()
    actual_collapsed = state.metrics["collapsed_tasks"]
    expected_groups: dict[str, list[str]] = {}
    for task in tasks:
        group = task.get("expected_group")
        if group:
            expected_groups.setdefault(group, []).append(task["task_id"])
    expected_collapsible_pairs = sum(max(len(group) - 1, 0) for group in expected_groups.values())
    true_positive_collapses = 0
    false_positive_collapses = 0
    for seu in state.seus:
        representative_group = next(
            (task.get("expected_group") for task in tasks if task["task_id"] == seu.representative_task_id),
            None,
        )
        for subscriber_id in seu.subscribers[1:]:
            subscriber_group = next(
                (task.get("expected_group") for task in tasks if task["task_id"] == subscriber_id),
                None,
            )
            if representative_group and representative_group == subscriber_group:
                true_positive_collapses += 1
            else:
                false_positive_collapses += 1
    collapse_precision = round(true_positive_collapses / actual_collapsed, 2) if actual_collapsed else 1.0
    false_collapse_rate = round(false_positive_collapses / actual_collapsed, 2) if actual_collapsed else 0.0
    latency_proxy_ms = state.metrics["backend_work_ms"]
    return {
        "total_tasks": len(tasks),
        "total_executions": len(state.seus),
        "executions_saved": state.metrics["executions_saved"],
        "dedup_ratio": round((len(tasks) / len(state.seus)), 2) if state.seus else 1.0,
        "collapse_precision": collapse_precision,
        "false_collapse_rate": false_collapse_rate,
        "expected_collapsible_pairs": expected_collapsible_pairs,
        "latency_proxy_ms": latency_proxy_ms,
        "metrics": state.metrics,
    }


def run_naive(tasks: list[dict[str, Any]]) -> dict[str, Any]:
    latency_proxy_ms = len(tasks) * 160
    return {
        "total_tasks": len(tasks),
        "total_executions": len(tasks),
        "executions_saved": 0,
        "dedup_ratio": 1.0,
        "collapse_precision": 1.0,
        "false_collapse_rate": 0.0,
        "latency_proxy_ms": latency_proxy_ms,
    }


def render_summary(result: dict[str, Any]) -> str:
    lines = [
        "# Benchmark Summary",
        "",
        "Generated from the current local benchmark run for Gemma4-WDC.",
        "",
        "| Scenario | Tasks Requested | Actual Executions | Executions Saved | Dedup Ratio | Latency Proxy Delta | False-Collapse Rate |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name, summary in result["results"].items():
        naive = summary["naive"]
        shared = summary["gemma4_wdc"]
        delta = naive["latency_proxy_ms"] - shared["latency_proxy_ms"]
        lines.append(
            f"| `{name}` | {shared['total_tasks']} | {shared['total_executions']} | {shared['executions_saved']} | "
            f"{shared['dedup_ratio']}x | {delta} ms | {shared['false_collapse_rate']:.2f} |"
        )
    lines.extend(
        [
            "",
            "Notes:",
            "",
            "- these are preliminary laptop-scale numbers from hand-authored scenarios",
            "- latency proxy is only a local comparative signal, not a production latency claim",
            "- mock or lightweight executors are used throughout the current harness",
            "- the safety scenario remaining at zero saved executions is an expected positive signal",
        ]
    )
    return "\n".join(lines) + "\n"


async def benchmark() -> dict[str, Any]:
    summaries = {}
    for scenario_file in sorted(ROOT.glob("scenarios/*/tasks.json")):
        scenario_name = scenario_file.parent.name
        scenario = load_scenario(scenario_file)
        tasks = scenario["tasks"]
        shared = await run_shared(tasks)
        naive = run_naive(tasks)
        summaries[scenario_name] = {
            "description": scenario["description"],
            "naive": naive,
            "gemma4_wdc": shared,
        }
    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "benchmark_version": "0.2.0",
        "results": summaries,
    }
    RESULTS_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    SUMMARY_PATH.write_text(render_summary(result), encoding="utf-8")
    return result


if __name__ == "__main__":
    report = asyncio.run(benchmark())
    print(json.dumps(report, indent=2))
