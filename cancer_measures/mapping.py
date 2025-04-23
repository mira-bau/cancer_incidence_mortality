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

COUNTRY_MAP = [
  {
    "country_id": 840,
    "standard_name": "USA",
    "aliases": [
      "USA",
      "United States",
      "United States of America"
    ]
  },
  {
    "country_id": 826,
    "standard_name": "United Kingdom",
    "aliases": [
      "United Kingdom",
      "United Kingdom of Great Britain and Northern Ireland"
    ]
  },
  {
    "country_id": 410,
    "standard_name": "Korea, Republic of",
    "aliases": [
      "Korea, Rep.",
      "Korea, Republic of",
      "Republic of Korea"
    ]
  },
  {
    "country_id": 528,
    "standard_name": "The Netherlands",
    "aliases": [
      "Netherlands",
      "Netherlands (Kingdom of the)",
      "The Netherlands"
    ]
  },
  {
    "country_id": 862,
    "standard_name": "Venezuela",
    "aliases": [
      "Venezuela",
      "Venezuela (Bolivarian Republic of)",
      "Venezuela, RB"
    ]
  },
  {
    "country_id": 703,
    "standard_name": "Slovakia",
    "aliases": [
      "Slovak Republic",
      "Slovakia"
    ]
  },
  {
    "country_id": 417,
    "standard_name": "Kyrgyzstan",
    "aliases": [
      "Kyrgyz Republic",
      "Kyrgyzstan"
    ]
  },
  {
    "country_id": 792,
    "standard_name": "Türkiye",
    "aliases": [
      "Turkiye",
      "Türkiye"
    ]
  },
  {
    "country_id": 250,
    "standard_name": "France (metropolitan)",
    "aliases": [
      "France",
      "France (metropolitan)"
    ]
  },
  {
    "country_id": 474,
    "standard_name": "France, Martinique",
    "aliases": [
      "France, Martinique"
    ]
  },
  {
    "country_id": 32,
    "standard_name": "Argentina",
    "aliases": [
      "Argentina"
    ]
  },
  {
    "country_id": 36,
    "standard_name": "Australia",
    "aliases": [
      "Australia"
    ]
  },
  {
    "country_id": 40,
    "standard_name": "Austria",
    "aliases": [
      "Austria"
    ]
  },
  {
    "country_id": 48,
    "standard_name": "Bahrain",
    "aliases": [
      "Bahrain"
    ]
  },
  {
    "country_id": 51,
    "standard_name": "Armenia",
    "aliases": [
      "Armenia"
    ]
  },
  {
    "country_id": 56,
    "standard_name": "Belgium",
    "aliases": [
      "Belgium"
    ]
  },
  {
    "country_id": 76,
    "standard_name": "Brazil",
    "aliases": [
      "Brazil"
    ]
  },
  {
    "country_id": 84,
    "standard_name": "Belize",
    "aliases": [
      "Belize"
    ]
  },
  {
    "country_id": 112,
    "standard_name": "Belarus",
    "aliases": [
      "Belarus"
    ]
  },
  {
    "country_id": 124,
    "standard_name": "Canada",
    "aliases": [
      "Canada"
    ]
  },
  {
    "country_id": 152,
    "standard_name": "Chile",
    "aliases": [
      "Chile"
    ]
  },
  {
    "country_id": 156,
    "standard_name": "China",
    "aliases": [
      "China"
    ]
  },
  {
    "country_id": 170,
    "standard_name": "Colombia",
    "aliases": [
      "Colombia"
    ]
  },
  {
    "country_id": 188,
    "standard_name": "Costa Rica",
    "aliases": [
      "Costa Rica"
    ]
  },
  {
    "country_id": 191,
    "standard_name": "Croatia",
    "aliases": [
      "Croatia"
    ]
  },
  {
    "country_id": 192,
    "standard_name": "Cuba",
    "aliases": [
      "Cuba"
    ]
  },
  {
    "country_id": 196,
    "standard_name": "Cyprus",
    "aliases": [
      "Cyprus"
    ]
  },
  {
    "country_id": 203,
    "standard_name": "Czechia",
    "aliases": [
      "Czechia"
    ]
  },
  {
    "country_id": 208,
    "standard_name": "Denmark",
    "aliases": [
      "Denmark"
    ]
  },
  {
    "country_id": 218,
    "standard_name": "Ecuador",
    "aliases": [
      "Ecuador"
    ]
  },
  {
    "country_id": 233,
    "standard_name": "Estonia",
    "aliases": [
      "Estonia"
    ]
  },
  {
    "country_id": 246,
    "standard_name": "Finland",
    "aliases": [
      "Finland"
    ]
  },
  {
    "country_id": 268,
    "standard_name": "Georgia",
    "aliases": [
      "Georgia"
    ]
  },
  {
    "country_id": 276,
    "standard_name": "Germany",
    "aliases": [
      "Germany"
    ]
  },
  {
    "country_id": 300,
    "standard_name": "Greece",
    "aliases": [
      "Greece"
    ]
  },
  {
    "country_id": 320,
    "standard_name": "Guatemala",
    "aliases": [
      "Guatemala"
    ]
  },
  {
    "country_id": 328,
    "standard_name": "Guyana",
    "aliases": [
      "Guyana"
    ]
  },
  {
    "country_id": 348,
    "standard_name": "Hungary",
    "aliases": [
      "Hungary"
    ]
  },
  {
    "country_id": 352,
    "standard_name": "Iceland",
    "aliases": [
      "Iceland"
    ]
  },
  {
    "country_id": 356,
    "standard_name": "India",
    "aliases": [
      "India"
    ]
  },
  {
    "country_id": 372,
    "standard_name": "Ireland",
    "aliases": [
      "Ireland"
    ]
  },
  {
    "country_id": 376,
    "standard_name": "Israel",
    "aliases": [
      "Israel"
    ]
  },
  {
    "country_id": 380,
    "standard_name": "Italy",
    "aliases": [
      "Italy"
    ]
  },
  {
    "country_id": 392,
    "standard_name": "Japan",
    "aliases": [
      "Japan"
    ]
  },
  {
    "country_id": 414,
    "standard_name": "Kuwait",
    "aliases": [
      "Kuwait"
    ]
  },
  {
    "country_id": 428,
    "standard_name": "Latvia",
    "aliases": [
      "Latvia"
    ]
  },
  {
    "country_id": 440,
    "standard_name": "Lithuania",
    "aliases": [
      "Lithuania"
    ]
  },
  {
    "country_id": 442,
    "standard_name": "Luxembourg",
    "aliases": [
      "Luxembourg"
    ]
  },
  {
    "country_id": 470,
    "standard_name": "Malta",
    "aliases": [
      "Malta"
    ]
  },
  {
    "country_id": 480,
    "standard_name": "Mauritius",
    "aliases": [
      "Mauritius"
    ]
  },
  {
    "country_id": 484,
    "standard_name": "Mexico",
    "aliases": [
      "Mexico"
    ]
  },
  {
    "country_id": 498,
    "standard_name": "Moldova",
    "aliases": [
      "Moldova"
    ]
  },
  {
    "country_id": 554,
    "standard_name": "New Zealand",
    "aliases": [
      "New Zealand"
    ]
  },
  {
    "country_id": 558,
    "standard_name": "Nicaragua",
    "aliases": [
      "Nicaragua"
    ]
  },
  {
    "country_id": 578,
    "standard_name": "Norway",
    "aliases": [
      "Norway"
    ]
  },
  {
    "country_id": 591,
    "standard_name": "Panama",
    "aliases": [
      "Panama"
    ]
  },
  {
    "country_id": 600,
    "standard_name": "Paraguay",
    "aliases": [
      "Paraguay"
    ]
  },
  {
    "country_id": 608,
    "standard_name": "Philippines",
    "aliases": [
      "Philippines"
    ]
  },
  {
    "country_id": 616,
    "standard_name": "Poland",
    "aliases": [
      "Poland"
    ]
  },
  {
    "country_id": 620,
    "standard_name": "Portugal",
    "aliases": [
      "Portugal"
    ]
  },
  {
    "country_id": 630,
    "standard_name": "Puerto Rico",
    "aliases": [
      "Puerto Rico"
    ]
  },
  {
    "country_id": 634,
    "standard_name": "Qatar",
    "aliases": [
      "Qatar"
    ]
  },
  {
    "country_id": 642,
    "standard_name": "Romania",
    "aliases": [
      "Romania"
    ]
  },
  {
    "country_id": 688,
    "standard_name": "Serbia",
    "aliases": [
      "Serbia"
    ]
  },
  {
    "country_id": 702,
    "standard_name": "Singapore",
    "aliases": [
      "Singapore"
    ]
  },
  {
    "country_id": 705,
    "standard_name": "Slovenia",
    "aliases": [
      "Slovenia"
    ]
  },
  {
    "country_id": 710,
    "standard_name": "South Africa",
    "aliases": [
      "South Africa"
    ]
  },
  {
    "country_id": 724,
    "standard_name": "Spain",
    "aliases": [
      "Spain"
    ]
  },
  {
    "country_id": 752,
    "standard_name": "Sweden",
    "aliases": [
      "Sweden"
    ]
  },
  {
    "country_id": 756,
    "standard_name": "Switzerland",
    "aliases": [
      "Switzerland"
    ]
  },
  {
    "country_id": 764,
    "standard_name": "Thailand",
    "aliases": [
      "Thailand"
    ]
  },
  {
    "country_id": 800,
    "standard_name": "Uganda",
    "aliases": [
      "Uganda"
    ]
  },
  {
    "country_id": 858,
    "standard_name": "Uruguay",
    "aliases": [
      "Uruguay"
    ]
  },
  {
    "country_id": 860,
    "standard_name": "Uzbekistan",
    "aliases": [
      "Uzbekistan"
    ]
  }
]
