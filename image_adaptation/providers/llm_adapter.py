from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class LLMAdapter:
    def __init__(self, config_path: Path | None = None) -> None:
        self.config = _load_config(config_path).get("llm", {}) if config_path else {}
        self.is_configured = bool(self.config.get("api_key") and self.config.get("model"))

    def plan_layout(self, manifest: Any) -> Any | None:
        """Return a LayoutPlan when a real LLM integration is implemented.

        The LLM must output coordinates only. It must not edit pixels or request
        product regeneration.
        """
        return None


def _load_config(config_path: Path | None) -> dict[str, Any]:
    if not config_path or not config_path.exists():
        return {}
    return json.loads(config_path.read_text(encoding="utf-8"))
