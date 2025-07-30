import streamlit as st
import pandas as pd
from services.simulator import simulate_budget
from utils.csv_export import export_to_csv
from utils.charts import plot_budget_line_chart, plot_budget_pie_chart

st.set_page_config(page_title="FinOpsPredict Pro", layout="wide")
st.title("💰 FinOpsPredict Pro - Planejamento Orçamentário em Cloud")

# Sidebar - Parâmetros do Forecast
st.sidebar.header("🔧 Parâmetros do Forecast")
baseline_value = st.sidebar.number_input("Baseline em R$", min_value=0.0, format="%.2f")
if baseline_value:
    st.sidebar.markdown(f"Valor inserido: **R$ {baseline_value:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
else:
    st.sidebar.markdown("Valor inserido:")

# Sidebar - Dados do Projeto
st.sidebar.header("📌 Dados do Projeto")
project_name = st.sidebar.text_input("Nome do Projeto", "Projeto X")
monthly_cost = st.sidebar.number_input("Custo Inicial Mensal (R$)", min_value=0.0, value=0.00, format="%.2f")
if monthly_cost:
    st.sidebar.markdown(f"Valor inserido: **R$ {monthly_cost:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
else:
    st.sidebar.markdown("Valor inserido:")

start_month_proj = st.sidebar.selectbox("Mês de Início do Projeto", list(range(1, 13)), index=0)
start_year_proj = st.sidebar.number_input("Ano de Início do Projeto", value=2025, step=1)
end_month_proj = st.sidebar.selectbox("Mês de Fim do Projeto", list(range(1, 13)), index=11)
end_year_proj = st.sidebar.number_input("Ano de Fim do Projeto", value=2025, step=1)

# Parâmetros gerais
growth_rate = st.sidebar.slider("Crescimento ou Redução (%) ao ano", -50, 50, 5)
start_month = 1
start_year = 2025
duration_months = 12

# Preparar lista de projetos
project_list = []
if project_name and start_month_proj and start_year_proj and end_month_proj and end_year_proj:
    project_list.append({
        "name": project_name,
        "monthly_cost": monthly_cost,
        "start_month": start_month_proj,
        "start_year": start_year_proj,
        "end_month": end_month_proj,
        "end_year": end_year_proj
    })

# Simulação
if st.sidebar.button("Simular Orçamento"):
    df = simulate_budget(
        baseline_cost=baseline_value,
        monthly_growth_rate=growth_rate,
        start_month=start_month,
        start_year=start_year,
        duration_months=duration_months,
        projects=project_list
    )

    if df.empty:
        st.warning("⚠️ Nenhum dado foi gerado. Verifique os parâmetros.")
    else:
        st.subheader("📊 Resultado da Simulação")

        df_exibicao = df.copy()
        df_exibicao["Custo Previsto (R$)"] = df_exibicao["Custo Previsto (R$)"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))

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
