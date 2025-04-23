import pandas as pd

import mapping

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

    # Drop missing values
    data = data[data["year"].astype(str).str.isnumeric()]
    data = data.dropna(subset=["tobacco_use"])

    # Map country_id
    data["country_id"] = data["Country Name"].map(mapping.REVERSE_COUNTRY_MAP)

    # Final filter
    data = data[data["country_id"].notna()]
    data = data[["country_id", "Country Name", "year", "tobacco_use"]]
    data.columns = ["country_id", "country_name", "year", "tobacco_use"]

    # Export to CSV
    data.to_csv("processed/smoking.csv", index=False)
