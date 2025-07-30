# utils/charts.py

import plotly.express as px

def plot_budget_line_chart(df):
    fig = px.line(
        df,
        x="Data",
        y="Custo Previsto (R$)",
        title="Evolução do Custo Mensal Previsto",
        markers=True
    )
    fig.update_layout(xaxis_title="Data", yaxis_title="Custo (R$)")
    return fig


def plot_budget_pie_chart(df):
    df_grouped = df.groupby("Projetos Ativos")["Custo Previsto (R$)"].sum().reset_index()
    fig = px.pie(
        df_grouped,
        values="Custo Previsto (R$)",
        names="Projetos Ativos",
        title="Distribuição de Custo por Projeto Ativo"
    )
    return fig
