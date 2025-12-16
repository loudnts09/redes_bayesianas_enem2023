import zipfile
import pandas as pd
from pathlib import Path
from config import *

def loadData():
    os.makedirs(BASE_DIR, exist_ok=True)

    if not os.path.exists(EXTRACT_TO):
        os.makedirs(BASE_DIR, exist_ok=True)
        if os.path.exists(ZIP_PATH):
            print("Extraindo dados do ENEM (CSV)...")
            with zipfile.ZipFile(ZIP_PATH, "r") as z:
                z.extractall(EXTRACT_TO)
            print("Extração concluída!")
        else:
            print("Arquivo ZIP não encontrado. Verifique o download.")

    if os.path.exists(PARQUET_PATH):
        print("Arquivo Parquet encontrado! Carregando dados otimizados...")
        df = pd.read_parquet(PARQUET_PATH)
    else:
        print("Parquet não encontrado. Lendo CSV original para converter...")
        
        csv_file_path = f"{EXTRACT_TO}/DADOS/MICRODADOS_ENEM_2023.csv"
        
        try:
            df = pd.read_csv(csv_file_path, sep=';', encoding='latin-1', low_memory=False)
            
            print("Convertendo e salvando em Parquet...")
            df.to_parquet(PARQUET_PATH, index=False)
            print("Conversão concluída! Nas próximas vezes será instantâneo.")
            
        except FileNotFoundError:
            print(f"Erro: Não encontrei o CSV em {csv_file_path}")

    print(f"Dados carregados! Formato: {df.shape}")
    df.head()

def _code_to_str7(x):
    """
      Converte código de município para string com 7 dígitos.
      - Alguns arquivos vêm como float (ex: 2304405.0)
      - Outros vêm como string sem zeros à esquerda
    """
    import pandas as _pd
    if _pd.isna(x):
        return None
    try:
        s = str(int(x))
    except:
        s = ''.join(ch for ch in str(x) if ch.isdigit())
    return s.zfill(7) if s else None

def _uf_code_from_mun(code7):
    """Extrai os 2 primeiros dígitos do código do município → código da UF."""
    return code7[:2] if code7 else None

def _region_from_mun(code7):
    """Extrai o 1º dígito do código do município → região do país."""
    return int(code7[0]) if code7 else None

def preparar_enem(src, dst, n_linhas):
    """
      Executa o pipeline de tratamento:
        - Seleção de colunas
        - Derivação de UF e Região
        - Remoção de treineiros
        - Remoção de linhas sem notas
        - Criação da média das notas
        - Conversão ordinal do questionário socioeconômico
        Retorna: dataframe tratado
    """

    src = Path(src)
    print("Lendo CSV bruto...")

    # 1. Seleciona e lê apenas colunas relevantes
    df = pd.read_csv(
        src,
        sep=";",
        encoding="latin-1",
        usecols=lambda c: c in WANTED_COLS,
        low_memory=False,
        nrows=n_linhas
    )

    # 2. Deriva UF e região
    if "CO_MUNICIPIO_PROVA" in df.columns:
        # Converte código do município para formato uniforme de 7 dígitos
        df["CO_MUNICIPIO_PROVA_str"] = df["CO_MUNICIPIO_PROVA"].apply(_code_to_str7)
        # Código da UF
        df["UF_CODE_PROVA"] = df["CO_MUNICIPIO_PROVA_str"].apply(_uf_code_from_mun)
        # Sigla da UF
        df["SG_UF_PROVA"] = df["UF_CODE_PROVA"].map(UF_CODE_TO_SIGLA)
        # Região (ID e nome)
        df["REGIAO_ID_PROVA"] = df["CO_MUNICIPIO_PROVA_str"].apply(_region_from_mun)
        df["REGIAO_NOME_PROVA"] = df["REGIAO_ID_PROVA"].map(REGION_NAME)

    # 3. Remove treineiros
    if "IN_TREINEIRO" in df.columns:
        df = df[df["IN_TREINEIRO"] == 0]

    # 4. Remove candidatos sem notas (faltaram)
    df = df.dropna(subset=[c for c in NOTE_COLS if c in df.columns])

    # 5. Cria média das cinco notas
    df["NOTA_MEDIA_5"] = df[NOTE_COLS].mean(axis=1)

    # 6. Converte questionário socioeconômico A,B,C,... para números
    for q in ["Q001", "Q002", "Q006", "Q022", "Q024", "Q025"]:
        if q in df.columns:
            df[f"{q}_ord"] = df[q].map(ORD_MAP)

    df.to_parquet(dst, index=False)

    print(f"Gerado: {dst}")
    print("Linhas:", len(df))

    return df
