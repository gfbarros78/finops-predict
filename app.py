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

# Projetos
st.sidebar.header("📌 Dados dos Projetos")
num_projects = st.sidebar.selectbox("Quantos projetos deseja incluir?", [1, 2, 3])

project_list = []
for i in range(num_projects):
    st.sidebar.subheader(f"Projeto {i+1}")
    name = st.sidebar.text_input(f"Nome do Projeto {i+1}", f"Projeto {i+1}")
    cost = st.sidebar.number_input(f"Custo Mensal (R$) - Projeto {i+1}", value=0.0, step=1000.0, format="%.2f")
    start_month_proj = st.sidebar.selectbox(f"Mês de Início - Projeto {i+1}", list(range(1, 13)), index=2, key=f"start_month_{i}")
    start_year_proj = st.sidebar.number_input(f"Ano de Início - Projeto {i+1}", value=2025, step=1, key=f"start_year_{i}")
    end_month_proj = st.sidebar.selectbox(f"Mês de Fim - Projeto {i+1}", list(range(1, 13)), index=5, key=f"end_month_{i}")
    end_year_proj = st.sidebar.number_input(f"Ano de Fi_
