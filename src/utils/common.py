import logging
from pathlib import Path


def setup_logging(level: int = logging.INFO) -> None:
    """Configure basic logging."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def ensure_dirs(dirs: list[Path]) -> None:
    """Ensure directories exist."""
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def get_project_root() -> Path:
    """Return project root directory."""
    return Path(__file__).resolve().parents[2]
