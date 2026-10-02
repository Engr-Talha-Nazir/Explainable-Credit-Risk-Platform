# Basic tests
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


def test_health_import():
    from api import main

    assert hasattr(main, "app")


def test_seed_reproducible():
    from utils import seed

    seed.set_seed(42)


def test_project_structure():
    root = Path(__file__).resolve().parents[1]
    assert (root / "README.md").exists()
    assert (root / "LICENSE").exists()
    assert (root / "pyproject.toml").exists()
    assert (root / "requirements.txt").exists()
