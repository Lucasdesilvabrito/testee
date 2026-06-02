from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
import import_ipynb
from Abstracao_dados import df

# =========================================================
# CÓPIA DO DATAFRAME
# =========================================================

df = df.copy()

# =========================================================
# CONVERSÃO DE TEMPO PARA MINUTOS NUMÉRICOS
# =========================================================

# duração individual
df['duracao_minutos'] = (
    pd.to_timedelta(df['duracao_minutos_individual'])
    .dt.total_seconds() / 60
)

# duração total por ticket
df['duracao_minutos_total'] = (
    pd.to_timedelta(df['duracao_minutos_total_por_ticket'])
    .dt.total_seconds() / 60
)

# =========================================================
# TRATAMENTO DE DATA
# =========================================================

df['data_atualizacao'] = pd.to_datetime(
    df['data_atualizacao'],
    errors='coerce'
)

# =========================================================
# PERÍODO DOS DADOS
# =========================================================

data_inicio = (
    df['data_atualizacao']
    .min()
    .strftime('%d/%m/%Y')
)

data_fim = (
    df['data_atualizacao']
    .max()
    .strftime('%d/%m/%Y')
)

dias_analisados = (
    df['data_atualizacao'].max()
    -
    df['data_atualizacao'].min()
).days

# =========================================================
# KPI'S
# =========================================================

total_tickets = df['id_ticket'].nunique()

tempo_medio = round(
    df['duracao_minutos_total'].mean(),
    2
)

problema_cti = round(
    (
        df['problema_nosso']
        .astype(str)
        .str.lower()
        .str.contains('sim', na=False)
        .mean()
    ) * 100,
    2
)

total_servicos = df['servico'].nunique()

total_colaboradores = df['colaborador'].nunique()

ticket_mais_comum = (
    df['categoria']
    .dropna()
    .value_counts()
    .idxmax()
)

# =========================================================
# GRÁFICO 1 - PROBLEMA NOSSO
# =========================================================

fig_problema = px.pie(
    df,
    names='problema_nosso',
    hole=0.5
)

fig_problema.update_traces(
    marker=dict(
        colors=['#08519c', '#3182bd']
    )
)

fig_problema.update_layout(
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=10, r=10, t=30, b=10)
)

# =========================================================
# GRÁFICO 2 - TIPOS DE TICKET
# =========================================================

categoria_count = (
    df['categoria']
    .value_counts()
    .reset_index()
)

categoria_count.columns = [
    'categoria',
    'quantidade'
]

fig_categoria = px.bar(
    categoria_count,
    x='quantidade',
    y='categoria',
    orientation='h',
    text='quantidade'
)

fig_categoria.update_traces(
    marker_color='#4a90e2'
)

fig_categoria.update_layout(
    xaxis_title='Quantidade',
    yaxis_title='Categoria',
    paper_bgcolor='white',
    plot_bgcolor='white',
    yaxis=dict(
        categoryorder='total ascending'
    )
)

# =========================================================
# GRÁFICO 3 - TEMPO MÉDIO POR MEIO
# =========================================================

tempo_por_meio = (
    df.groupby('meio')['duracao_minutos']
    .mean()
    .reset_index()
    .sort_values(
        by='duracao_minutos',
        ascending=False
    )
)

fig_tempo_meio = px.bar(
    tempo_por_meio,
    x='meio',
    y='duracao_minutos',
    text_auto='.2f'
)

fig_tempo_meio.update_traces(
    marker_color='#4a90e2'
)

fig_tempo_meio.update_layout(
    xaxis_title='Meio',
    yaxis_title='Tempo Médio (Min)',
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# =========================================================
# GRÁFICO 4 - MÉDIA DE TEMPO MENSAL
# =========================================================

df['mes'] = (
    df['data_atualizacao']
    .dt.strftime('%Y-%m')
)

tempo_mensal = (
    df.groupby('mes')['duracao_minutos']
    .mean()
    .reset_index()
)

fig_tempo_mensal = px.line(
    tempo_mensal,
    x='mes',
    y='duracao_minutos',
    markers=True
)

fig_tempo_mensal.update_traces(
    line_color='#4a90e2',
    marker_color='#4a90e2'
)

fig_tempo_mensal.update_layout(
    xaxis_title='Mês',
    yaxis_title='Tempo Médio (Min)',
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# =========================================================
# GRÁFICO 5 - TEMPO POR SERVIÇO
# =========================================================

tempo_por_servico = (
    df.groupby('servico')['duracao_minutos_total']
    .mean()
    .reset_index()
    .sort_values(by='duracao_minutos_total', ascending=False)
    .head(10)
)

tempo_por_servico.columns = [
    'servico',
    'tempo_medio'
]

fig_servicos = px.bar(
    tempo_por_servico,
    x='tempo_medio',
    y='servico',
    orientation='h',
    text_auto='.2f',
    color='tempo_medio',
    color_continuous_scale='Blues'
)

fig_servicos.update_traces(
    textposition='auto'
)

fig_servicos.update_layout(
    xaxis_title='Tempo Médio (Min)',
    yaxis_title='Serviço',
    paper_bgcolor='white',
    plot_bgcolor='white',
    yaxis=dict(
        categoryorder='total ascending'
    ),
    coloraxis_showscale=False
)

# =========================================================
# GRÁFICO 6 - TICKETS POR ATENDENTE
# =========================================================

atendente_count = (
    df['colaborador']
    .value_counts()
    .reset_index()
    .head(15)
)

atendente_count.columns = [
    'Colaborador',
    'quantidade'
]

fig_classificacao = px.bar(
    atendente_count,
    x='quantidade',
    y='Colaborador',
    orientation='h',
    text='quantidade',
    color='quantidade',
    color_continuous_scale='Blues'
)

fig_classificacao.update_traces(
    textposition='auto'
)

fig_classificacao.update_layout(
    xaxis_title='Quantidade de Tickets',
    yaxis_title='Colaborador',
    paper_bgcolor='white',
    plot_bgcolor='white',
    yaxis=dict(
        categoryorder='total ascending'
    ),
    coloraxis_showscale=False
)

# =========================================================
# ESTILOS - PALETA EMPRESARIAL
# =========================================================

BACKGROUND = '#ecf0f1'
PRIMARY = '#1a3a52'
SECONDARY = '#2980b9'

CARD_STYLE = {
    'backgroundColor': 'white',
    'padding': '15px',
    'borderRadius': '10px',
    'boxShadow': '0px 2px 6px rgba(0,0,0,0.1)',
    'margin': '10px',
    'flex': '1',
    'minWidth': '350px'
}

KPI_STYLE = {
    'backgroundColor': 'white',
    'padding': '20px',
    'borderRadius': '10px',
    'textAlign': 'center',
    'boxShadow': '0px 2px 6px rgba(0,0,0,0.1)',
    'flex': '1',
    'margin': '10px',
    'borderTop': f'5px solid {SECONDARY}',
    'minWidth': '220px'
}

TITLE_STYLE = {
    'fontSize': '18px',
    'fontWeight': 'bold',
    'marginBottom': '10px',
    'color': PRIMARY,
    'fontFamily': 'Arial'
}

# =========================================================
# APP
# =========================================================

app = Dash(__name__)


# =========================================================
# LAYOUT
# =========================================================

app.layout = html.Div(

    style={
        'backgroundColor': BACKGROUND,
        'padding': '20px',
        'fontFamily': 'Arial'
    },

    children=[

        # =================================================
        # HEADER
        # =================================================

        html.Div(
            children='Dashboard Empresarial - CTI',

            style={
                'backgroundColor': PRIMARY,
                'color': 'white',
                'padding': '20px',
                'borderRadius': '10px',
                'fontSize': '28px',
                'fontWeight': 'bold',
                'textAlign': 'center',
                'marginBottom': '20px'
            }
        ),

        # =================================================
        # PERÍODO ANALISADO
        # =================================================

        html.Div(

            children=[
                html.H3(
                    f'Dados analisados de {data_inicio} até {data_fim} | {dias_analisados} dias analisados'
                )
            ],

            style={
                'background': 'linear-gradient(to right, #003366, #0055aa)',
                'padding': '12px',
                'borderRadius': '10px',
                'marginBottom': '20px',
                'textAlign': 'center',
                'color': 'white',
                'fontWeight': 'bold',
                'fontSize': '18px',
                'boxShadow': '0px 2px 6px rgba(0,0,0,0.2)'
            }
        ),

        # =================================================
        # KPI'S
        # =================================================

        html.Div(

            style={
                'display': 'flex',
                'flexWrap': 'wrap'
            },

            children=[

                html.Div(style=KPI_STYLE, children=[
                    html.H3('🎫 Total Tickets'),
                    html.H1(total_tickets)
                ]),

                html.Div(style=KPI_STYLE, children=[
                    html.H3('⏱ Tempo Médio'),
                    html.H1(f'{tempo_medio:.2f} min')
                ]),

                html.Div(style=KPI_STYLE, children=[
                    html.H3('⚠ Problema CTI'),
                    html.H1(f'{problema_cti}%')
                ]),

                html.Div(style=KPI_STYLE, children=[
                    html.H3('🛠 Serviços'),
                    html.H1(total_servicos)
                ]),

                html.Div(style=KPI_STYLE, children=[
                    html.H3('� Colaboradores'),
                    html.H1(total_colaboradores)
                ]),

                html.Div(style=KPI_STYLE, children=[
                    html.H3('�📌 Ticket Mais Comum'),
                    html.H1(ticket_mais_comum)
                ]),
            ]
        ),

        # =================================================
        # PRIMEIRA LINHA
        # =================================================

        html.Div(

            style={
                'display': 'flex',
                'flexWrap': 'wrap'
            },

            children=[

                html.Div(style=CARD_STYLE, children=[
                    html.Div(
                        "Problema Nosso x Não Nosso",
                        style=TITLE_STYLE
                    ),
                    dcc.Graph(figure=fig_problema)
                ]),

                html.Div(style=CARD_STYLE, children=[
                    html.Div(
                        "Tipos de Ticket",
                        style=TITLE_STYLE
                    ),
                    dcc.Graph(figure=fig_categoria)
                ]),

                html.Div(style=CARD_STYLE, children=[
                    html.Div(
                        "Tempo Médio Mensal",
                        style=TITLE_STYLE
                    ),
                    dcc.Graph(figure=fig_tempo_mensal)
                ])
            ]
        ),

        # =================================================
        # SEGUNDA LINHA
        # =================================================

        html.Div(

            style={
                'display': 'flex',
                'flexWrap': 'wrap'
            },

            children=[

                html.Div(style=CARD_STYLE, children=[
                    html.Div(
                        "Tempo Médio por Meio",
                        style=TITLE_STYLE
                    ),
                    dcc.Graph(figure=fig_tempo_meio)
                ]),

                html.Div(style=CARD_STYLE, children=[
                    html.Div(
                        "Tempo Médio por Serviço",
                        style=TITLE_STYLE
                    ),
                    dcc.Graph(figure=fig_servicos)
                ]),

                html.Div(style=CARD_STYLE, children=[
                    html.Div(
                        "Top Atendentes por Tickets",
                        style=TITLE_STYLE
                    ),
                    dcc.Graph(figure=fig_classificacao)
                ])
            ]
        )
    ]
)

# =========================================================
# EXECUÇÃO
# =========================================================

if __name__ == '__main__':
    app.run(
        debug=True,
        port=8050
    )