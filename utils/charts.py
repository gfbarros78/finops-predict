import plotly.express as px
import pandas as pd

def plot_budget_line_chart(df: pd.DataFrame):
    fig = px.line(
        df,
        x="Data",
        y="Custo Previsto (R$)",
        markers=True,
        title="Evolução do Custo Mensal Previsto",
        hover_data={"Custo Previsto (R$)": ":,.0f"}
    )
    fig.update_traces(line=dict(color="royalblue", width=3))
    fig.update_layout(
        title_x=0.5,
        yaxis_title="Custo (R$)",
        xaxis_title="Mês",
        hoverlabel=dict(bgcolor="white", font_size=14),
    )
    return fig

def plot_budget_pie_chart(df: pd.DataFrame):
    if "Projetos Ativos" not in df.columns:
        return px.pie(title="Nenhum projeto adicionado.")

    # Expande a coluna de projetos para calcular o total por projeto
    expanded_rows = []
    for _, row in df.iterrows():
        projetos = [p.strip() for p in row["Projetos Ativos"].split(",")] if row["Projetos Ativos"] != "Nenhum" else []
        valor = row["Custo Previsto (R$)"]
        if projetos:
            valor_por_projeto = valor / len(projetos)
            for projeto in projetos:
                expanded_rows.append({
                    "Projeto": projeto,
                    "Custo Previsto (R$)": valor_por_projeto
                })

    if not expanded_rows:
        return px.pie(title="Nenhum projeto com custo atribuído.")

    df_expandido = pd.DataFrame(expanded_rows)
    df_grouped = df_expandido.groupby("Projeto")["Custo Previsto (R$)"].sum().reset_index()

    df_grouped["Custo Previsto (R$)"] = df_grouped["Custo Previsto (R$)"].apply(
        lambda x: round(x)
    )

    fig = px.pie(
        df_grouped,
        names="Projeto",
        values="Custo Previsto (R$)",
        title="Distribuição de Custos por Projeto"
    )
    fig.update_layout(title_x=0.5)
    return fig
