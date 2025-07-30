import streamlit as st
import pandas as pd
from babel.numbers import format_currency
from datetime import datetime

# Título
st.set_page_config(page_title="FinOps Predict MVP", layout="wide")
st.title("📊 Previsão Orçamentária em Cloud - FinOps Predict")

# --- INPUT DE BASELINE ---
baseline = st.number_input("Baseline em R$", min_value=0.0, step=100.0, format="%.2f")

# Exibe valor formatado
if baseline:
    st.markdown(f"**Valor inserido:** {format_currency(baseline, 'BRL', locale='pt_BR')}")

# --- DADOS DO PROJETO ---
st.header("📝 Dados do Projeto")
col1, col2 = st.columns(2)

with col1:
    projeto = st.text_input("Nome do Projeto")
    responsavel = st.text_input("Responsável")
with col2:
    ambiente = st.selectbox("Ambiente", ["Produção", "Homologação", "Desenvolvimento", "UAT", "Outros"])
    data_inicio = st.date_input("Data de Início")

valor_estimado = st.number_input("Valor Estimado Mensal (R$)", min_value=0.0, step=100.0, format="%.2f")
if valor_estimado:
    st.markdown(f"**Valor inserido:** {format_currency(valor_estimado, 'BRL', locale='pt_BR')}")

# --- PARÂMETROS DE CRESCIMENTO E OTIMIZAÇÃO ---
st.header("📈 Parâmetros de Crescimento e Otimização")
col3, col4 = st.columns(2)

with col3:
    crescimento_mensal = st.slider("Crescimento Mensal (%)", -100, 100, 10)
with col4:
    reducao_otimizacoes = st.slider("Redução por Otimizações (%)", 0, 100, 0)

# --- EXECUTAR SIMULAÇÃO ---
if st.button("Executar Simulação"):
    meses = [i for i in range(12)]
    datas = pd.date_range(start=data_inicio, periods=12, freq='MS')

    valores = []
    valor_mensal = valor_estimado

    for i in range(12):
        crescimento = valor_mensal * (crescimento_mensal / 100)
        reducao = valor_mensal * (reducao_otimizacoes / 100)
        valor_mensal = valor_mensal + crescimento - reducao
        valores.append(valor_mensal)

    df = pd.DataFrame({
        "Mês": [data.strftime("%m-%Y") for data in datas],
        "Valor Estimado (R$)": [format_currency(v, 'BRL', locale='pt_BR') for v in valores]
    })

    st.subheader("📅 Resultado da Simulação")
    st.dataframe(df, use_container_width=True)

    total = sum(valores)
    st.markdown(f"### 💰 Total estimado para 12 meses: {format_currency(total, 'BRL', locale='pt_BR')}")
    st.caption("Desenvolvido com ❤️ seguindo as práticas FinOps.")
