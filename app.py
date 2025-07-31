# app.py
import streamlit as st
import pandas as pd
from services.simulator import simulate_budget
from utils.csv_export import export_to_csv
from utils.charts import plot_budget_line_chart, plot_budget_pie_chart

st.set_page_config(page_title="FinOpsPredict Pro", layout="wide")
st.title("💰 FinOpsPredict Pro - Planejamento Orçamentário em Cloud")

# Inicializa o estado da sessão
if "projetos" not in st.session_state:
    st.session_state.projetos = []

# Função para remover projeto
def remover_projeto(index):
    if 0 <= index < len(st.session_state.projetos):
        st.session_state.projetos.pop(index)

# Formulário para adicionar projeto
with st.form("form_projeto"):
    st.subheader("➕ Adicionar Novo Projeto")

    nome = st.text_input("Nome do Projeto")
    ambiente = st.selectbox("Ambiente", ["Produção", "Homologação", "Desenvolvimento", "UAT", "Outros"])
    responsavel = st.text_input("Responsável")
    baseline = st.number_input("Baseline em R$", min_value=0.0, step=100.0, format="%.2f")
    crescimento_percentual = st.slider("Crescimento Mensal Estimado (%)", 0, 100, 10)
    novo_projeto = st.checkbox("Projeto Novo?")
    valor_estimado = st.number_input("Valor Estimado Mensal (R$)", min_value=0.0, step=100.0, format="%.2f")

    st.caption(f"💡 Valor inserido: R$ {valor_estimado:,.2f}")

    submitted = st.form_submit_button("Adicionar Projeto")
    if submitted:
        novo = {
            "Projeto": nome,
            "Ambiente": ambiente,
            "Responsável": responsavel,
            "Baseline (R$)": baseline,
            "Crescimento (%)": crescimento_percentual,
            "Projeto Novo?": "Sim" if novo_projeto else "Não",
            "Valor Estimado Mensal (R$)": valor_estimado
        }
        st.session_state.projetos.append(novo)
        st.success(f"Projeto '{nome}' adicionado com sucesso!")

# Exibe os projetos adicionados
if st.session_state.projetos:
    st.subheader("📋 Projetos Adicionados")
    for idx, projeto in enumerate(st.session_state.projetos):
        col1, col2 = st.columns([10, 1])
        with col1:
            st.markdown(f"**{projeto['Projeto']}** | Ambiente: {projeto['Ambiente']} | "
                        f"Responsável: {projeto['Responsável']} | "
                        f"Baseline: R$ {projeto['Baseline (R$)']:,.2f} | "
                        f"Crescimento: {projeto['Crescimento (%)']}% | "
                        f"Novo: {projeto['Projeto Novo?']} | "
                        f"Valor Estimado: R$ {projeto['Valor Estimado Mensal (R$)']:,.2f}")
        with col2:
            if st.button("🗑️", key=f"delete_{idx}"):
                remover_projeto(idx)
                st.experimental_rerun()

# Simulação de orçamento
st.subheader("🧮 Simulação Orçamentária")
if st.button("Simular Orçamento"):
    if st.session_state.projetos:
        df = pd.DataFrame(st.session_state.projetos)

        # Verifica se as colunas esperadas estão presentes
        if "Projeto" in df.columns and "Valor Estimado Mensal (R$)" in df.columns:
            df_simulado = simulate_budget(df)
            st.subheader("📊 Gráficos do Orçamento Simulado")
            st.plotly_chart(plot_budget_line_chart(df_simulado), use_container_width=True)
            st.plotly_chart(plot_budget_pie_chart(df_simulado), use_container_width=True)

            csv = export_to_csv(df_simulado)
            st.download_button("📥 Baixar CSV", data=csv, file_name="orcamento_simulado.csv", mime="text/csv")
        else:
            st.warning("❌ As colunas necessárias não foram encontradas nos dados.")
    else:
        st.warning("⚠️ Nenhum projeto foi adicionado para simulação.")
