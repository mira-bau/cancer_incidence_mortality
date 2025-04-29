import pandas as pd

# Load the normalized data
df = pd.read_csv("normalized_data.csv")

# Separate incidence and mortality data
incidence_df = df[df["measure"] == "Incidence"]
mortality_df = df[df["measure"] == "Mortality"]

# Find the cancer with the highest total incidence rate per country
incidence_grouped = (
    incidence_df.groupby(["country_name", "cancer_name"])["rate"].sum().reset_index()
)
dominant_incidence = (
    incidence_grouped.sort_values(["country_name", "rate"], ascending=[True, False])
    .drop_duplicates("country_name")
    .set_index("country_name")
)

# Find the cancer with the highest total mortality rate per country
mortality_grouped = (
    mortality_df.groupby(["country_name", "cancer_name"])["rate"].sum().reset_index()
)
dominant_mortality = (
    mortality_grouped.sort_values(["country_name", "rate"], ascending=[True, False])
    .drop_duplicates("country_name")
    .set_index("country_name")
)

# Create result DataFrame
result = pd.DataFrame(
    {
        "highest_incidence_cancer": dominant_incidence["cancer_name"],
        "highest_mortality_cancer": dominant_mortality["cancer_name"],
    }
)

# Save the result
result.to_csv("dominant_cancer_types.csv")

print(
    "Dominant cancer types per country identified and saved as 'dominant_cancer_types.csv'."
)
