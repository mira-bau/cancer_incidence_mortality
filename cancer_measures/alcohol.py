import pandas as pd
import mapping

# Build alias-to-id lookup
ALIAS_TO_ID = {
    alias: entry["country_id"]
    for entry in mapping.COUNTRY_MAP
    for alias in [entry["standard_name"]] + entry["aliases"]
}

# Build id-to-standard name lookup
ID_TO_STANDARD_NAME = {
    entry["country_id"]: entry["standard_name"] for entry in mapping.COUNTRY_MAP
}


if __name__ == "__main__":
    # Load the dataset
    data = pd.read_csv("raw/ALCOHOL.csv")

    # Extract numeric value before brackets from the 'Value' column
    data["alcohol_use"] = data["Value"].str.extract(r"^([\d.]+)")

    # Map country_id using aliases
    data["country_id"] = data["Location"].map(ALIAS_TO_ID).astype("Int64")

    # Filter only valid mappings
    data = data[data["country_id"].notna()]

    # Add standard country names and year
    data["country_name"] = data["country_id"].map(ID_TO_STANDARD_NAME)
    data["year"] = data["Period"]

    # Select and rename columns
    data = data[["country_id", "country_name", "year", "alcohol_use"]]

    # Export cleaned data
    data.to_csv("processed/alcohol_use.csv", index=False)
