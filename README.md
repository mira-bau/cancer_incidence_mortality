# Cancer Incidence Mortality
A unified data parser for non-communicable disease (NCD) risk factors and cancer statistics, sourced from global health datasets.


## Overview

This project standardizes data parsing for key health indicators across multiple sources.
Each dataset outputs a consistent schema:

**Shared columns:**
- `country_id`: A unique numeric identifier for each country
- `country_name`: The official country name
- `year`: Year of the observation

Additional columns vary depending on the dataset (e.g., `tobacco_use`, `alcohol_use`, `obesity`, `new_cases/deaths`, etc.).


**NOTE: The `new_cases/deaths` column is determined by the value in the `measure` column: if measure is *Incidence*, the value represents *new_cases*; if measure is *Mortality*, it represents *deaths*.**


# Cancer Statistics Dataset Documentation

This dataset provides cancer-related statistics per country and year, alongside health and economic indicators. Below is a description of each column.

## Column Descriptions

| Column Name          | Description                                                                                                                          |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **country_name**     | Name of the country.                                                                                                                 |
| **year**             | Year the data was collected.                                                                                                         |
| **population**       | Total national population in that year.                                                                                              |
| **cancer_name**      | Specific cancer type (e.g., Head and neck).                                                                                          |
| **new_cases/deaths** | Number of new cancer cases or deaths in that year (depends on `measure`).                                                            |
| **total_cases**      | Estimated total number of people ever diagnosed with any cancer up to that year (prevalence), including both survivors and deceased. |
| **cumulative_risk**  | Probability (0–1) of developing or dying from the cancer before age 75, assuming no other causes of death.                           |
| **measure**          | Type of data reported: `Incidence` (new cases) or `Mortality` (deaths).                                                              |
| **air_pollution**    | Average annual PM2.5 air pollution (in micrograms per cubic meter).                                                                  |
| **alcohol_use**      | Average alcohol consumption per capita per year (liters).                                                                            |
| **gdp_per_capita**   | GDP per capita in USD (inflation-adjusted).                                                                                          |
| **uhc_index**        | Universal Health Coverage index (0–100 scale).                                                                                       |
| **obesity_rate**     | Percentage of population classified as obese.                                                                                        |
| **tobacco_use**      | Percentage of population using tobacco.                                                                                              |
| **rate**             | Cancer case or death rate per person (e.g., new_cases/population). Very small value due to population scaling.                       |

## Notes

- The `total_cases` field is not limited to the specific `cancer_name`; it reflects national totals across all cancers.
- `cumulative_risk` is specific to the listed `cancer_name`.


## Parsers

Each parser handles one data source:
- `alcohol.py` – parses alcohol consumption rates
- `cancer.py` – scrapes cancer incidence and mortality from GCO
- `smoking.py` – extracts tobacco use prevalence
- `air_pollution.py` - extracts mean annual exposure of air pollution
- `health_coverage.py` - extracts the Universal Health Coverage Index
- `gdp.py` - extracts the GDP per Capita (current US$)
- `obesity.py` - extracts the obesity rates
- `population.py` - extracts the population of countries over the years

All parsers map countries using a unified COUNTRY_MAP structure from `mapping.py`, which includes multiple name aliases for robust matching.


## Data Sources

| Dataset                             | Source                    | Link                                                                                                                                          |
| ----------------------------------- | ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **Cancer**                          | Global Cancer Observatory | [gco.iarc.fr](https://gco.iarc.fr/overtime/en/dataviz/trends)                                                                                 |
| **Smoking**                         | World Bank                | [data.worldbank.org](https://data.worldbank.org/indicator/SH.PRV.SMOK)                                                                        |
| **Alcohol Use**                     | World Health Organization | [who.int](https://www.who.int/data/gho/indicator-metadata-registry/imr-details/462)                                                           |
| **Air Pollution**                   | World Bank                | [data.worldbank.org](https://data.worldbank.org/indicator/EN.ATM.PM25.MC.M3)                                                                  |
| **Universal Health Coverage Index** | World Health Organization | [who.int](https://data.who.int/indicators/i/3805B1E/9A706FD)                                                                                  |
| **GDP per Capita**                  | World Bank                | [data.worldbank.org](https://data.worldbank.org/indicator/NY.GDP.PCAP.CD)                                                                     |
| **Obesity**                         | World Health Organization | [who.int](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/prevalence-of-obesity-among-adults-bmi--30-(crude-estimate)-(-)) |
| **Population**                      | Kaggle                    | [kaggle.com](https://www.kaggle.com/datasets/iamsouravbanerjee/world-population-dataset)                                                      |


## Methodology

- Each dataset is parsed and normalized into the shared schema.
- Country names are resolved using `mapping.py`, which supports both official and alias names.
- For gender-specific data, values for men and women are averaged.
- The raw data is pivoted using country_name as the index.
- Data is cleaned, filtered (e.g., years ≥ 2020), and exported to CSV.
- Missing values are estimated using a RandomForestRegressor model.
- For model performance evaluation, a train/test split was performed on complete data entries.
- The model’s predictive performance was assessed using Mean Absolute Error (MAE) and R² (coefficient of determination).
- Using filter.py, the input data is split into smaller chunks by year and by country. These can be found in the `/filtered` directory.
- `/filtered/report.py` generates a profiling report for each country and each year, saved under the `/reports` directory.
- `final_report.py` generates the predicted cancer profiling reports, also stored in the `/reports` directory.
- Final outputs can be found in `predicted_cancer_data.csv` and for visualization `reports/predicted_cancer_data_profile.html`.


## Usage

- `/processed` is the folder that contains the data for each measurement. This data is generated by running the corresponding script for each marker located in the `/markers` directory.
- `preprocessed_data.csv` is the combined dataset collected from all markers. We created it by running the `combine.py` script.
- `normalized_data.csv` is a cleaned cancer data with normalized rates, missing values filled per country, and incomplete rows dropped. We created it using the `normalization.py` script.
- `dominant_cancer_types.csv` lists the dominant cancer types with the highest incidence and mortality rates for each country. We created it using the `dominant_cancer_type.py` script.


**Re-running Parsers**

To re-run any parser script locally, make sure you have Poetry installed. Then:
1. Install dependencies:
```bash
poetry install
```


2. Navigate to the project directory
```bash
cd cancer_measures
cd markers
```

3. Run a specific parser
```bash
poetry run python <parser_name>.py
```
Example `poetry run python smoking.py`

Each parser will output a standardized CSV file into the processed/ folder.
