import pandas as pd
import os
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv

load_dotenv()

SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")


def connect_to_snowflake():
    """
    Snowflake ke sath connection banata hai
    """
    print("connecting to snowflake...")

    conn = snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE
    )

    print("connected successfully")
    return conn


def load_data(csv_path, table_name, schema_name="RAW"):
    """
    CSV file ko padh kar Snowflake ke table me load karta hai
    """
    # step 1: data padho
    dataframe = pd.read_csv(csv_path)
    print(len(dataframe), "rows loaded from", csv_path)

    # step 2: column names UPPERCASE me convert karo
    # (Snowflake normally uppercase column names expect karta hai)
    dataframe.columns = [col.upper() for col in dataframe.columns]

    # step 3: snowflake se connect karo
    conn = connect_to_snowflake()

    # step 4: data ko table me insert karo
    success, num_chunks, num_rows, output = write_pandas(
        conn=conn,
        df=dataframe,
        table_name=table_name,
        schema=schema_name,
        auto_create_table=True
    )

    print("upload success:", success)
    print("rows inserted:", num_rows)

    # step 5: connection band karo
    conn.close()
    print("connection closed")

    return success


if __name__ == "__main__":
    load_data(
        csv_path="data/sp500_clean_data.csv",
        table_name="SP500_COMPANY_PROFILE",
        schema_name="RAW"
    )