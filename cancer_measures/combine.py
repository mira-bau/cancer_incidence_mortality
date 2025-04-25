import os
import pandas as pd

# Define the folder containing the processed files
processed_folder = "processed"
output_file = "preprocessed_data.csv"

# List all files
all_files = sorted(os.listdir(processed_folder))

# Make sure to start with cancer data first
all_files = [f for f in all_files if f == "cancer_data.csv"] + [
    f for f in all_files if f != "cancer_data.csv"
]

# Initialize base DataFrame
base_df = None

# Process files
for file_name in all_files:
    if not file_name.endswith(".csv"):
        continue

    file_path = os.path.join(processed_folder, file_name)
    df = pd.read_csv(file_path)

    # Make sure 'year' is integer
    if "year" in df.columns:
        df["year"] = df["year"].astype(int)

    if base_df is None:
        base_df = df
    else:
        # If df is a measure file (only one data column)
        if len(df.columns) == 4:  # country_id, country_name, year, measure
            measure_column = [
                col
                for col in df.columns
                if col not in ["country_id", "country_name", "year"]
            ][0]
            # Merge on country_id, country_name, year
            base_df = base_df.merge(
                df, on=["country_id", "country_name", "year"], how="left"
            )
        else:
            # If df is a cancer data file, just add columns
            df = df.drop(
                columns=[
                    col
                    for col in ["country_id", "country_name", "year"]
                    if col in df.columns
                ]
            )
            base_df = pd.concat(
                [base_df.reset_index(drop=True), df.reset_index(drop=True)], axis=1
            )

# Drop 'country_id' and 'cancer_id'
base_df = base_df.drop(columns=["country_id", "cancer_id"], errors="ignore")

# Move 'population' to 4th index
cols = base_df.columns.tolist()

cols.insert(1, cols.pop(cols.index("year")))
cols.insert(2, cols.pop(cols.index("population")))
base_df = base_df[cols]

# Save the final data
base_df.to_csv(output_file, index=False)

print(f"Data combined and saved to '{output_file}'")
