import json
from pathlib import Path
import pandas as pd
from src.logger_config import get_logger

logger = get_logger("transform")
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "products.json"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "products.csv"



def transform_products():
    try:
        logger.info("Reading raw product data")

        with INPUT_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict) or not isinstance(
            data.get("products"), list
        ):
            raise ValueError(
                "Invalid raw data: expected a products list"
            )

        df = pd.DataFrame(data["products"])

        required_columns = [
            "id", "title", "price", "category", "rating"
        ]
        missing_columns = [
            col for col in required_columns if col not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

        # Select required columns
        df = df[required_columns].copy()

        # Separate rating and rating count
        df["rating_count"] = df["rating"].apply(
            lambda x: x.get("count") if isinstance(x, dict) else None
        )
        df["rating"] = df["rating"].apply(
            lambda x: x.get("rate") if isinstance(x, dict) else x
        )

        # Clean text
        df["title"] = df["title"].astype("string").str.strip()
        df["category"] = df["category"].astype("string").str.strip()

        # Convert data types
        df["id"] = pd.to_numeric(df["id"], errors="coerce")
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
        df["rating_count"] = pd.to_numeric(
            df["rating_count"], errors="coerce"
        )

        # Remove invalid rows and duplicate product IDs
        df = df.dropna(subset=["id", "title", "price", "category"])
        df = df.drop_duplicates(subset=["id"])
        df = df[df["price"] >= 0]
        df = df[df["rating"].between(0, 5) | df["rating"].isna()]

        if df.empty:
            raise ValueError("No valid product records remain after cleaning")

        # Save cleaned data
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(OUTPUT_FILE, index=False)

        logger.info("Records after cleaning: %s", len(df))
        logger.info("Columns: %s", ", ".join(df.columns))
        logger.info("Saved to: %s", OUTPUT_FILE)
        logger.info("Preview:\n%s", df.head().to_string(index=False))

    except (OSError, json.JSONDecodeError, ValueError, KeyError, TypeError):
        logger.exception("Transformation failed")
        raise


if __name__ == "__main__":
    transform_products()