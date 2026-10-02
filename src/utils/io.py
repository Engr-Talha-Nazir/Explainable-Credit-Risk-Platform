from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_config(config_path: str | Path) -> dict[str, Any]:
    """Load YAML configuration file."""
    path = Path(config_path)
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def save_config(config: dict[str, Any], config_path: str | Path) -> None:
    """Save configuration to YAML file."""
    path = Path(config_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(config, f, default_flow_style=False, sort_keys=False)
