# services/simulator.py
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def simulate_budget(project_name, scenario, start_month, start_year, monthly_cost, growth_rate, duration_months):
    data = []
    start_date = datetime(start_year, start_month, 1)
    cost = monthly_cost

    for i in range(duration_months):
        date = start_date + relativedelta(months=i)
        data.append({
            "Projeto": project_name,
            "Ano": date.year,
            "Mes": date.month,  # Número do mês, usado no app.py
            "Custo": round(cost, 2)
        })

        cost *= (1 + growth_rate / 100)

    df = pd.DataFrame(data)
    return df
