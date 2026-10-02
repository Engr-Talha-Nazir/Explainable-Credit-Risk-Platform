from pathlib import Path

from api import main
from utils import seed


def test_health_import() -> None:
    assert hasattr(main, "app")


def test_seed_reproducible() -> None:
    seed.set_seed(42)


def test_project_structure() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (root / "README.md").exists()
    assert (root / "LICENSE").exists()
    assert (root / "pyproject.toml").exists()
    assert (root / "requirements.txt").exists()
