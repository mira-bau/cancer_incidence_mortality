import requests
import pandas as pd
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Catch errors only and logging them
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="failures.log",
)

BASE_URL = "https://gco.iarc.fr"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Origin": "https://gco.iarc.who.int",
    "Referer": "https://gco.iarc.who.int/",
}
CANCER_OVERTIME_PARAMS = {
    "ages_group": "0_14",  # 0-75 Years
    "year_start": "2000",
    "year_end": "2023",
}

cancer_overtime_path = "/gateway_prod/api/overtime/v2/21//data/population/%i/0/%i/(%i)/"

MEASURE_MAP = {
    0: "Incidence",
    1: "Mortality",
}

CANCER_MAP = {
    1: "Head and neck",
    2: "Oesophagus",
    3: "Stomach",
    5: "Colon",
    6: "Rectum and anus",
    7: "Liver",
    8: "Gallbladder",
    9: "Pancreas",
    10: "Larynx",
    11: "Lung",
    106: "Colorectum",
    12: "Melanoma of skin",
    13: "Kaposi sarcoma",
    14: "Breast",
    24: "Thyroid",
    16: "Cervix uteri",
    17: "Corpus uteri",
    18: "Ovary",
    19: "Prostate",
    20: "Testis",
    21: "Kidney",
    22: "Bladder",
    23: "Brain and central nervous system",
    25: "Hodgkin lymphoma",
    26: "Non-Hodgkin lymphoma",
    27: "Multiple myeloma",
    28: "Leukaemia",
    15: "Uterus",
}

COUNTRY_MAP = {
    32: "Argentina",
    36: "Australia",
    40: "Austria",
    48: "Bahrain",
    51: "Armenia",
    56: "Belgium",
    76: "Brazil",
    84: "Belize",
    112: "Belarus",
    124: "Canada",
    152: "Chile",
    156: "China",
    170: "Colombia",
    188: "Costa Rica",
    191: "Croatia",
    192: "Cuba",
    196: "Cyprus",
    203: "Czechia",
    208: "Denmark",
    218: "Ecuador",
    233: "Estonia",
    246: "Finland",
    250: "France (metropolitan)",
    268: "Georgia",
    276: "Germany",
    300: "Greece",
    320: "Guatemala",
    328: "Guyana",
    348: "Hungary",
    352: "Iceland",
    356: "India",
    372: "Ireland",
    376: "Israel",
    380: "Italy",
    392: "Japan",
    410: "Korea, Republic of",
    414: "Kuwait",
    417: "Kyrgyzstan",
    428: "Latvia",
    440: "Lithuania",
    442: "Luxembourg",
    470: "Malta",
    474: "France, Martinique",
    480: "Mauritius",
    484: "Mexico",
    498: "Moldova",
    528: "The Netherlands",
    554: "New Zealand",
    558: "Nicaragua",
    578: "Norway",
    591: "Panama",
    600: "Paraguay",
    608: "Philippines",
    616: "Poland",
    620: "Portugal",
    630: "Puerto Rico",
    634: "Qatar",
    642: "Romania",
    688: "Serbia",
    702: "Singapore",
    703: "Slovakia",
    705: "Slovenia",
    710: "South Africa",
    724: "Spain",
    752: "Sweden",
    756: "Switzerland",
    764: "Thailand",
    792: "Türkiye",
    800: "Uganda",
    826: "United Kingdom",
    840: "USA",
    858: "Uruguay",
    860: "Uzbekistan",
    862: "Venezuela",
    8260: "UK, England",
    8261: "UK, Wales",
    8262: "UK, Scotland",
    8263: "UK, Northern Ireland",
    8265: "UK, England and wales",
    8401: "USA: White",
    8402: "USA: Black",
}


def build_country_cancer_url(measure_id: int, country_id: int, cancer_id: int) -> str:
    return BASE_URL + cancer_overtime_path % (measure_id, country_id, cancer_id)


def parse_cancer_data(measure: str, data: list[dict]):
    parsed_data = [
        {
            "country_id": item["country"],
            "country_name": COUNTRY_MAP[int(item["country"])],
            "cancer_id": item["cancer"],
            "cancer_name": CANCER_MAP[int(item["cancer"])],
            "year": item["year"],
            "new_cases": item["total"],
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
        for measure_id, measure_label in MEASURE_MAP.items():
            for cancer_id in CANCER_MAP.keys():
                for country_id in COUNTRY_MAP.keys():
                    future = executor.submit(
                        fetch_data, measure_id, measure_label, cancer_id, country_id
                    )
                    futures.append(future)

        for future in tqdm(
            as_completed(futures), total=len(futures), desc="Fetching data"
        ):
            warehouse.extend(future.result())

    df = pd.DataFrame(warehouse)
    print("Exporting data to CSV...")
    df.to_csv("cancer_data.csv", index=False)


if __name__ == "__main__":
    entrypoint()
