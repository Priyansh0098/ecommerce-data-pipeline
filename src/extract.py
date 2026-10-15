import json
from datetime import datetime, timezone
from pathlib import Path

import requests
from logger_config import get_logger

logger = get_logger("extract")

API_URL = "https://fakestoreapi.com/products"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_FILE = RAW_DATA_DIR / "products.json"



def extract_products():
    try:
        RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

        logger.info("Fetching product data from API")

        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()

        products = response.json()

        if not isinstance(products, list):
            raise ValueError("Expected a list of products from the API")

        extracted_at = datetime.now(timezone.utc).isoformat()

        output = {
            "source": API_URL,
            "extracted_at": extracted_at,
            "record_count": len(products),
            "products": products,
        }

        with OUTPUT_FILE.open("w", encoding="utf-8") as file:
            json.dump(output, file, indent=2, ensure_ascii=False)

        logger.info("Records extracted: %s", len(products))
        logger.info("Saved raw data to: %s", OUTPUT_FILE)

    except (requests.RequestException, ValueError, OSError):
        logger.exception("Extraction failed")
        raise


if __name__ == "__main__":
    extract_products()
