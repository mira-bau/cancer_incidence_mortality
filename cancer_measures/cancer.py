import requests
import pandas as pd
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

import cancer_measures.mapping as mapping

# Catch errors only and logging them
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="failures.log",
)

BASE_URL = "https://gco.iarc.fr"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Origin": "https://gco.iarc.who.int",
    "Referer": "https://gco.iarc.who.int/",
}
CANCER_OVERTIME_PARAMS = {
    "ages_group": "0_14",
    "year_start": "2000",
    "year_end": "2023",
}

cancer_overtime_path = "/gateway_prod/api/overtime/v2/21//data/population/%i/0/%i/(%i)/"

# Build country lookup maps
COUNTRY_ID_TO_NAME = {
    entry["country_id"]: entry["standard_name"] for entry in mapping.COUNTRY_MAP
}


def build_country_cancer_url(measure_id: int, country_id: int, cancer_id: int) -> str:
    return BASE_URL + cancer_overtime_path % (measure_id, country_id, cancer_id)


def parse_cancer_data(measure: str, data: list[dict]):
    parsed_data = [
        {
            "country_id": item["country"],
            "country_name": COUNTRY_ID_TO_NAME.get(int(item["country"]), "Unknown"),
            "cancer_id": item["cancer"],
            "cancer_name": mapping.CANCER_MAP.get(int(item["cancer"]), "Unknown"),
            "year": item["year"],
            "new_cases/deaths": item["total"],
            "total_cases": item["total_pop"],
            "cumulative_risk": item["cum_risk_74"],
            "measure": measure,
        }
        for item in data
    ]
    return parsed_data


def fetch_data(measure_id, measure_label, cancer_id, country_id):
    url = build_country_cancer_url(measure_id, country_id, cancer_id)
    try:
        response = requests.get(url, headers=HEADERS, params=CANCER_OVERTIME_PARAMS)
        response.raise_for_status()
        data = response.json().get("dataset", [])
        return parse_cancer_data(measure_label, data)
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
        return []


def entrypoint():
    warehouse = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for measure_id, measure_label in mapping.MEASURE_MAP.items():
            for cancer_id in mapping.CANCER_MAP.keys():
                for country in mapping.COUNTRY_MAP:
                    future = executor.submit(
                        fetch_data,
                        measure_id,
                        measure_label,
                        cancer_id,
                        country["country_id"],
                    )
                    futures.append(future)

        for future in tqdm(
            as_completed(futures), total=len(futures), desc="Fetching data"
        ):
            warehouse.extend(future.result())

    df = pd.DataFrame(warehouse)
    print("Exporting data to CSV...")
    df.to_csv("processed/cancer_data.csv", index=False)


if __name__ == "__main__":
    entrypoint()
