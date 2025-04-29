import pandas as pd

# Load the data
df = pd.read_csv("preprocessed_data.csv")

# Fill missing population values per country
df["population"] = df.groupby("country_name")["population"].transform(
    lambda x: x.fillna(x.mean())
)

# Fix rate calculation: use new_cases/deaths for both Incidence and Mortality (if no death data available)
df["rate"] = df["new_cases/deaths"] / df["population"]

# Fill missing values for other markers
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

# Drop rows where all markers are missing
df = df[~df[markers].isnull().all(axis=1)]

# Save cleaned data
df.to_csv("normalized_data.csv", index=False)

print("Fixed normalization and saved as 'normalized_data.csv'.")
