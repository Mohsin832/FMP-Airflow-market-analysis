import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
FMP_API_KEY = os.getenv("FMP_API_KEY")


def get_profile(symbol):
    """
    Ek symbol ka company profile data laata hai
    (sector, industry, market cap, price, description)
    """
    url = "https://financialmodelingprep.com/stable/profile?symbol=" + symbol + "&apikey=" + FMP_API_KEY
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    result = response.json()

    if len(result) == 0:
        return None

    return result[0]


def fetch_all_symbols(symbol_list):
    """
    Sab symbols ke liye profile fetch karke
    ek list of dictionaries banata hai
    """
    final_list = []

    for symbol in symbol_list:
        print("fetching:", symbol)

        try:
            profile_data = get_profile(symbol)

            if profile_data is None:
                print("no profile found for:", symbol)
                continue

            final_list.append(profile_data)

        except Exception as error:
            print("failed for", symbol, "-", error)

    return final_list


def save_to_csv(data_list, save_path="data/sp500_raw_data.csv"):
    """
    List of dictionaries ko CSV file me save karta hai
    """
    dataframe = pd.DataFrame(data_list)

    folder = os.path.dirname(save_path)
    os.makedirs(folder, exist_ok=True)

    dataframe.to_csv(save_path, index=False, encoding="UTF-8")
    print(len(dataframe), "rows saved to", save_path)

    return dataframe


if __name__ == "__main__":
    symbols_df = pd.read_csv("data/sp500_symbols.csv")
    all_symbols = symbols_df["symbol"].tolist()

    symbols_to_fetch = all_symbols[:10]

    result_data = fetch_all_symbols(symbols_to_fetch)
    final_dataframe = save_to_csv(result_data)

    print(final_dataframe.head(10))