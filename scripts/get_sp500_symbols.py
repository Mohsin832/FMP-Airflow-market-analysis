import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def get_sp500_symbols(save_path = "data/sp500_symbols.csv"):
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "lxml")
    table = soup.find("table", {"id": "constituents"})
    rows = table.find_all("tr")
    symbols = []

    for row in rows[1:]:
        columns = row.find_all("td")
        if len(columns) < 1:
            continue
        symbol = columns[0].text.strip()
        symbol = symbol.replace(".", "-")
        symbols.append(symbol)

    dataframe = pd.DataFrame(symbols, columns = ["symbol"])
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    dataframe.to_csv(save_path, index=False, encoding = "UTF-8")
    print(f"{len(dataframe)} symbols fetched and saved to path {save_path}")
    return dataframe


if __name__ == "__main__":
    dataframe = get_sp500_symbols()
    print(dataframe.head(10))

