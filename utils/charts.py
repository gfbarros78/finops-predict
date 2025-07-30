import plotly.express as px

def plot_budget_line_chart(df):
    df_plot = df.groupby("Data")["Custo Previsto (R$)"].sum().reset_index()

    # Formata valor para exibir no tooltip como número inteiro com separador de milhar brasileiro
    df_plot["Custo Formatado"] = df_plot["Custo Previsto (R$)"].apply(
        lambda x: f"R$ {int(x):,}".replace(",", "v").replace(".", ",").replace("v", ".")
    )

    fig = px.line(
        df_plot,
        x="Data",
        y="Custo Previsto (R$)",
        markers=True,
        title="Evolução do Custo Mensal Previsto",
        custom_data=["Custo Formatado"]
    )

    fig.update_traces(
        hovertemplate="Data=%{x}<br>Custo Previsto (R$)=%{customdata[0]}<extra></extra>"
    )

    fig.update_layout(yaxis_title="Custo (R$)", xaxis_title="Data")
    return fig


def plot_budget_pie_chart(df):
    df_grouped = df.groupby("Projeto")["Custo Previsto (R$)"].sum().reset_index()

    fig = px.pie(
        df_grouped,
        names="Projeto",
        values="Custo Previsto (R$)",
        title="Distribuição de Custos por Projeto"
    )

    fig.update_traces(textinfo='percent+label')
    return fig
