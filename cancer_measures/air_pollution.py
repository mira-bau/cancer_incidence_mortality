import pandas as pd
import mapping

# Build alias and standard name lookup maps
ALIAS_TO_ID = {
    alias: entry["country_id"]
    for entry in mapping.COUNTRY_MAP
    for alias in [entry["standard_name"]] + entry["aliases"]
}
ID_TO_STANDARD_NAME = {
    entry["country_id"]: entry["standard_name"] for entry in mapping.COUNTRY_MAP
}

if __name__ == "__main__":
    # Load air pollution data
    df = pd.read_csv("raw/PM25_air_polution.csv", skiprows=4)

    # Keep only years from 2000 onward
    year_columns = [col for col in df.columns if col.isnumeric() and int(col) >= 2000]
    df = df[["Country Name"] + year_columns]

    # Reshape to long format
    df = df.melt(id_vars="Country Name", var_name="year", value_name="air_pollution")
    df["year"] = df["year"].astype(int)

    # Map country_id using aliases
    df["country_id"] = df["Country Name"].map(ALIAS_TO_ID).astype("Int64")
    df = df[df["country_id"].notna()]

    # Map country_name using standard name
    df["country_name"] = df["country_id"].map(ID_TO_STANDARD_NAME)

    # Final selection and export
    df = df[["country_id", "country_name", "year", "air_pollution"]]
    df.to_csv("processed/air_pollution.csv", index=False)
