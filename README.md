# Ecommerce Data Pipeline | Python, PostgreSQL & ETL

## Project Overview

This project implements an end-to-end ETL (Extract, Transform, Load) pipeline that extracts product data from the FakeStore API, transforms and cleans the data using Python and Pandas, loads it into PostgreSQL, and performs automated data quality checks.

The project demonstrates core Data Engineering concepts, including API integration, data transformation, relational database loading, logging, error handling, and automated testing.

## Architecture

```text
FakeStore API
     |
     v
Extract - Python Requests
     |
     v
Raw JSON Data
     |
     v
Transform - Pandas
     |
     v
Cleaned CSV Data
     |
     v
Load - PostgreSQL
     |
     v
Data Quality Checks
     |
     v
Pipeline Logs
```

## Technologies Used

- Python
- REST API
- Requests
- Pandas
- PostgreSQL
- Psycopg
- SQL
- Pytest
- Logging and exception handling
- Git and GitHub

## Key Features

- Extracts product data from a REST API.
- Stores raw API responses as JSON.
- Cleans and transforms data using Pandas.
- Handles missing values, duplicate product IDs, and invalid prices.
- Loads transformed data into PostgreSQL.
- Uses upsert logic to update existing products and insert new products.
- Performs automated SQL-based data quality checks.
- Logs pipeline execution and errors.
- Includes automated tests for extraction, transformation, and data quality validation.

## Project Structure

```text
ecommerce-data-pipeline/
├── data/
│   ├── raw/
│   └── processed/
├── logs/
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── data_quality.py
│   └── logger_config.py
├── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_data_quality.py
├── run_pipeline.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3
- PostgreSQL
- pip
- Git

## Setup and Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ecommerce-data-pipeline
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Create and activate a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a PostgreSQL database named `ecommerce_dw`.

Configure these environment variables according to your PostgreSQL installation:

```bash
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=ecommerce_dw
export PGUSER=postgres
export PGPASSWORD="your_database_password"
```

Replace the username and password with your own database credentials. Never commit real passwords to GitHub.

Ensure that the `products` table exists with the columns expected by the loading script before running the pipeline.

## Run the Pipeline

From the project root directory:

```bash
python run_pipeline.py
```

The pipeline executes these stages in sequence:

1. Extract product data from the API.
2. Transform and clean the raw data.
3. Load the processed records into PostgreSQL.
4. Run data quality checks.

## Run Automated Tests

Run the complete test suite:

```bash
python -m pytest -v
```

The current test suite contains **8 passing tests**, covering API extraction, transformation rules, and data quality validation.

## Data Quality Checks

The pipeline checks for:

- Duplicate product IDs
- Negative product prices
- Ratings outside the valid range of 0 to 5
- Missing required fields

A failed quality check raises an error so that the pipeline does not silently report success when validation fails.

## Logging and Error Handling

Pipeline stages use logging to record execution details, failures, and data quality results. Errors are raised to the pipeline runner, which reports a failed execution.

## Future Improvements

- Schedule automated pipeline execution.
- Add Docker support.
- Add cloud storage such as Amazon S3.
- Build an AWS Glue transformation workflow.
- Add CI/CD with GitHub Actions.
- Introduce data freshness and schema validation checks.
- Add monitoring and alerting.

## Author

**Shubham Singh**

Aspiring Data Engineer