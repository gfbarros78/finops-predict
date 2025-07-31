import pandas as pd

def simulate_budget(projects):
    if not projects:
        # Retorna DataFrame vazio com colunas esperadas para evitar erros
        return pd.DataFrame(columns=["Projeto", "Mês", "Custo Previsto (R$)"])

    df_simulacao = pd.DataFrame(projects)

    resultado = []

    for _, row in df_simulacao.iterrows():
        nome = row["nome"]
        baseline = float(row["baseline"])
        crescimento = float(row["crescimento"])
        meses = int(row["meses"])
        for mes in range(1, meses + 1):
            custo_previsto = baseline * ((1 + crescimento / 100) ** (mes - 1))
            resultado.append({
                "Projeto": nome,
                "Mês": f"Mês {mes}",
                "Custo Previsto (R$)": round(custo_previsto, 2)
            })

    return pd.DataFrame(resultado)
