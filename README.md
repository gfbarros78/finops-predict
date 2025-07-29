# README.md

# 💰 FinOpsPredict Pro

Simulador inteligente de orçamento e previsão de gastos em cloud baseado em boas práticas FinOps. Ideal para empresas que desejam prever custos, planejar cenários e acompanhar a evolução dos investimentos em nuvem de forma prática e visual.

---

## 🎯 Funcionalidades

- 📁 Cadastro de projetos com nome, data, tipo e custo inicial
- 📊 Simulação de cenários: crescimento vegetativo, novos projetos e otimização de custos
- 📈 Visualização interativa com gráficos de linha e pizza (Plotly)
- 📤 Exportação de dados para CSV
- 📆 Previsão para 3 a 60 meses com crescimento ou redução mensal

---

## 🚀 Como Executar Localmente

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/finops-predict.git
cd finops-predict
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute a aplicação:

```bash
streamlit run app.py
```

---

## 🌐 Deploy Online

Acesse a versão online (caso publicada):

👉 [Abrir FinOpsPredict Pro no Streamlit](https://seu-usuario-finops-predict.streamlit.app)

---

## 📁 Estrutura do Projeto

```
finops_predict/
├── app.py                  # Interface principal em Streamlit
├── services/
│   └── simulator.py        # Lógica da simulação
├── utils/
│   ├── csv_export.py       # Exportação para CSV
│   └── charts.py           # Gráficos com Plotly
├── requirements.txt        # Lista de dependências
```

---

## 🙋‍♂️ Desenvolvedor

Desenvolvido por **Gustavo Barros**  
Especialista em Infraestrutura FinOps na Midway (Grupo Guararapes/Riachuelo)  
🔗 [LinkedIn](https://www.linkedin.com/in/gfbarros)  
📧 contato: [insira seu e-mail profissional aqui]

---

## 💡 Contribuições

Sugestões, melhorias ou bugs? Fique à vontade para abrir uma _issue_ ou pull request.

---