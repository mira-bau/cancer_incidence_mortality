import pandas as pd

# Load the normalized data
df = pd.read_csv("normalized_data.csv")

# Separate incidence and mortality data
incidence_df = df[df["measure"] == "Incidence"]
mortality_df = df[df["measure"] == "Mortality"]

# Find the cancer with the highest total incidence rate per country
dominant_incidence = (
    incidence_df.groupby(["country_name", "cancer_name"])["rate"]
    .sum()
    .groupby("country_name")
    .idxmax()
)

# Find the cancer with the highest total mortality rate per country
dominant_mortality = (
    mortality_df.groupby(["country_name", "cancer_name"])["rate"]
    .sum()
    .groupby("country_name")
    .idxmax()
)

# Create a DataFrame to store the results
result = pd.DataFrame(
    {
        "highest_incidence_cancer": dominant_incidence.apply(lambda x: x[1]),
        "highest_mortality_cancer": dominant_mortality.apply(lambda x: x[1]),
    }
)

# Save the result
result.to_csv("dominant_cancer_types.csv")

print(
    "Dominant cancer types per country identified and saved as 'dominant_cancer_types.csv'."
)
