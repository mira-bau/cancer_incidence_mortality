import pandas as pd
import cancer_measures.mapping as mapping

# Build alias-to-id lookup
ALIAS_TO_ID = {
    alias.lower(): entry["country_id"]
    for entry in mapping.COUNTRY_MAP
    for alias in [entry["standard_name"]] + entry["aliases"]
}

# Build id-to-standard name lookup
ID_TO_STANDARD_NAME = {
    entry["country_id"]: entry["standard_name"] for entry in mapping.COUNTRY_MAP
}

if __name__ == "__main__":
    # Load the dataset
    data = pd.read_csv("../raw/health_coverage.csv")

    # Normalize country names
    data["geo_name_lower"] = data["GEO_NAME_SHORT"].str.lower()

    # Map country_id using aliases
    data["country_id"] = data["geo_name_lower"].map(ALIAS_TO_ID).astype("Int64")

    # Filter only valid mappings
    data = data[data["country_id"].notna()]

    # Add standard country names and year
    data["country_name"] = data["country_id"].map(ID_TO_STANDARD_NAME)
    data["year"] = data["DIM_TIME"]
    data["uhc_index"] = data["INDEX_N"]

    # Select and rename columns
    data = data[["country_id", "country_name", "year", "uhc_index"]]

    # Save cleaned data
    data.to_csv("../processed/health_coverage.csv", index=False)
