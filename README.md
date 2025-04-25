# Cancer Incidence Mortality
A unified data parser for non-communicable disease (NCD) risk factors and cancer statistics, sourced from global health datasets.


## Overview

This project standardizes data parsing for key health indicators across multiple sources.
Each dataset outputs a consistent schema:

**Shared columns:**
- `country_id`: A unique numeric identifier for each country
- `country_name`: The official country name
- `year`: Year of the observation

Additional columns vary depending on the dataset (e.g., `tobacco_use`, `alcohol_use`, `diabetes`, `new_cases`, etc.).


## Parsers

Each parser handles one data source:
- `alcohol.py` – parses alcohol consumption rates
- `cancer.py` – scrapes cancer incidence and mortality from GCO
- `diabetes.py` – processes diabetes prevalence rates
- `smoking.py` – extracts tobacco use prevalence
- `air_pollution.py` - extracts mean annual exposure of air pollution
- `health_coverage.py` - extracts the Universal Health Coverage Index
- `gcp.py` - extracts the GDP per Capita (current US$)
- `obesity.py` - extracts the obesity rate

All parsers map countries using a unified COUNTRY_MAP structure from `mapping.py`, which includes multiple name aliases for robust matching.


## Data Sources

| Dataset                             | Source                        | Link                                                                                                                                          |
| ----------------------------------- | ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **Cancer**                          | Global Cancer Observatory     | [gco.iarc.fr](https://gco.iarc.fr/overtime/en/dataviz/trends)                                                                                 |
| **Smoking**                         | World Bank                    | [data.worldbank.org](https://data.worldbank.org/indicator/SH.PRV.SMOK)                                                                        |
| **Alcohol Use**                     | World Health Organization     | [who.int](https://www.who.int/data/gho/indicator-metadata-registry/imr-details/462)                                                           |
| **Diabetes**                        | NCD Risk Factor Collaboration | [ncdrisc.org](https://www.ncdrisc.org/data-downloads-diabetes.html)                                                                           |
| **Air Pollution**                   | World Bank                    | [data.worldbank.org](https://data.worldbank.org/indicator/EN.ATM.PM25.MC.M3)                                                                  |
| **Universal Health Coverage Index** | World Health Organization     | [who.int](https://data.who.int/indicators/i/3805B1E/9A706FD)                                                                                  |
| **GDP per Capita**                  | World Bank                    | [data.worldbank.org](https://data.worldbank.org/indicator/NY.GDP.PCAP.CD)                                                                     |
| **Obesity**                         | World Health Organization     | [who.int](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/prevalence-of-obesity-among-adults-bmi--30-(crude-estimate)-(-)) |


## Methodology

- Each dataset is parsed and normalized into the shared schema.
- Country names are resolved using `mapping.py`, which supports both official and alias names.
- For gender-specific data (e.g., diabetes prevalence), values for men and women are averaged.
- Data is cleaned, filtered (e.g. years ≥ 2020), and exported to CSV.
- Missing or unmapped countries are logged for traceability.
- Final outputs are stored in the processed/ directory, ready for analysis or visualization.


## Usage

You can use the pre-cleaned datasets available in the `/processed` directory, including the combined output file `result.csv`.

**Re-running Parsers**

To re-run any parser script locally, make sure you have Poetry installed. Then:
1. Install dependencies:
```bash
poetry install
```


2. Navigate to the project directory
```bash
cd cancer_measures
```

3. Run a specific parser
```bash
poetry run python <parser_name>.py
```
Example `poetry run python smoking.py`

Each parser will output a standardized CSV file into the processed/ folder.
