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

start_month = st.sidebar.selectbox("Mês de Início do Forecast", list(range(1, 13)), index=0)
start_year = st.sidebar.number_input("Ano de Início do Forecast", value=2025, step=1)
growth_rate_total = st.sidebar.slider("Crescimento ou Redução (%) ao ano", -50, 50, 5)
duration_months = st.sidebar.slider("Duração (meses)", 3, 60, 12)
monthly_growth_rate = round(growth_rate_total / 12, 4)

# Sidebar - Projetos
st.sidebar.header("📌 Dados dos Projetos")

if "projects" not in st.session_state:
    st.session_state.projects = []

# Variáveis de estado para manter os valores entre execuções
if "form_cost" not in st.session_state:
    st.session_state.form_cost = 0.0

# Formulário
with st.sidebar.form(key="project_form", clear_on_submit=False):
    name = st.text_input("Nome do Projeto")
    cost = st.number_input("Custo Mensal (R$)", min_value=0.0, step=100.0, format="%.2f", value=st.session_state.form_cost, key="cost_input")

    if st.session_state.cost_input > 0:
        cost_formatado = f"R$ {st.session_state.cost_input:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
        st.markdown(f"Valor inserido: **{cost_formatado}**")

    start_month_proj = st.selectbox("Mês de Início", list(range(1, 13)), index=2)
    start_year_proj = st.number_input("Ano de Início", value=2025, step=1)
    end_month_proj = st.selectbox("Mês de Fim", list(range(1, 13)), index=5)
    end_year_proj = st.numb
