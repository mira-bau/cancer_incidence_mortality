import pandas as pd

# Load the data
df = pd.read_csv("preprocessed_data.csv")

# Fill missing values for population only first
df["population"] = df.groupby("country_name")["population"].transform(
    lambda x: x.fillna(x.mean())
)

# Create normalized rates based on measure
df["rate"] = df.apply(
    lambda row: row["new_cases"] / row["population"]
    if row["measure"] == "Incidence"
    else row["total_cases"] / row["population"],
    axis=1,
)

# Now fill missing values for the other selected markers
markers = [
    "air_pollution",
    "alcohol_use",
    "gdp_per_capita",
    "uhc_index",
    "obesity_rate",
    "tobacco_use",
]
df[markers] = df.groupby("country_name")[markers].transform(
    lambda x: x.fillna(x.mean())
)

# Drop the population column
# df = df.drop(columns=["population"])

# Drop rows where all markers are missing
df = df[~df[markers].isnull().all(axis=1)]

# Save the result
df.to_csv("normalized_data.csv", index=False)

print(
    "Normalization and missing data handling complete. File saved as 'normalized_data.csv'."
)
