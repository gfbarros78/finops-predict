# app.py
import streamlit as st
from services.simulator import simulate_budget
from utils.csv_export import export_to_csv
from utils.charts import plot_budget_line_chart, plot_budget_pie_chart
import pandas as pd
import locale
import calendar

# Define local para português brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

st.set_page_config(page_title="FinOpsPredict Pro", layout="wide")
st.title("Ὃ0 FinOpsPredict Pro - Planejamento Orçamentário em Cloud")

# Sidebar - Entrada de dados
st.sidebar.header("📌 Dados do Projeto")
project_name = st.sidebar.text_input("Nome do Projeto", "Projeto X")
scenario = st.sidebar.selectbox("Cenário", ["Crescimento Vegetativo", "Novo Projeto", "Otimização de Custos"])
start_month = st.sidebar.selectbox("Mês de Início", list(range(1, 13)), index=0)
start_year = st.sidebar.number_input("Ano de Início", value=2025, step=1)
monthly_cost = st.sidebar.number_input("Custo Inicial Mensal (R$)", value=10000.0, step=1000.0)

# Novo campo: Baseline em R$
baseline_value = st.sidebar.number_input("Baseline em R$", value=50000.0, step=1000.0)
st.sidebar.caption(f"Valor inserido: R$ {baseline_value:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))

growth_rate = st.sidebar.slider("Crescimento ou Redução (%) ao mês", -50, 50, 5)
duration_months = st.sidebar.slider("Duração (meses)", 3, 60, 12)

# Simulação
if st.sidebar.button("Simular Orçamento"):
    df = simulate_budget(
        project_name,
        scenario,
        start_month,
        start_year,
        monthly_cost,
        growth_rate,
        duration_months
    )

    # Ajusta colunas do DataFrame
    df['Mês'] = df['Mes'].apply(lambda x: calendar.month_name[x].capitalize())
    df['Data'] = df['Mes'].astype(str).str.zfill(2) + '-' + df['Ano'].astype(str)
    df['Custo Previsto (R$)'] = df['Custo'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))

    # Reorganiza colunas
    colunas_desejadas = ['Mês', 'Data', 'Ano', 'Mes', 'Custo Previsto (R$)', 'Projeto']
    colunas_existentes = [col for col in colunas_desejadas if col in df.columns]
    df = df[colunas_existentes]

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
