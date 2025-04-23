import pandas as pd

import mapping


if __name__ == "__main__":
    # Load the dataset
    data = pd.read_csv("raw/ALCOHOL.csv")

    # Extract numeric value before brackets from the 'Value' column
    data["alcohol_use"] = data["Value"].str.extract(r"^([\d.]+)")

    # Map country_id using alias mapping
    data["country_id"] = data["Location"].map(mapping.ALIAS_COUNTRY_MAP)

    # Add year from the Period column
    data["year"] = data["Period"]

    # Filter valid rows
    data = data[data["country_id"].notna()]

    # Select and rename columns
    data = data[["country_id", "Location", "year", "alcohol_use"]]
    data.columns = ["country_id", "country_name", "year", "alcohol_use"]

    # Export cleaned data
    data.to_csv("processed/alcohol_use.csv", index=False)
