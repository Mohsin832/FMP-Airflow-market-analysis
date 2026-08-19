# S&P 500 Market Data Analysis Pipeline

An automated ETL pipeline built with **Apache Airflow, Docker, Python, Pandas, FMP API, and Snowflake**. It extracts S&P 500 market data, transforms it with Pandas, and loads it into Snowflake.

## Architecture

```text
Wikipedia / FMP API
        ↓
   Apache Airflow
        ↓
   Python + Pandas
        ↓
     Snowflake
```

## Tech Stack

* **Python & Pandas** — Data extraction and transformation
* **FMP API** — Market data
* **Apache Airflow** — Pipeline orchestration
* **Docker & Docker Compose** — Containerization
* **Snowflake** — Data warehouse

## Project Structure

```text
├── dags/                    # Airflow DAGs
├── scripts/                 # ETL scripts
├── docker-compose.yaml      # Docker configuration
├── requirements.txt         # Python dependencies
├── .env                     # API and Snowflake credentials
└── README.md
```

## Requirements

* Git
* Docker & Docker Compose
* Python 3.10+
* FMP API key
* Snowflake account

## Setup

### 1. Clone the project

```bash
git clone https://github.com/YOUR_USERNAME/FMP-Airflow-market-analysis.git
cd FMP-Airflow-market-analysis
```

### 2. Configure `.env`

Create `.env` in the project root:

```env
AIRFLOW_UID=50000
FMP_API_KEY=your_fmp_api_key
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
```

**Do not commit `.env` to GitHub.**

### 3. Start Airflow

```bash
docker compose up -d
docker compose ps
```

### 4. Open Airflow

Go to:

```text
http://localhost:8080
```

Default login:

```text
Username: airflow
Password: airflow
```

For GitHub Codespaces, open the forwarded **Port 8080**.

## Run the Pipeline

1. Open the Airflow UI.
2. Find `sp500_market_data_pipeline`.
3. Turn the DAG **ON**.
4. Click **Trigger DAG**.
5. Monitor the tasks and logs.
6. Check the processed data in Snowflake.

Pipeline flow:

```text
Get S&P 500 Symbols
        ↓
Extract Market Data
        ↓
Transform with Pandas
        ↓
Load into Snowflake
```

## Useful Commands

```bash
# Check containers
docker compose ps

# View scheduler logs
docker compose logs airflow-scheduler --tail 50

# Restart
docker compose down
docker compose up -d

# Stop
docker compose down
```

## Troubleshooting

If the DAG does not appear, check the scheduler logs:

```bash
docker compose logs airflow-scheduler --tail 100
```

If you get an FMP or Snowflake connection error, verify the credentials in `.env`.

## Author

**Muhammad Mohsin**

Data Engineering project using **Python, Airflow, Docker, Pandas, APIs, and Snowflake**.
