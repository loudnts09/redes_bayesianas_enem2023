from pgmpy.estimators import HillClimbSearch, BicScore
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
from networkDefinition import df_bn
from visualization import *

def trainingGraphStructure():
    # Amostra dos dados
    df_amostra = df_bn.sample(n=50000, random_state=42)

    print("Iniciando aprendizado da estrutura...")

    # 1. Inicializa o buscador
    hc = HillClimbSearch(df_amostra)

    # 2. Inicializa o objeto de pontuação (Score) passando os dados para ele
    bic = BicScore(df_amostra)

    # 3. Executa a busca passando o OBJETO bic, e não uma string
    best_model = hc.estimate(scoring_method=bic)

    print("Estrutura aprendida (Arestas):")
    print(best_model.edges())

    graphs(best_model)

    return best_model.edges()

def bayesianModel():

    # criando o modelo final com a estrutura aprendida
    model = BayesianNetwork(trainingGraphStructure())

    # aprendendo as tabelas de probabilidade condicional usando os dados completos
    model.fit(df_bn, estimator=MaximumLikelihoodEstimator)

    # verificando se o modelo é válido
    assert model.check_model()
    print("Modelo treinado com sucesso!")

    return model

def infering():
    # inferência (Fazer perguntas para a IA)
    infer = VariableElimination(bayesianModel())

    # p1: Probabilidade das notas de Matemática dado Escola Privada
    print("Probabilidade Nota Matemática dado Escola Privada:")
    q1 = infer.query(variables=['Nota_Matematica'], evidence={'Escola': 'Privada'})
    print(q1)

    # p2: Probabilidade das notas de Matemática dado Escola Pública
    print("\nProbabilidade Nota Matemática dado Escola Pública:")
    q2 = infer.query(variables=['Nota_Matematica'], evidence={'Escola': 'Publica'})
    print(q2)
    graphic1(q1, q2)
    print("\nparadoxo de gênero (STEM vs Humanas)")
    # Hipótese: Meninos vão melhor em Matemática, Meninas em Redação?
    q_masc_mt = infer.query(['Nota_Matematica'], evidence={'Sexo': 'M'})
    q_fem_mt = infer.query(['Nota_Matematica'], evidence={'Sexo': 'F'})

    print(f"Prob. Matemática ALTA - Homens: {q_masc_mt.values[0]*100:.1f}% (Assumindo índice 0=Alta, verifique a ordem)")
    print(f"Prob. Matemática ALTA - Mulheres: {q_fem_mt.values[0]*100:.1f}%")

    q_masc_red = infer.query(['Nota_Redacao'], evidence={'Sexo': 'M'})
    q_fem_red = infer.query(['Nota_Redacao'], evidence={'Sexo': 'F'})
    print(f"Prob. Redação ALTA - Homens: {q_masc_red.values[0]*100:.1f}%")
    print(f"Prob. Redação ALTA - Mulheres: {q_fem_red.values[0]*100:.1f}%")

    print("\nCapital cultural vs financeiro")
    print("="*50)

    graphic2(q_masc_mt, q_fem_mt, q_masc_red, q_fem_red)
    # Hipótese: Mãe educada (G=Pós graduação) compensa Renda Baixa (B=Classe baixa)?
    # Nota: Q002 vai de A(1) a G(7). Q006 vai de A(1) a Q(17).

    # Cenário 1: Rico (17) mas Mãe sem estudo (1)
    try:
        q_rico_sem_estudo = infer.query(['Nota_Redacao'], evidence={'Renda': 17, 'Escolaridade_Mae': 1})
        print("Rico + Mãe sem estudo (Nota Alta):", q_rico_sem_estudo)
    except: print("Combinação rara nos dados (Rico/Mãe sem estudo).")

    # Cenário 2: Pobre (2) mas Mãe com Pós-Graduação (7)
    try:
        q_pobre_com_estudo = infer.query(['Nota_Redacao'], evidence={'Renda': 2, 'Escolaridade_Mae': 7})
        print("Pobre + Mãe Pós-Graduada (Nota Alta):", q_pobre_com_estudo)
    except: print("Combinação rara nos dados.")

    print("\nInclusão digital na escola pública")
    print("="*50)
    # Hipótese: Ter internet muda a situação para quem é de escola pública?

    # Pública SEM Internet
    q_pub_no_net = infer.query(['Nota_Redacao'], evidence={'Escola': 'Publica', 'Internet': 'Nao'})
    print("Escola Pública SEM Internet:\n", q_pub_no_net)

    # Pública COM Internet
    q_pub_yes_net = infer.query(['Nota_Redacao'], evidence={'Escola': 'Publica', 'Internet': 'Sim'})
    print("Escola Pública COM Internet:\n", q_pub_yes_net)

    graphic3(q_pub_no_net, q_pub_yes_net)