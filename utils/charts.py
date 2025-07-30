# utils/charts.py
import plotly.express as px
import plotly.graph_objects as go


def plot_budget_line_chart(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Data"],
        y=df["Custo Previsto (R$)"],
        mode="lines+markers",
        name="Custo Previsto",
        hovertemplate="<b>Mês:</b> %{x}<br><b>Custo:</b> R$ %{y:,.0f}<extra></extra>",
        line=dict(color="royalblue")
    ))

    fig.update_layout(
        title="📈 Evolução do Custo Mensal Previsto",
        xaxis_title="Data",
        yaxis_title="Custo Previsto (R$)",
        hovermode="x unified"
    )

    return fig


def plot_budget_pie_chart(df):
    if "Projeto" in df.columns:
        df_grouped = df.groupby("Projeto")["Custo Previsto (R$)"].sum().reset_index()
    else:
        # Expande "Projetos Ativos" para cada projeto individual
        df_expandido = []
        for _, row in df.iterrows():
            projetos = row["Projetos Ativos"].split(", ")
            for proj in projetos:
                if proj != "Nenhum":
                    df_expandido.append({
                        "Projeto": proj,
                        "Custo Previsto (R$)": row["Custo Previsto (R$)"] / len(projetos)
                    })
        df_grouped = pd.DataFrame(df_expandido).groupby("Projeto")["Custo Previsto (R$)"].sum().reset_index()

    fig = px.pie(
        df_grouped,
        names="Projeto",
        values="Custo Previsto (R$)",
        title="📌 Distribuição por Projeto"
    )
    return fig
