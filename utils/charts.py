# utils/charts.py

import plotly.express as px

def plot_budget_line_chart(df):
    fig = px.line(
        df,
        x="Data",
        y="Custo Previsto (R$)",
        title="📈 Evolução do Custo Mensal Previsto",
        markers=True
    )
    fig.update_traces(hovertemplate="Mês: %{x}<br>Custo: R$ %{y:,.0f}")
    return fig

def plot_budget_pie_chart(df):
    # Verifica se 'Projetos Ativos' existe e há dados válidos
    if "Projetos Ativos" in df.columns and df["Projetos Ativos"].notna().any():
        # Cria cópias separadas para cada projeto em cada mês
        expanded_rows = []
        for _, row in df.iterrows():
            projetos = [p.strip() for p in row["Projetos Ativos"].split(",")]
            if projetos == ["Nenhum"]:
                continue
            custo_por_projeto = row["Custo Previsto (R$)"] / len(projetos)
            for projeto in projetos:
                expanded_rows.append({
                    "Projeto": projeto,
                    "Custo Previsto (R$)": custo_por_projeto
                })

        df_expandido = px.data.tips()  # fallback
        if expanded_rows:
            df_expandido = pd.DataFrame(expanded_rows)
            df_grouped = df_expandido.groupby("Projeto")["Custo Previsto (R$)"].sum().reset_index()

            fig = px.pie(
                df_grouped,
                names="Projeto",
                values="Custo Previsto (R$)",
                title="🥧 Distribuição de Custo por Projeto"
            )
            return fig
    # Se não houver dados válidos para o gráfico
    return px.pie(title="🥧 Nenhum projeto com custo registrado")
