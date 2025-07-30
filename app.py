# app.py
import streamlit as st
from services.simulator import simulate_budget
from utils.csv_export import export_to_csv
from utils.charts import plot_budget_line_chart, plot_budget_pie_chart
import pandas as pd

st.set_page_config(page_title="FinOpsPredict Pro", layout="wide")
st.title("\U0001F4B0 FinOpsPredict Pro - Planejamento Orçamentário em Cloud")

# Sidebar - Entrada de dados
st.sidebar.header("\U0001F527 Parâmetros do Forecast")
baseline_value = st.sidebar.number_input("Baseline em R$", min_value=0.0, value=0.00, step=100.0, format="%.2f")
if baseline_value:
    st.sidebar.markdown(f"**Valor inserido:** R$ {baseline_value:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
else:
    st.sidebar.markdown("**Valor inserido:**")

st.sidebar.header("\U0001F4CC Dados do Projeto")
project_name = st.sidebar.text_input("Nome do Projeto", "Projeto X")
scenario = st.sidebar.selectbox("Cenário", ["Crescimento Vegetativo", "Novo Projeto", "Otimização de Custos"])
start_month = st.sidebar.selectbox("Mês de Início", list(range(1, 13)), index=0)
start_year = st.sidebar.number_input("Ano de Início", value=2025, step=1)
end_month = st.sidebar.selectbox("Mês de Fim", list(range(1, 13)), index=11)
end_year = st.sidebar.number_input("Ano de Fim", value=2025, step=1)
monthly_cost = st.sidebar.number_input("Custo Inicial Mensal (R$)", min_value=0.0, value=0.00, step=100.0, format="%.2f")
if monthly_cost:
    st.sidebar.markdown(f"**Valor inserido:** R$ {monthly_cost:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
else:
    st.sidebar.markdown("**Valor inserido:**")

growth_rate = st.sidebar.slider("Crescimento ou Redução (%) total no período", -100, 100, 12)

# Simulação
df = None
if st.sidebar.button("Simular Orçamento"):
    df = simulate_budget(
        project_name,
        scenario,
        start_month,
        start_year,
        baseline_value,
        growth_rate,
        end_month,
        end_year
    )

    st.subheader("\U0001F4CA Resultado da Simulação")

    # Formatar dados para exibição
    df_exibicao = df.copy()
    df_exibicao["Mês"] = pd.to_datetime(df_exibicao["Data"], format="%m-%Y").dt.strftime("%B").str.capitalize()
    df_exibicao["Custo Previsto (R$)"] = df_exibicao["Custo Previsto (R$)"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
    df_exibicao = df_exibicao[["Data", "Mês", "Custo Previsto (R$)", "Projeto"]]

    st.dataframe(df_exibicao, use_container_width=True)

    st.download_button(
        label="⬇️ Exportar CSV",
        data=export_to_csv(df),
        file_name="orcamento_cloud.csv",
        mime="text/csv"
    )

    st.plotly_chart(plot_budget_line_chart(df), use_container_width=True)

    pie_chart = plot_budget_pie_chart(df)
    if pie_chart:
        st.plotly_chart(pie_chart, use_container_width=True)
else:
    st.info("Preencha os dados ao lado e clique em 'Simular Orçamento'.")
    st.caption("Desenvolvido com ❤️ seguindo as práticas FinOps.")
