import pandas as pd

# apni 4 scripts se functions import karo
from scripts.get_sp500_symbols import get_sp500_symbols
from scripts.get_fmp_data import fetch_all_symbols, save_to_csv
from scripts.data_processing import (
    load_raw_data,
    select_useful_columns,
    remove_missing_and_duplicates,
    fix_data_types,
    remove_invalid_values,
    save_clean_data
)
from scripts.load_to_snowflake import load_data


def run_pipeline(limit=10):
    """
    Poora pipeline ek ke baad ek chalata hai:
    symbols -> fetch -> clean -> load
    """

    print("========== STEP 1: GET SYMBOLS ==========")
    symbols_df = get_sp500_symbols()
    all_symbols = symbols_df["symbol"].tolist()

    # testing ke liye limit use karo (default 10)
    symbols_to_fetch = all_symbols[:limit]

    print("\n========== STEP 2: FETCH FMP DATA ==========")
    raw_data = fetch_all_symbols(symbols_to_fetch)
    save_to_csv(raw_data)

    print("\n========== STEP 3: CLEAN DATA ==========")
    df = load_raw_data()
    df = select_useful_columns(df)
    df = remove_missing_and_duplicates(df)
    df = fix_data_types(df)
    df = remove_invalid_values(df)
    save_clean_data(df)

    print("\n========== STEP 4: LOAD TO SNOWFLAKE ==========")
    load_data(
        csv_path="data/sp500_clean_data.csv",
        table_name="SP500_COMPANY_PROFILE",
        schema_name="RAW"
    )

    print("\n========== PIPELINE COMPLETE ==========")


if __name__ == "__main__":
    run_pipeline(limit=10)