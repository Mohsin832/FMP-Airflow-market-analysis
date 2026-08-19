from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Python dummy/placeholder functions for pipeline tasks
def extract_sp500_symbols():
    print("Extracting S&P 500 symbols...")

def fetch_market_data():
    print("Fetching market data from FMP API...")

def transform_data():
    print("Cleaning and transforming data with Pandas...")

def load_to_snowflake():
    print("Loading final processed data into Snowflake...")

# DAG Definition using updated 'schedule' parameter
with DAG(
    'sp500_market_data_pipeline',
    default_args=default_args,
    description='Pipeline for S&P 500 market data processing and loading to Snowflake',
    schedule='@daily',  # Updated from schedule_interval
    catchup=False,
    tags=['sp500', 'fmp', 'snowflake'],
) as dag:

    task_extract = PythonOperator(
        task_id='extract_symbols',
        python_callable=extract_sp500_symbols,
    )

    task_fetch = PythonOperator(
        task_id='fetch_market_data',
        python_callable=fetch_market_data,
    )

    task_transform = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
    )

    task_load = PythonOperator(
        task_id='load_to_snowflake',
        python_callable=load_to_snowflake,
    )

    # Task Dependencies Execution Flow
    task_extract >> task_fetch >> task_transform >> task_load