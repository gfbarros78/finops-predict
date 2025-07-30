# utils/charts.py

import pandas as pd
import plotly.express as px

def plot_budget_line_chart(df: pd.DataFrame):
    fig = px.line(
        df,
        x="Data",
        y="Custo Previsto (R$)",
        title="📈 Evolução do Custo Mensal Previsto",
        markers=True
    )
    fig.update_traces(hovertemplate="Mês: %{x}<br>Custo: R$ %{y:,.0f}")
    fig.update_layout(xaxis_title="Data", yaxis_title="Custo Previsto (R$)")
    return fig

def plot_budget_pie_chart(df: pd.DataFrame):
    # Verifica se existe a coluna "Projetos Ativos"
    if "Projetos Ativos" not in df.columns:
        return px.pie(names=["Sem Projetos"], values=[1], title="🧁 Distribuição por Projeto")

    # Expande os projetos ativos (caso haja múltiplos por linha)
    expanded_rows = []
    for _, row in df.iterrows():
        projetos = [p.strip() for p in row["Projetos Ativos"].split(",") if p.strip() and p.strip().lower() != "nenhum"]
        if not projetos:
            continue
        valor_unitario = row["Custo Previsto (R$)"] / len(projetos)
        for projeto in projetos:
            expanded_rows.append({
                "Projeto": projeto,
                "Custo Previsto (R$)": valor_unitario
            })

    if not expanded_rows:
        return px.pie(names=["Sem Projetos"], values=[1], title="🧁 Distribuição por Projeto")

    df_expandido = pd.DataFrame(expanded_rows)
    df_grouped = df_expandido.groupby("Projeto")["Custo Previsto (R$)"].sum().reset_index()

    fig = px.pie(
        df_grouped,
        names="Projeto",
        values="Custo Previsto (R$)",
        title="🧁 Distribuição por Projeto"
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig
