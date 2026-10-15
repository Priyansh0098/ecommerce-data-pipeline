
import subprocess
import sys
from pathlib import Path

from src.logger_config import get_logger

PROJECT_ROOT = Path(__file__).resolve().parent
PYTHON = sys.executable
logger = get_logger("pipeline")

SCRIPTS = [
    "src/extract.py",
    "src/transform.py",
    "src/load.py",
    "src/data_quality.py",
]


def run_pipeline():
    print("=" * 45)
    print("ECOMMERCE ETL PIPELINE STARTED")
    print("=" * 45)

    logger.info("ETL pipeline started")

    for script in SCRIPTS:
        print(f"\n>>> Running {script}")
        logger.info("Running stage: %s", script)

        try:
            subprocess.run(
                [PYTHON, str(PROJECT_ROOT / script)],
                cwd=PROJECT_ROOT,
                check=True,
            )

            print(f">>> Completed {script}")
            logger.info("Completed stage: %s", script)

        except subprocess.CalledProcessError:
            logger.exception("Pipeline stage failed: %s", script)
            raise

    print("\n" + "=" * 45)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 45)

    logger.info("ETL pipeline completed successfully")


if __name__ == "__main__":
    try:
        run_pipeline()

    except subprocess.CalledProcessError as error:
        failed_script = Path(error.cmd[-1]).name
        print(f"\nPIPELINE FAILED: {failed_script}")
        logger.error("Pipeline failed at script: %s", failed_script)
        sys.exit(1)

    except Exception:
        logger.exception("Unexpected pipeline failure")
        print("\nPIPELINE FAILED: Unexpected error")
        sys.exit(1)
