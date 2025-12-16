from etl import pd

def selectingColumns(df_tratado):
    #selecionando apenas as colunas que fazem sentido para a rede
    #vamos pegar Tipo de Escola, Renda (Q006), Região e as Notas
    cols_rede = [
        'TP_ESCOLA', 'TP_SEXO', 'Q006_ord', 'Q002_ord', 'Q025_ord', 'REGIAO_NOME_PROVA',
        'NU_NOTA_MT', 'NU_NOTA_LC', 'NU_NOTA_CH', 'NU_NOTA_CN', 'NU_NOTA_REDACAO'
    ]

    df_bn = df_tratado[cols_rede].copy()

    #discretizar as notas (transformar números em faixas)
    # vamos dividir em 3 categorias: 1 (Baixa), 2 (Média), 3 (Alta) usando qcut (quartis)
    labels_notas = ['Baixa', 'Média', 'Alta']
    cols_notas = ['NU_NOTA_MT', 'NU_NOTA_LC', 'NU_NOTA_CH', 'NU_NOTA_CN', 'NU_NOTA_REDACAO']

    for col in cols_notas:
        # Cria faixas baseadas na distribuição dos dados
        df_bn[f'{col}_CAT'] = pd.qcut(df_bn[col], q=3, labels=labels_notas)

    #remover as colunas numéricas originais, deixando apenas as categóricas
    df_bn = df_bn.drop(columns=cols_notas)

    # mapeamentos para deixar os nomes legíveis no gráfico
    mapa_escola = {1: 'N/R', 2: 'Publica', 3: 'Privada'}
    mapa_internet = {1: 'Nao', 2: 'Sim'} # Q025: A=1 (Não), B=2 (Sim)

    df_bn['TP_ESCOLA'] = df_bn['TP_ESCOLA'].map(mapa_escola)
    df_bn['Q025_ord'] = df_bn['Q025_ord'].map(mapa_internet)

    #vamos mapear TP_ESCOLA para nomes para ficar melhor no gráfico
    mapa_nomes = {
        'TP_ESCOLA': 'Escola',
        'TP_SEXO': 'Sexo',
        'Q006_ord': 'Renda',
        'Q002_ord': 'Escolaridade_Mae',
        'Q025_ord': 'Internet',
        'REGIAO_NOME_PROVA': 'Regiao',
        'NU_NOTA_MT_CAT': 'Nota_Matematica',
        'NU_NOTA_LC_CAT': 'Nota_Linguagens',
        'NU_NOTA_CH_CAT': 'Nota_Humanas',
        'NU_NOTA_CN_CAT': 'Nota_Natureza',
        'NU_NOTA_REDACAO_CAT': 'Nota_Redacao'
    }
    df_bn = df_bn.rename(columns=mapa_nomes)

    print(df_bn.head())