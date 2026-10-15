import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import data_quality


class FakeCursor:
    def __init__(self, results):
        self.results = iter(results)

    def execute(self, query):
        pass

    def fetchone(self):
        return (next(self.results),)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class FakeConnection:
    def __init__(self, results):
        self.results = results

    def cursor(self):
        return FakeCursor(self.results)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


def test_quality_checks_pass_with_valid_data(monkeypatch):
    monkeypatch.setenv("PGPASSWORD", "test_password")
    monkeypatch.setattr(
        data_quality.psycopg,
        "connect",
        lambda **kwargs: FakeConnection([3, 0, 0, 0, 0])
    )

    data_quality.check_data_quality()


def test_quality_checks_fail_when_duplicates_exist(monkeypatch):
    monkeypatch.setenv("PGPASSWORD", "test_password")
    monkeypatch.setattr(
        data_quality.psycopg,
        "connect",
        lambda **kwargs: FakeConnection([3, 1, 0, 0, 0])
    )

    with pytest.raises(ValueError, match="Duplicate product IDs"):
        data_quality.check_data_quality()
