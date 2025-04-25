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
    df = pd.read_csv("../raw/gdp.csv", skiprows=4)

    # Keep only columns from 2000 to 2024
    year_columns = [str(year) for year in range(2000, 2025)]
    df = df[["Country Name"] + year_columns]

    # Normalize country names
    df["country_lower"] = df["Country Name"].str.lower()
    df["country_id"] = df["country_lower"].map(ALIAS_TO_ID).astype("Int64")

    # Filter out rows without matching country_id
    df = df[df["country_id"].notna()]

    # Add standard country name
    df["country_name"] = df["country_id"].map(ID_TO_STANDARD_NAME)

    # Reshape the dataframe
    df = df.melt(
        id_vars=["country_id", "country_name"],
        value_vars=year_columns,
        var_name="year",
        value_name="gdp_per_capita",
    )

    # Drop missing values
    df = df[df["gdp_per_capita"].notna()]

    # Save the processed data
    df.to_csv("../processed/gdp.csv", index=False)
