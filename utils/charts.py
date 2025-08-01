# utils/charts.py
import pandas as pd
import plotly.express as px

def plot_budget_line_chart(df):
    fig = px.line(
        df,
        x="Data",
        y="Custo Previsto (R$)",
        markers=True,
        title="Evolução do Custo Mensal Previsto",
    )
    fig.update_layout(
        xaxis_title="Mês",
        yaxis_title="Custo Previsto (R$)",
        hovermode="x unified"
    )
    fig.update_traces(
        hovertemplate="Mês: %{x}<br>Custo Previsto: R$ %{y:,.0f}<extra></extra>",
        line=dict(color="#007bff", width=3),
        marker=dict(size=8)
    )
    return fig

def plot_budget_pie_chart(df):
    # Verifica se existe pelo menos um projeto ativo
    if "Projetos Ativos" not in df.columns:
        return px.pie(values=[1], names=["Nenhum projeto"], title="Distribuição de Custo por Projeto")

    # Expande os projetos ativos separados por vírgula
    expanded_rows = []
    for _, row in df.iterrows():
        projetos = [p.strip() for p in row["Projetos Ativos"].split(",") if p.strip() and p.strip() != "Nenhum"]
        if projetos:
            custo_por_projeto = row["Custo Previsto (R$)"] / len(projetos)
            for projeto in projetos:
                expanded_rows.append({
                    "Projeto": projeto,
                    "Custo Previsto (R$)": custo_por_projeto
                })

    # Se nenhum projeto foi adicionado
    if not expanded_rows:
        return px.pie(values=[1], names=["Nenhum projeto"], title="Distribuição de Custo por Projeto")

    df_expandido = pd.DataFrame(expanded_rows)
    df_grouped = df_expandido.groupby("Projeto")["Custo Previsto (R$)"].sum().reset_index()
    df_grouped = df_grouped.sort_values(by="Custo Previsto (R$)", ascending=False)

    fig = px.pie(
        df_grouped,
        values="Custo Previsto (R$)",
        names="Projeto",
        title="Distribuição de Custo por Projeto",
        hole=0.4
    )
    fig.update_traces(
        textinfo="percent+label",
        hovertemplate="Projeto: %{label}<br>Custo: R$ %{value:,.0f}<extra></extra>",
    )
    return fig
