
import json

import pytest
import requests

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import extract


class FakeResponse:
    def __init__(self, data):
        self.data = data

    def raise_for_status(self):
        pass

    def json(self):
        return self.data


def test_extract_saves_products(tmp_path, monkeypatch):
    products = [
        {
            "id": 1,
            "title": "Test Product",
            "price": 10.0,
            "category": "electronics",
            "rating": {"rate": 4.5, "count": 10},
        }
    ]

    output_file = tmp_path / "products.json"

    monkeypatch.setattr(extract, "RAW_DATA_DIR", tmp_path)
    monkeypatch.setattr(extract, "OUTPUT_FILE", output_file)
    monkeypatch.setattr(
        extract.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(products),
    )

    extract.extract_products()

    saved_data = json.loads(output_file.read_text(encoding="utf-8"))

    assert saved_data["record_count"] == 1
    assert saved_data["products"][0]["title"] == "Test Product"


def test_extract_rejects_invalid_response(tmp_path, monkeypatch):
    output_file = tmp_path / "products.json"

    monkeypatch.setattr(extract, "RAW_DATA_DIR", tmp_path)
    monkeypatch.setattr(extract, "OUTPUT_FILE", output_file)
    monkeypatch.setattr(
        extract.requests,
        "get",
        lambda *args, **kwargs: FakeResponse({"error": "bad response"}),
    )

    with pytest.raises(ValueError, match="Expected a list"):
        extract.extract_products()


def test_extract_handles_api_failure(tmp_path, monkeypatch):
    def fail_request(*args, **kwargs):
        raise requests.ConnectionError("Test connection failure")

    monkeypatch.setattr(extract, "RAW_DATA_DIR", tmp_path)
    monkeypatch.setattr(
        extract.requests, "get", fail_request
    )

    with pytest.raises(requests.ConnectionError):
        extract.extract_products()
