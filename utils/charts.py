# utils/charts.py
import plotly.express as px
import pandas as pd


def plot_budget_line_chart(df):
    fig = px.line(
        df,
        x="Data",
        y="Custo Previsto (R$)",
        title="📈 Evolução Mensal do Orçamento",
        markers=True
    )
    fig.update_layout(xaxis_title="Data", yaxis_title="R$", hovermode="x unified")
    return fig


def plot_budget_pie_chart(df):
    df_expandido = []

    for _, row in df.iterrows():
        projetos_ativos = row.get("Projetos Ativos", "")
        if projetos_ativos and projetos_ativos != "Nenhum":
            projetos = [proj.strip() for proj in projetos_ativos.split(",")]
            valor_total = row["Custo Previsto (R$)"]
            valor_individual = valor_total / len(projetos)
            for proj in projetos:
                df_expandido.append({"Projeto": proj, "Custo Previsto (R$)": valor_individual})

    if not df_expandido:
        return px.pie(
            names=["Nenhum projeto"],
            values=[1],
            title="📌 Distribuição por Projeto (Sem dados)"
        )

    df_grouped = pd.DataFrame(df_expandido).groupby("Projeto")["Custo Previsto (R$)"].sum().reset_index()

    fig = px.pie(
        df_grouped,
        names="Projeto",
        values="Custo Previsto (R$)",
        title="📌 Distribuição por Projeto",
        hole=0.4
    )

    fig.update_traces(textinfo="percent+label", hovertemplate='%{label}: R$ %{value:,.0f}<extra></extra>')
    return fig
