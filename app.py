# app.py
import streamlit as st
from services.simulator import simulate_budget
from utils.csv_export import export_to_csv
from utils.charts import plot_budget_line_chart, plot_budget_pie_chart
import pandas as pd

st.set_page_config(page_title="FinOpsPredict Pro", layout="wide")
st.title("💰 FinOpsPredict Pro - Planejamento Orçamentário em Cloud")

# Inicializa session state
if "projetos" not in st.session_state:
    st.session_state["projetos"] = []

if "project_name_input" not in st.session_state:
    st.session_state["project_name_input"] = ""

if "project_cost_input" not in st.session_state:
    st.session_state["project_cost_input"] = 0.0

# Função para resetar os campos
def reset_fields():
    st.session_state["project_name_input"] = ""
    st.session_state["project_cost_input"] = 0.0

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
st.sidebar.text_input("Nome do Projeto", key="project_name_input", placeholder="Ex: Projeto Alpha")
st.sidebar.number_input("Custo Mensal (R$)", min_value=0.0, value=st.session_state["project_cost_input"], step=100.0, format="%.2f", key="project_cost_input")
start_month_proj = st.sidebar.selectbox("Mês de Início - Projeto", list(range(1, 13)), index=0)
start_year_proj = st.sidebar.number_input("Ano de Início - Projeto", value=2025, step=1, key="start_year_proj")
end_month_proj = st.sidebar.selectbox("Mês de Fim - Projeto", list(range(1, 13)), index=5)
end_year_proj = st.sidebar.number_input("Ano de Fim - Projeto", value=2025, step=1, key="end_year_proj")

if st.sidebar.button("➕ Adicionar Projeto"):
    if st.session_state["project_name_input"]:
        st.session_state["projetos"].append({
            "name": st.session_state["project_name_input"],
            "monthly_cost": st.session_state["project_cost_input"],
            "start_month": start_month_proj,
            "start_year": start_year_proj,
            "end_month": end_month_proj,
            "end_year": end_year_proj
        })
        reset_fields()

# Exibição dos projetos adicionados
with st.sidebar.expander("📁 Ver Projetos Adicionados", expanded=False):
    if st.session_state["projetos"]:
        for i, proj in enumerate(st.session_state["projetos"]):
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                valor_formatado = f"R$ {proj['monthly_cost']:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
                st.markdown(f"**{proj['name']}**  \n{valor_formatado} - {proj['start_month']}/{proj['start_year']} até {proj['end_month']}/{proj['end_year']}")
            with col2:
                if st.button("🗑️", key=f"delete_{i}"):
                    st.session_state["projetos"].pop(i)
                    st.experimental_rerun()
    else:
        st.info("Nenhum projeto adicionado.")

# Simulação
if st.sidebar.button("📊 Simular Orçamento"):
    df = simulate_budget(
        baseline_cost=baseline_value,
        monthly_growth_rate=monthly_growth_rate,
        start_month=start_month,
        start_year=start_year,
        duration_months=duration_months,
        projects=st.session_state["projetos"]
    )

    meses_pt = {
        "January": "Janeiro", "February": "Fevereiro", "March": "Março",
        "April": "Abril", "May": "Maio", "June": "Junho",
        "July": "Julho", "August": "Agosto", "September": "Setembro",
        "October": "Outubro", "November": "Novembro", "December": "Dezembro"
    }

    df_exibicao = df.copy()
    df_exibicao["Custo Previsto (R$)"] = df_exibicao["Custo Previsto (R$)"].apply(
        lambda x: f"R$ {x:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    )
    df_exibicao["Mês"] = pd.to_datetime(df_exibicao["Data"], format="%m-%Y").dt.month_name().map(meses_pt)

    st.subheader("📊 Resultado da Simulação")
    st.dataframe(df_exibicao, use_container_width=True)

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
