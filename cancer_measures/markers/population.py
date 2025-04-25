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
    df = pd.read_csv("../raw/population.csv")

    # Normalize country names
    df["country_lower"] = df["Country/Territory"].str.lower()
    df["country_id"] = df["country_lower"].map(ALIAS_TO_ID).astype("Int64")

    # Filter valid countries
    df = df[df["country_id"].notna()]

    # Add standard names
    df["country_name"] = df["country_id"].map(ID_TO_STANDARD_NAME)

    # Extract population columns from 2000 onward
    pop_cols = [
        col
        for col in df.columns
        if "Population" in col
        and col.split()[0].isdigit()
        and int(col.split()[0]) >= 2000
    ]

    # Reshape the data
    df = df.melt(
        id_vars=["country_id", "country_name"],
        value_vars=pop_cols,
        var_name="year",
        value_name="population",
    )

    # Extract numeric year and drop rows where year is NaN
    df["year"] = df["year"].str.extract(r"(\d{4})")
    df = df[df["year"].notna()]
    df["year"] = df["year"].astype(int)

    # Drop missing
    df = df[df["population"].notna()]

    # Save
    df.to_csv("../processed/population.csv", index=False)
