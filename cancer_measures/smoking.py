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
    # Load Excel file
    data = pd.read_excel("raw/API_SH.PRV.xlsx", sheet_name="Data", skiprows=3)

    # Filter tobacco use indicator
    data = data[data["Indicator Code"] == "SH.PRV.SMOK"]

    # Melt the year columns
    data = data.melt(
        id_vars=["Country Name", "Country Code"],
        var_name="year",
        value_name="tobacco_use",
    )

    # Keep only numeric years and non-null values
    data = data[data["year"].astype(str).str.isnumeric()]
    data = data.dropna(subset=["tobacco_use"])

    # Map country_id using aliases
    data["country_id"] = data["Country Name"].map(ALIAS_TO_ID).astype("Int64")

    # Filter only valid mappings
    data = data[data["country_id"].notna()]

    # Map standard country names
    data["country_name"] = data["country_id"].map(ID_TO_STANDARD_NAME)

    # Select final columns
    data = data[["country_id", "country_name", "year", "tobacco_use"]]

    # Export to CSV
    data.to_csv("processed/smoking.csv", index=False)
