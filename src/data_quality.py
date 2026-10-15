
import os

import psycopg
from logger_config import get_logger

logger = get_logger("data_quality")


def check_data_quality():
    try:
        db_config = {
            "host": os.getenv("PGHOST", "localhost"),
            "port": os.getenv("PGPORT", "5432"),
            "dbname": os.getenv("PGDATABASE", "ecommerce_dw"),
            "user": os.getenv("PGUSER", "postgres"),
            "password": os.getenv("PGPASSWORD"),
        }

        if not db_config["password"]:
            raise ValueError("Please set PGPASSWORD first.")

        checks = {
            "Total products": """
                SELECT COUNT(*) FROM products
            """,
            "Duplicate product IDs": """
                SELECT COUNT(*) FROM (
                    SELECT id
                    FROM products
                    GROUP BY id
                    HAVING COUNT(*) > 1
                ) AS duplicates
            """,
            "Invalid prices": """
                SELECT COUNT(*) FROM products
                WHERE price < 0
            """,
            "Invalid ratings": """
                SELECT COUNT(*) FROM products
                WHERE rating < 0 OR rating > 5
            """,
            "Missing required fields": """
                SELECT COUNT(*) FROM products
                WHERE id IS NULL
                   OR title IS NULL
                   OR price IS NULL
                   OR category IS NULL
            """,
        }

        failed_checks = []

        logger.info("Starting data quality checks")

        with psycopg.connect(**db_config) as conn:
            with conn.cursor() as cur:
                for name, query in checks.items():
                    cur.execute(query)
                    result = cur.fetchone()[0]

                    if name == "Total products":
                        print(f"{name}: {result}")
                        logger.info("%s: %s", name, result)

                    elif result == 0:
                        print(f"PASS - {name}: {result}")
                        logger.info("PASS - %s: %s", name, result)

                    else:
                        print(f"FAIL - {name}: {result}")
                        logger.error("FAIL - %s: %s", name, result)
                        failed_checks.append(name)

        if failed_checks:
            raise ValueError(
                f"Data quality checks failed: {', '.join(failed_checks)}"
            )

        logger.info("All data quality checks passed")

    except (psycopg.Error, ValueError):
        logger.exception("Data quality validation failed")
        raise


if __name__ == "__main__":
    check_data_quality()
