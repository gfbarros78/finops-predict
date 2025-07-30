# utils/charts.py
import plotly.express as px


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
    df_grouped = df.groupby("Projeto")["Custo Previsto (R$)"].sum().reset_index()
    fig = px.pie(
        df_grouped,
        names="Projeto",
        values="Custo Previsto (R$)",
        title="📌 Distribuição por Projeto"
    )
    return fig