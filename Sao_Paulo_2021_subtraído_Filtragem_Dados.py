import pandas as pd
import numpy as np

# Carregar, converter e filtrar os dados para o município de São Paulo   
sao_paulo_data = pd.read_csv('dados_covid_sp.csv', delimiter=';', \
                             parse_dates=['datahora']).query("nome_munic == 'São Paulo'")
    
def save_cases(data, year, municipio):
    cases = data[data['datahora'].dt.year == year]['casos'] - 401718
    cases = cases.rolling(window=7).mean().fillna(method='bfill')
    cases = cases[cases != 0]  # Remover zeros
    with open(f'{municipio}_casos_mm7d_{year}_sub.txt', 'w') as file:
        file.write(' '.join(map(str, cases)))    
        
save_cases(sao_paulo_data, 2021, 'sao_paulo')