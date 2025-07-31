
# services/simulator.py

import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime


def simulate_budget(
    baseline_cost: float,
    monthly_growth_rate: float,
    start_month: int,
    start_year: int,
    duration_months: int,
    projects: list = []
) -> pd.DataFrame:

    start_date = datetime(start_year, start_month, 1)
    data = []
    forecast_cost = baseline_cost

    for i in range(duration_months):
        current_date = start_date + relativedelta(months=i)
        mes = current_date.strftime("%B").capitalize()
        data_mes = current_date.strftime("%m-%Y")

        if i > 0:
            forecast_cost *= (1 + monthly_growth_rate / 100)

        custo_projetos_ativos = 0.0
        projetos_ativos = []

        for proj in projects:
            proj_start = datetime(proj["start_year"], proj["start_month"], 1)
            proj_end = datetime(proj["end_year"], proj["end_month"], 1)

            if proj_start <= current_date <= proj_end:
                custo_projetos_ativos += proj["monthly_cost"]
                projetos_ativos.append(proj["name"])

        total_mes = forecast_cost + custo_projetos_ativos

        data.append({
            "Mês": mes,
            "Data": data_mes,
            "Projetos Ativos": ", ".join(projetos_ativos) if projetos_ativos else "Nenhum",
            "Custo Previsto (R$)": round(total_mes, 2)
        })

    return pd.DataFrame(data)
