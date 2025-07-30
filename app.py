# app.py
import streamlit as st
from services.simulator import simulate_budget
from utils.csv_export import export_to_csv
from utils.charts import plot_budget_line_chart, plot_budget_pie_chart
import pandas as pd

st.set_page_config(page_title="FinOpsPredict Pro", layout="wide")
st.title("💰 FinOpsPredict Pro - Planejamento Orçamentário em Cloud")

# Sidebar - Parâmetros do Forecast
st.sidebar.header("🔧 Parâmetros do Forecast")
baseline_value = st.sidebar.number_input("Baseline em R$", min_value=0.0, step=100.0, value=0.0, format="%.2f")
if baseline_value > 0:
    baseline_formatado = f"R$ {baseline_value:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    st.sidebar.markdown(f"Valor inserido: **{baseline_formatado}**")

# Sidebar - Dados do Projeto
st.sidebar.header("📌 Dados do Projeto")
project_name = st.sidebar.text_input("Nome do Projeto", "Projeto X")
scenario = st.sidebar.selectbox("Cenário", ["Crescimento Vegetativo", "Novo Projeto", "Otimização de Custos"])
start_month = st.sidebar.selectbox("Mês de Início do Forecast", list(range(1, 13)), index=0)
start_year = st.sidebar.number_input("Ano de Início do Forecast", value=2025, step=1)

project_month = st.sidebar.selectbox("Mês de Entrada do Projeto", list(range(1, 13)), index=2)
project_year = st.sidebar.number_input("Ano de Entrada do Projeto", value=2025, step=1)

project_cost = st.sidebar.number_input("Custo Mensal do Projeto (R$)", value=0.0, step=1000.0, format="%.2f")
if project_cost > 0:
    project_cost_formatado = f"R$ {project_cost:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    st.sidebar.markdown(f"Valor inserido: **{project_cost_formatado}**")

growth_rate_total = st.sidebar.slider("Crescimento ou Redução (%) ao ano", -50, 50, 5)
duration_months = st.sidebar.slider("Duração (meses)", 3, 60, 12)

# Converte o crescimento anual em mensal
monthly_growth_rate = round(growth_rate_total / 12, 4)

# Simulação
if st.sidebar.button("Simular Orçamento"):
    df = simulate_budget(
        project_name=project_name,
        scenario=scenario,
        start_month=start_month,
        start_year=start_year,
        baseline_cost=baseline_value,
        monthly_growth_rate=monthly_growth_rate,
        duration_months=duration_months,
        project_cost=project_cost,
        project_month=project_month,
        project_year=project_year
    )

    st.subheader("📊 Resultado da Simulação")
    st.dataframe(df, use_container_width=True)

    st.download_button(
        label="⬇️ Exportar CSV",
        data=export_to_csv(df),
        file_name="orcamento_cloud.csv",
        mime="text/csv"
    )

    st.plotly_chart(plot_budget_line_chart(df), use_container_width=True)
    st.plotly_chart(plot_budget_pie_chart(df), use_container_width=True)
else:
    st.info("Preencha os dados ao lado e clique em 'Simular Orçamento'.")
    st.caption("Desenvolvido com ❤️ seguindo as práticas FinOps.")
