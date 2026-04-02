from __future__ import annotations

import os


def env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


class RuntimeConfig:
    def __init__(self) -> None:
        self.enable_embeddings = env_bool("SER_ENABLE_EMBEDDINGS", False)
        self.default_admission_window_ms = int(os.getenv("SER_DEFAULT_ADMISSION_WINDOW_MS", "800"))
        self.default_similarity_threshold = float(os.getenv("SER_DEFAULT_SIMILARITY_THRESHOLD", "0.87"))
        self.window_ms_by_task_type = {
            "repo_scan": int(os.getenv("SER_REPO_SCAN_WINDOW_MS", "1100")),
            "code_search": int(os.getenv("SER_CODE_SEARCH_WINDOW_MS", "850")),
            "test_run": int(os.getenv("SER_TEST_RUN_WINDOW_MS", "450")),
            "doc_extract": int(os.getenv("SER_DOC_EXTRACT_WINDOW_MS", "900")),
            "api_call": int(os.getenv("SER_API_CALL_WINDOW_MS", "600")),
            "sql_query": int(os.getenv("SER_SQL_QUERY_WINDOW_MS", "500")),
            "nl_research_task": int(os.getenv("SER_NL_RESEARCH_TASK_WINDOW_MS", "900")),
        }
        self.threshold_by_task_type = {
            "repo_scan": float(os.getenv("SER_REPO_SCAN_SIMILARITY_THRESHOLD", "0.7")),
            "code_search": float(os.getenv("SER_CODE_SEARCH_SIMILARITY_THRESHOLD", "0.82")),
            "test_run": float(os.getenv("SER_TEST_RUN_SIMILARITY_THRESHOLD", "0.9")),
            "doc_extract": float(os.getenv("SER_DOC_EXTRACT_SIMILARITY_THRESHOLD", "0.78")),
            "api_call": float(os.getenv("SER_API_CALL_SIMILARITY_THRESHOLD", "0.88")),
            "sql_query": float(os.getenv("SER_SQL_QUERY_SIMILARITY_THRESHOLD", "0.93")),
            "nl_research_task": float(os.getenv("SER_NL_RESEARCH_TASK_SIMILARITY_THRESHOLD", "0.8")),
        }

    def admission_window_ms(self, task_type: str) -> int:
        return self.window_ms_by_task_type.get(task_type, self.default_admission_window_ms)

    def similarity_threshold(self, task_type: str) -> float:
        return self.threshold_by_task_type.get(task_type, self.default_similarity_threshold)
