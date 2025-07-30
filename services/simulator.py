# services/simulator.py

import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime


def simulate_budget(
    project_name: str,
    scenario: str,
    start_month: int,
    start_year: int,
    baseline_cost: float,
    monthly_growth_rate: float,
    duration_months: int,
    project_cost: float = 0.0,
    project_month: int = None,
    project_year: int = None
) -> pd.DataFrame:
    
    start_date = datetime(start_year, start_month, 1)
    data = []

    for i in range(duration_months):
        current_date = start_date + relativedelta(months=i)
        mes = current_date.strftime("%B").capitalize()
        data_mes = current_date.strftime("%m-%Y")

        # Aplica crescimento ao baseline
        if i == 0:
            forecast_cost = baseline_cost
        else:
            forecast_cost *= (1 + monthly_growth_rate / 100)

        # Verifica se é o mês de entrada do projeto
        if project_month and project_year:
            if current_date.month >= project_month and current_date.year >= project_year:
                forecast_cost += project_cost

        data.append({
            "Mês": mes,
            "Data": data_mes,
            "Cenário": scenario,
            "Projeto": project_name,
            "Custo Previsto (R$)": round(forecast_cost, 2)
        })

    df = pd.DataFrame(data)
    return df
