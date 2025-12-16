import networkx as nx
from etl import pd
from pyvis.network import Network
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from networkDefinition import df_bn

def graphs(best_model):
    # objeto de visualização
    G = nx.DiGraph()
    G.add_edges_from(best_model.edges())

    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, k=0.7, iterations=60)

    nx.draw(
        G, pos, with_labels=True,
        node_size=5000, node_color="skyblue",
        font_size=9, font_weight="bold",
        width=1.5, arrowsize=25
    )

    net = Network(notebook=True, directed=True)
    net.from_nx(G)

    net.toggle_physics(True)
    net.show("rede_bayesiana.html")

    plt.title("Rede Bayesiana - Gênero, Renda, Cultura e Internet no ENEM 2023", fontsize=15)
    plt.show()

def graphic1(q1, q2):
    categorias = q1.state_names['Nota_Matematica'] # Ex: ['Baixa', 'Média', 'Alta']

    data = {
        'Nota_Matematica': categorias,
        'Privada': q1.values, # Valores de probabilidade para Escola Privada
        'Publica': q2.values  # Valores de probabilidade para Escola Pública
    }

    df_plot1 = pd.DataFrame(data).set_index('Nota_Matematica')

    # Gerar Gráfico de Barras Agrupadas
    plt.figure(figsize=(10, 6))
    df_plot1.T.plot(kind='bar', ax=plt.gca(), rot=0)

    plt.title('Probabilidade da Nota de Matemática por Tipo de Escola')
    plt.xlabel('Tipo de Escola')
    plt.ylabel('Probabilidade')
    plt.legend(title='Categoria da Nota')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    plt.tight_layout()
    plt.show()

def graphic2(q_masc_mt, q_fem_mt, q_masc_red, q_fem_red):
    idx_alta = 0

    prob_masc_mt_alta = q_masc_mt.values[idx_alta]
    prob_fem_mt_alta = q_fem_mt.values[idx_alta]
    prob_masc_red_alta = q_masc_red.values[idx_alta]
    prob_fem_red_alta = q_fem_red.values[idx_alta]

    data = {
        'Matemática (Alta)': [prob_masc_mt_alta, prob_fem_mt_alta],
        'Redação (Alta)': [prob_masc_red_alta, prob_fem_red_alta]
    }

    df_plot2 = pd.DataFrame(data, index=['Homens (M)', 'Mulheres (F)'])

    # Gerar Gráfico de Barras Agrupadas
    plt.figure(figsize=(10, 6))
    df_plot2.plot(kind='bar', ax=plt.gca(), rot=0)

    plt.title('Probabilidade de Nota ALTA por Área e Gênero')
    plt.xlabel('Gênero')
    plt.ylabel('Probabilidade (P[Nota Alta])')
    plt.legend(title='Área de Conhecimento')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    plt.tight_layout()
    plt.show()

def graphic3(q_pub_no_net, q_pub_yes_net):
    categorias_red = q_pub_no_net.state_names['Nota_Redacao'] # Ex: ['Baixa', 'Média', 'Alta']

    data = {
        'Nota_Redacao': categorias_red,
        'Pública SEM Internet': q_pub_no_net.values,
        'Pública COM Internet': q_pub_yes_net.values
    }

    df_plot3 = pd.DataFrame(data).set_index('Nota_Redacao')

    # Gerar Gráfico de Barras Agrupadas
    plt.figure(figsize=(10, 6))
    df_plot3.T.plot(kind='bar', ax=plt.gca(), rot=0)

    plt.title('Probabilidade da Nota de Redação na Escola Pública: Com vs. Sem Internet')
    plt.xlabel('Cenário de Acesso')
    plt.ylabel('Probabilidade')
    plt.legend(title='Categoria da Nota')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    plt.tight_layout()
    plt.show()

def graphic4():
    df_plot_renda = df_bn.dropna(subset=['Renda', 'Nota_Matematica']).copy()

    # Calcula, para cada nível de renda, a proporção de Nota_Matematica = 'Alta'
    prob_alta_por_renda = (
        df_plot_renda
        .assign(is_alta = df_plot_renda['Nota_Matematica'] == 'Alta')
        .groupby('Renda')['is_alta']
        .mean()
        .reset_index()
    )

    plt.figure(figsize=(10, 6))
    plt.plot(prob_alta_por_renda['Renda'], prob_alta_por_renda['is_alta'], marker='o')
    plt.title('Probabilidade de Nota ALTA em Matemática por Nível de Renda')
    plt.xlabel('Renda (Q006_ord – categorias crescentes)')
    plt.ylabel('P(Nota Matemática = Alta)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.show()

def graphic5():
    df_plot_regiao = df_bn.dropna(subset=['Regiao', 'Nota_Matematica']).copy()

    prob_alta_por_regiao = (
        df_plot_regiao
        .assign(is_alta = df_plot_regiao['Nota_Matematica'] == 'Alta')
        .groupby('Regiao')['is_alta']
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    plt.figure(figsize=(10, 6))
    plt.bar(prob_alta_por_regiao['Regiao'], prob_alta_por_regiao['is_alta'])
    plt.title('Probabilidade de Nota ALTA em Matemática por Região')
    plt.xlabel('Região')
    plt.ylabel('P(Nota Matemática = Alta)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.show()

def graphic6():
    # Usa apenas colunas relevantes
    df_sankey = df_bn[['Renda', 'Escola', 'Nota_Matematica']].dropna().copy()

    # Converte tudo para string (plotly gosta de labels texto)
    df_sankey['Renda_str'] = 'Renda: ' + df_sankey['Renda'].astype(int).astype(str)
    df_sankey['Escola_str'] = 'Escola: ' + df_sankey['Escola'].astype(str)
    df_sankey['Nota_str'] = 'Nota Mat: ' + df_sankey['Nota_Matematica'].astype(str)

    # Lista de todos os nós (labels)
    labels = list(
        pd.unique(
            pd.concat([df_sankey['Renda_str'], df_sankey['Escola_str'], df_sankey['Nota_str']])
        )
    )

    label_to_idx = {lab: i for i, lab in enumerate(labels)}

    # Fluxo Renda → Escola
    links_RE = (
        df_sankey
        .groupby(['Renda_str', 'Escola_str'])
        .size()
        .reset_index(name='count')
    )

    # Fluxo Escola → Nota
    links_EN = (
        df_sankey
        .groupby(['Escola_str', 'Nota_str'])
        .size()
        .reset_index(name='count')
    )

    # Monta listas source/target/value
    source = []
    target = []
    value  = []

    # Renda → Escola
    for _, row in links_RE.iterrows():
        source.append(label_to_idx[row['Renda_str']])
        target.append(label_to_idx[row['Escola_str']])
        value.append(row['count'])

    # Escola → Nota
    for _, row in links_EN.iterrows():
        source.append(label_to_idx[row['Escola_str']])
        target.append(label_to_idx[row['Nota_str']])
        value.append(row['count'])

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(width=0.5),
            label=labels,
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
        )
    )])

    fig.update_layout(
        title_text="Fluxo: Renda → Tipo de Escola → Nota em Matemática",
        font_size=10
    )
    fig.show()