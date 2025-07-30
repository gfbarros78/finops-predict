# utils/charts.py
import plotly.express as px

def plot_budget_line_chart(df):
    fig = px.line(
        df,
        x="Data",
        y="Custo",
        title="📈 Evolução Mensal do Orçamento",
        markers=True,
        color="Projeto"
    )
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Custo (R$)",
        hovermode="x unified"
    )
    fig.update_traces(hovertemplate='Data: %{x}<br>Custo: R$ %{y:,.2f}')
    return fig

def plot_budget_pie_chart(df):
    df_grouped = df.groupby("Projeto")["Custo"].sum().reset_index()
    fig = px.pie(
        df_grouped,
        names="Projeto",
        values="Custo",
        title="📌 Distribuição por Projeto"
    )
    fig.update_traces(textinfo='label+percent', hovertemplate='Projeto: %{label}<br>Custo: R$ %{value:,.2f}')
    return fig
