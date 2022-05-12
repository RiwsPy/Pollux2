from pathlib import Path
import pytest
from .base import LampsFactory

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = 'tests/fixtures'


@pytest.fixture
def base_dir() -> Path:
    return BASE_DIR


@pytest.fixture
def db_dir() -> str:
    return DB_DIR


@pytest.fixture
def lamp():
    return LampsFactory()
