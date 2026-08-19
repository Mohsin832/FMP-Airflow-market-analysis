import pandas as pd
import os


def load_raw_data(input_path="data/sp500_raw_data.csv"):
    """
    Raw CSV file ko padhta hai
    """
    dataframe = pd.read_csv(input_path)
    print("raw data loaded:", len(dataframe), "rows")
    return dataframe


def select_useful_columns(dataframe):
    """
    Sirf wo columns rakhta hai jo hume chahiye,
    baaki extra columns hata deta hai
    """
    columns_to_keep = [
        "symbol",
        "companyName",
        "sector",
        "industry",
        "price",
        "marketCap",
        "beta",
        "volume",
        "exchange",
        "country",
        "currency",
        "ipoDate"
    ]

    # sirf wo columns rakho jo actually dataframe me maujood hain
    available_columns = []
    for col in columns_to_keep:
        if col in dataframe.columns:
            available_columns.append(col)

    dataframe = dataframe[available_columns]
    print("columns selected:", available_columns)
    return dataframe


def remove_missing_and_duplicates(dataframe):
    """
    Missing symbol/price wali rows hataata hai
    aur duplicate symbols bhi hataata hai
    """
    before = len(dataframe)

    # jin rows me symbol ya price missing hai unhe hatao
    dataframe = dataframe.dropna(subset=["symbol", "price"])

    # agar same symbol do baar aaya ho to duplicate hatao
    dataframe = dataframe.drop_duplicates(subset=["symbol"])

    after = len(dataframe)
    print("removed", before - after, "rows (missing/duplicate)")

    return dataframe


def fix_data_types(dataframe):
    """
    Numeric columns ko sahi type me convert karta hai
    """
    numeric_columns = ["price", "marketCap", "beta", "volume"]

    for col in numeric_columns:
        if col in dataframe.columns:
            dataframe[col] = pd.to_numeric(dataframe[col], errors="coerce")

    return dataframe


def remove_invalid_values(dataframe):
    """
    Galat/impossible values wali rows hataata hai
    (jaise price 0 ya negative)
    """
    before = len(dataframe)

    dataframe = dataframe[dataframe["price"] > 0]

    after = len(dataframe)
    print("removed", before - after, "rows (invalid price)")

    return dataframe


def save_clean_data(dataframe, output_path="data/sp500_clean_data.csv"):
    """
    Clean data ko naye CSV file me save karta hai
    """
    folder = os.path.dirname(output_path)
    os.makedirs(folder, exist_ok=True)

    dataframe.to_csv(output_path, index=False, encoding="UTF-8")
    print(len(dataframe), "clean rows saved to", output_path)

    return dataframe


if __name__ == "__main__":
    # step 1: raw data load karo
    df = load_raw_data()

    # step 2: sirf useful columns rakho
    df = select_useful_columns(df)

    # step 3: missing/duplicate rows hatao
    df = remove_missing_and_duplicates(df)

    # step 4: data types fix karo
    df = fix_data_types(df)

    # step 5: invalid values hatao
    df = remove_invalid_values(df)

    # step 6: clean CSV save karo
    df = save_clean_data(df)

    # step 7: result dikhao
    print(df.head(10))