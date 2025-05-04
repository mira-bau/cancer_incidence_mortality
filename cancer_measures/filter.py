import os
import pandas as pd

# === CONFIG ===
INPUT_FILE = 'normalized_data.csv'
CHUNK_SIZE = 50000

# === CREATE OUTPUT DIRECTORIES ===
os.makedirs('filtered/country', exist_ok=True)
os.makedirs('filtered/year', exist_ok=True)

# === GET UNIQUE COUNTRY NAMES & YEARS ===
unique_countries = set()
unique_years = set()

# Step 1: First pass to collect all unique countries and years
for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE):
    unique_countries.update(chunk['country_name'].dropna().unique())
    unique_years.update(chunk['year'].dropna().unique())

# Optional: sort them
unique_countries = sorted(list(unique_countries))
unique_years = sorted(list(unique_years))

# Step 2: Filter by country and save
for country in unique_countries:
    filtered_chunks = []
    for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE):
        filtered = chunk[chunk['country_name'] == country]
        if not filtered.empty:
            filtered_chunks.append(filtered)
    if filtered_chunks:
        df_country = pd.concat(filtered_chunks)
        df_country.to_csv(f'filtered/country/{country}.csv', index=False)

# Step 3: Filter by year and save
for year in unique_years:
    filtered_chunks = []
    for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE):
        filtered = chunk[chunk['year'] == year]
        if not filtered.empty:
            filtered_chunks.append(filtered)
    if filtered_chunks:
        df_year = pd.concat(filtered_chunks)
        df_year.to_csv(f'filtered/year/{year}.csv', index=False)

print("✅ Filtering complete.")
