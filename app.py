# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime
from babel.numbers import format_currency, parse_decimal
from babel import Locale

# Função para formatar valores em reais (padrão brasileiro)
def formatar_valor(valor):
    try:
        return format_currency(valor, 'BRL', locale='pt_BR')
    except:
        return valor

st.set_page_config(page_title="FinOpsPredict", layout="wide")
st.title("📊 FinOpsPredict - Previsão Orçamentária em Cloud")
st.markdown("---")

# Sidebar para inputs
st.sidebar.header("🔧 Parâmetros do Forecast")
baseline_input = st.sidebar.text_input("Baseline em R$", value="")
try:
    baseline = float(parse_decimal(baseline_input, locale=Locale.parse("pt_BR"))) if baseline_input else 0.0
except:
    baseline = 0.0
    st.sidebar.error("Insira um valor válido no formato brasileiro. Ex: 5.000.000,00")

if baseline_input:
    st.sidebar.markdown(f"Valor inserido: **{formatar_valor(baseline)}**")

periodo = st.sidebar.selectbox("Período de Projeção (em anos)", [1, 3], index=0)

st.sidebar.subheader("📈 Cenários de Crescimento Vegetativo Anual")
crescimento_conservador = st.sidebar.slider("Cenário Conservador (%)", 0, 30, 3)
crescimento_moderado = st.sidebar.slider("Cenário Moderado (%)", 0, 30, 6)
crescimento_agressivo = st.sidebar.slider("Cenário Agressivo (%)", 0, 30, 10)

st.sidebar.markdown("---")
st.sidebar.subheader("📁 Novos Projetos")
num_projetos = st.sidebar.number_input("Quantos projetos novos serão adicionados?", 0, 12, 0, 1)

projetos = []
anos = list(range(datetime.now().year, datetime.now().year + periodo))
meses_nome = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

for i in range(num_projetos):
    with st.sidebar.expander(f"Projeto {i+1}"):
        nome = st.text_input(f"Nome do Projeto {i+1}", key=f"nome_{i}")
        ano_inicio = st.selectbox(f"Ano de Início", anos, key=f"ano_inicio_{i}")
        mes_inicio = st.selectbox(f"Mês de Início", meses_nome, key=f"mes_inicio_{i}")
        ano_fim = st.selectbox(f"Ano de Término", anos, index=len(anos)-1, key=f"ano_fim_{i}")
        mes_fim = st.selectbox(f"Mês de Término", meses_nome, index=11, key=f"mes_fim_{i}")
        valor_input = st.text_input(f"Valor Estimado Mensal (R$)", value="", key=f"valor_input_{i}")
        try:
            valor = float(parse_decimal(valor_input, locale=Locale.parse("pt_BR"))) if valor_input else 0.0
        except:
            valor = 0.0
            st.sidebar.error("Insira um valor válido no formato brasileiro.")

        if valor_input:
            st.markdown(f"Valor inserido: **{formatar_valor(valor)}**")

        projetos.append({"nome": nome, "ano_inicio": ano_inicio, "mes_inicio": mes_inicio, "ano_fim": ano_fim, "mes_fim": mes_fim, "valor": valor})

st.markdown(f"## 📈 Resultado da Previsão para os próximos {periodo} ano(s)")

cenarios = {
    "Conservador": crescimento_conservador,
    "Moderado": crescimento_moderado,
    "Agressivo": crescimento_agressivo
}

# Geração dos meses com ano
meses_completos = []
anos_meses = []
for ano in anos:
    for mes in meses_nome:
        meses_completos.append(mes)
        anos_meses.append({"mes": mes, "ano": ano})

df = pd.DataFrame({"Mês": meses_completos, "Ano": [m["ano"] for m in anos_meses]})

projetos_coluna = []
for nome_cenario, crescimento in cenarios.items():
    valores_formatados = []
    valores_numericos = []
    atual = baseline
    for idx, mes_data in enumerate(anos_meses):
        atual *= (1 + crescimento / 100 / 12)
        total_mes = atual
        projetos_mes = []

        for projeto in projetos:
            dentro_intervalo = (
                (projeto["ano_inicio"] < mes_data["ano"] or
                 (projeto["ano_inicio"] == mes_data["ano"] and meses_nome.index(projeto["mes_inicio"]) <= meses_nome.index(mes_data["mes"]))) and
                (projeto["ano_fim"] > mes_data["ano"] or
                 (projeto["ano_fim"] == mes_data["ano"] and meses_nome.index(projeto["mes_fim"]) >= meses_nome.index(mes_data["mes"])))
            )
            if dentro_intervalo:
                total_mes += projeto["valor"]
                projetos_mes.append(projeto["nome"])

        valor_final = round(total_mes, 2)
        valores_numericos.append(valor_final)
        valores_formatados.append(formatar_valor(valor_final))

        if nome_cenario == "Conservador":
            projetos_coluna.append(", ".join(projetos_mes) if projetos_mes else "-")

    df[nome_cenario] = valores_formatados
    df[nome_cenario + "_raw"] = valores_numericos

df["Projetos"] = projetos_coluna

# Tabela formatada
st.dataframe(df[["Mês", "Ano", "Projetos", *cenarios.keys()]], use_container_width=True)

# Gráfico com matplotlib
fig, ax = plt.subplots(figsize=(14, 6))
cores = {"Conservador": "#1f77b4", "Moderado": "#2ca02c", "Agressivo": "#d62728"}
x_labels = df["Mês"] + "/" + df["Ano"].astype(str)

for nome_cenario in cenarios:
    y_values = df[nome_cenario + "_raw"]
    ax.plot(x_labels, y_values, label=nome_cenario, color=cores[nome_cenario], marker='o')
    for x, y in zip(x_labels, y_values):
        ax.text(x, y, f"{y:,.0f}".replace(",", "v").replace(".", ",").replace("v", "."), fontsize=8, ha='center', va='bottom')

ax.set_title("Previsão Mensal de Gastos em Cloud", fontsize=14)
ax.set_ylabel("R$ (milhares)")
ax.grid(True, linestyle='--', alpha=0.4)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"R$ {x:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")))
plt.xticks(rotation=45)
ax.legend()

st.pyplot(fig)

st.markdown("---")
st.caption("Desenvolvido com ❤️ seguindo as práticas FinOps.")
