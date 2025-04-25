import pandas as pd

# Load the data
df = pd.read_csv("preprocessed_data.csv")

# Fill missing values for selected columns only
columns_to_fill = [
    "population",
    "air_pollution",
    "alcohol_use",
    "gdp_per_capita",
    "uhc_index",
    "obesity_rate",
    "tobacco_use",
]
df[columns_to_fill] = df.groupby("country_name")[columns_to_fill].transform(
    lambda x: x.fillna(x.mean())
)

# Create normalized rates based on measure
df["rate"] = df.apply(
    lambda row: row["new_cases"] / row["population"]
    if row["measure"] == "Incidence"
    else row["total_cases"] / row["population"],
    axis=1,
)

# Drop the population column
df = df.drop(columns=["population"])

# Drop any remaining missing rows
df = df.dropna()

# Save the result
df.to_csv("normalized_data.csv", index=False)

print(
    "Normalization and missing data handling complete. File saved as 'normalized_data.csv'."
)
