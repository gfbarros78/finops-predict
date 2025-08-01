# utils/charts.py

import plotly.graph_objects as go
import pandas as pd

def plot_budget_line_chart(df):
    df["Data"] = pd.to_datetime(df["Data"], format="%m-%Y")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Data"],
        y=df["Custo Previsto (R$)"],
        mode="lines+markers",
        name="Custo Previsto",
        hovertemplate="R$ %{y:,.0f}<extra></extra>"
    ))
    fig.update_layout(title="Evolução do Custo Mensal Previsto", xaxis_title="Data", yaxis_title="Custo (R$)")
    return fig


def plot_budget_pie_chart(df):
    if "Projetos Ativos" not in df.columns:
        return go.Figure()

    rows = []
    for _, row in df.iterrows():
        projetos = row["Projetos Ativos"].split(", ") if row["Projetos Ativos"] != "Nenhum" else []
        for projeto in projetos:
            rows.append({
                "Projeto": projeto,
                "Custo Previsto (R$)": row["Custo Previsto (R$)"] / len(projetos) if projetos else 0
            })

    if not rows:
        return go.Figure()

    df_grouped = pd.DataFrame(rows).groupby("Projeto")["Custo Previsto (R$)"].sum().reset_index()

    fig = go.Figure(data=[go.Pie(
        labels=df_grouped["Projeto"],
        values=df_grouped["Custo Previsto (R$)"],
        hovertemplate="R$ %{value:,.0f}<extra></extra>"
    )])
    fig.update_layout(title="Distribuição de Custo por Projeto")
    return fig
