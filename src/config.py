import os

actual_dir = os.getcwd()

BASE_DIR = os.path.join(actual_dir, "data")
ZIP_PATH = os.path.join(BASE_DIR, "microdados_enem_2023.zip")
EXTRACT_TO = os.path.join(BASE_DIR, "microdados_enem_2023")
PARQUET_PATH = os.path.join(BASE_DIR, "enem_2023.parquet")
CSV_FILE_PATH = os.path.join(EXTRACT_TO, "DADOS", "MICRODADOS_ENEM_2023.csv")
df = None

#codigo para tratar os dados do enem
#colunas que queremos manter do dataset
WANTED_COLS = [
    "NU_NOTA_MT", "NU_NOTA_LC", "NU_NOTA_CH", "NU_NOTA_CN", "NU_NOTA_REDACAO",
    "TP_ESCOLA", "TP_SEXO",
    "CO_MUNICIPIO_PROVA", "NO_MUNICIPIO_PROVA",
    "Q001", "Q002", "Q006", "Q022", "Q024", "Q025",
    "IN_TREINEIRO",
]

#lista com as notas das 5 provas
NOTE_COLS = ["NU_NOTA_MT", "NU_NOTA_LC", "NU_NOTA_CH", "NU_NOTA_CN", "NU_NOTA_REDACAO"]

# Conversão de respostas do questionário socioeconômico (A,B,C...) → (1,2,3...)
ORD_MAP = {chr(i): i - 64 for i in range(65, 91)}

# Nome das regiões
REGION_NAME = {
    1: "Norte",
    2: "Nordeste",
    3: "Sudeste",
    4: "Sul",
    5: "Centro-Oeste",
}

# Código da UF
UF_CODE_TO_SIGLA = {
    "11": "RO", "12": "AC", "13": "AM", "14": "RR", "15": "PA", "16": "AP", "17": "TO",
    "21": "MA", "22": "PI", "23": "CE", "24": "RN", "25": "PB", "26": "PE", "27": "AL", "28": "SE", "29": "BA",
    "31": "MG", "32": "ES", "33": "RJ", "35": "SP",
    "41": "PR", "42": "SC", "43": "RS",
    "50": "MS", "51": "MT", "52": "GO", "53": "DF",
}