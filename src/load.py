
import os
from pathlib import Path

import pandas as pd
import psycopg
from src.logger_config import get_loggers

logger = get_logger("load")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_FILE = PROJECT_ROOT / "data" / "processed" / "products.csv"


def load_products():
    try:
        logger.info("Reading transformed CSV")

        df = pd.read_csv(CSV_FILE)

        db_config = {
            "host": os.getenv("PGHOST", "localhost"),
            "port": os.getenv("PGPORT", "5432"),
            "dbname": os.getenv("PGDATABASE", "ecommerce_dw"),
            "user": os.getenv("PGUSER", "postgres"),
            "password": os.getenv("PGPASSWORD"),
        }

        if not db_config["password"]:
            raise ValueError(
                "Set the PGPASSWORD environment variable before running."
            )

        insert_sql = """
            INSERT INTO products
                (id, title, price, category, rating, rating_count)
            VALUES
                (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                title = EXCLUDED.title,
                price = EXCLUDED.price,
                category = EXCLUDED.category,
                rating = EXCLUDED.rating,
                rating_count = EXCLUDED.rating_count;
        """

        records = [
            (
                int(row.id),
                row.title,
                float(row.price),
                row.category,
                None if pd.isna(row.rating) else float(row.rating),
                None if pd.isna(row.rating_count)
                else int(row.rating_count),
            )
            for row in df.itertuples(index=False)
        ]

        logger.info(
            "Loading %s products into PostgreSQL", len(records)
        )

        with psycopg.connect(**db_config) as conn:
            with conn.cursor() as cur:
                cur.executemany(insert_sql, records)

                cur.execute("SELECT COUNT(*) FROM products")
                count = cur.fetchone()[0]

        logger.info(
            "Load complete! Total rows in products table: %s", count
        )

    except (OSError, ValueError, pd.errors.ParserError,
            psycopg.Error):
        logger.exception("Loading failed")
        raise


if __name__ == "__main__":
    load_products()
