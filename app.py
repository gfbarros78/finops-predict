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

# Sessão de input de projeto
if "projects" not in st.session_state:
    st.session_state["projects"] = []

# Campos fora do formulário (não submetem ao pressionar Enter)
project_name = st.sidebar.text_input("Nome do Projeto", value="", placeholder="Digite o nome do projeto")
project_cost = st.sidebar.number_input("Custo Mensal (R$)", min_value=0.0, step=100.0, format="%.2f", value=0.0)
if project_cost > 0:
    cost_formatado = f"R$ {project_cost:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    st.sidebar.markdown(f"Valor inserido: **{cost_formatado}**")

# Formulário para os outros campos + botão
with st.sidebar.form(key="add_project_form", clear_on_submit=True):
    start_month_proj = st.selectbox("Mês de Início", list(range(1, 13)), index=2)
    start_year_proj = st.number_input("Ano de Início", value=2025, step=1)
    end_month_proj = st.selectbox("Mês de Fim", list(range(1, 13)), index=5)
    end_year_proj = st.number_input("Ano de Fim", value=2025, step=1)
    submitted = st.form_submit_button("+ Adicionar Projeto")

if submitted and project_name and project_cost > 0:
    st.session_state["projects"].append({
        "name": project_name,
        "monthly_cost": project_cost,
        "start_month": start_month_proj,
        "start_year": start_year_proj,
        "end_month": end_month_proj,
        "end_year": end_year_proj
    })

# Mostrar projetos adicionados
if st.sidebar.checkbox("👁 Ver Projetos Adicionados", value=True):
    st.sidebar.markdown("### Projetos Adicionados")
    for idx, proj in enumerate(st.session_state["projects"]):
        col1, col2 = st.sidebar.columns([0.85, 0.15])
        with col1:
            st.markdown(
                f"**{proj['name']}**\n\n"
                f"💸 {proj['monthly_cost']:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".") + " por mês\n"
                f"🗓️ {proj['start_month']:02d}/{proj['start_year']} até {proj['end_month']:02d}/{proj['end_year']}"
            )
        with col2:
            if st.button("🗑️", key=f"delete_{idx}"):
                st.session_state["projects"].pop(idx)
                st.experimental_rerun()

# Simulação
if st.sidebar.button("Simular Orçamento"):
    df = simulate_budget(
        baseline_cost=baseline_value,
        monthly_growth_rate=monthly_growth_rate,
        start_month=start_month,
        start_year=start_year,
        duration_months=duration_months,
        projects=st.session_state["projects"]
    )

    # Tradução manual dos meses
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
