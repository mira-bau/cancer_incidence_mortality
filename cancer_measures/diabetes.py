import pandas as pd
import mapping

# Build alias-to-id and id-to-standard name lookups
ALIAS_TO_ID = {
    alias: entry["country_id"]
    for entry in mapping.COUNTRY_MAP
    for alias in [entry["standard_name"]] + entry["aliases"]
}
ID_TO_STANDARD_NAME = {
    entry["country_id"]: entry["standard_name"] for entry in mapping.COUNTRY_MAP
}

if __name__ == "__main__":
    # Load dataset
    df = pd.read_csv("raw/NCD_RisC_Lancet_2024_Diabetes_age_standardised_countries.csv")

    # Filter for only men and women
    df = df[df["Sex"].isin(["Men", "Women"])]

    # Keep only relevant columns
    df = df[
        ["Country/Region/World", "Year", "Sex", "Prevalence of diabetes (18+ years)"]
    ]

    # Keep only years from 2000 and onward
    df = df[df["Year"] >= 2000]

    # Pivot to wide format: separate columns for Men and Women
    df_pivot = df.pivot_table(
        index=["Country/Region/World", "Year"],
        columns="Sex",
        values="Prevalence of diabetes (18+ years)",
    ).reset_index()

    # Calculate average prevalence of diabetes
    df_pivot["diabetes"] = df_pivot[["Men", "Women"]].mean(axis=1)

    # Map country_id using alias map
    df_pivot["country_id"] = (
        df_pivot["Country/Region/World"].map(ALIAS_TO_ID).astype("Int64")
    )

    # Filter only mapped countries
    df_pivot = df_pivot[df_pivot["country_id"].notna()]

    # Map standard country names
    df_pivot["country_name"] = df_pivot["country_id"].map(ID_TO_STANDARD_NAME)

    # Final selection and renaming
    df_final = df_pivot[["country_id", "country_name", "Year", "diabetes"]]
    df_final.columns = ["country_id", "country_name", "year", "diabetes"]

    # Export
    df_final.to_csv("processed/diabetes.csv", index=False)
