
import json

import pandas as pd
import pytest
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from transform import transform_products
import transform
from src import transform


def test_transform_removes_duplicate_ids(tmp_path, monkeypatch):
    products = {
        "products": [
            {
                "id": 1,
                "title": "Product A",
                "price": 10.0,
                "category": "electronics",
                "rating": {"rate": 4.5, "count": 10},
            },
            {
                "id": 1,
                "title": "Product A Duplicate",
                "price": 12.0,
                "category": "electronics",
                "rating": {"rate": 4.0, "count": 5},
            },
        ]
    }

    input_file = tmp_path / "products.json"
    output_file = tmp_path / "products.csv"

    input_file.write_text(json.dumps(products), encoding="utf-8")

    monkeypatch.setattr(transform, "INPUT_FILE", input_file)
    monkeypatch.setattr(transform, "OUTPUT_FILE", output_file)

    transform.transform_products()

    result = pd.read_csv(output_file)

    assert len(result) == 1
    assert result["id"].tolist() == [1]


def test_transform_removes_negative_prices(tmp_path, monkeypatch):
    products = {
        "products": [
            {
                "id": 1,
                "title": "Valid Product",
                "price": 10.0,
                "category": "electronics",
                "rating": {"rate": 4.5, "count": 10},
            },
            {
                "id": 2,
                "title": "Invalid Product",
                "price": -5.0,
                "category": "electronics",
                "rating": {"rate": 4.0, "count": 5},
            },
        ]
    }

    input_file = tmp_path / "products.json"
    output_file = tmp_path / "products.csv"

    input_file.write_text(json.dumps(products), encoding="utf-8")

    monkeypatch.setattr(transform, "INPUT_FILE", input_file)
    monkeypatch.setattr(transform, "OUTPUT_FILE", output_file)

    transform.transform_products()

    result = pd.read_csv(output_file)

    assert len(result) == 1
    assert result["id"].tolist() == [1]
    assert (result["price"] >= 0).all()


def test_transform_rejects_missing_required_columns(
    tmp_path, monkeypatch
):
    products = {
        "products": [
            {
                "id": 1,
                "title": "Product A",
                "price": 10.0,
                # category intentionally missing
                "rating": {"rate": 4.5, "count": 10},
            }
        ]
    }

    input_file = tmp_path / "products.json"
    output_file = tmp_path / "products.csv"

    input_file.write_text(json.dumps(products), encoding="utf-8")

    monkeypatch.setattr(transform, "INPUT_FILE", input_file)
    monkeypatch.setattr(transform, "OUTPUT_FILE", output_file)

    with pytest.raises(ValueError, match="Missing required columns"):
        transform.transform_products()
