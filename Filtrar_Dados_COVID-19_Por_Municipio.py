import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# Carregar, converter e filtrar os dados para o município de Bauru
bauru_data = pd.read_csv('dados_covid_sp.csv', delimiter=';', \
                         parse_dates=['datahora']).query("nome_munic == 'Bauru'")
# Carregar, converter e filtrar os dados para o município de São Paulo   
sao_paulo_data = pd.read_csv('dados_covid_sp.csv', delimiter=';', \
                             parse_dates=['datahora']).query("nome_munic == 'São Paulo'")

# Função para salvar os números de casos e óbitos em um arquivo
def save_cases_and_deaths(data, year, municipio):
    cases = data[data['datahora'].dt.year == year]['casos'].rolling(window=7).mean().fillna(method='bfill')
    cases = cases[cases != 0]  # Remover zeros
    with open(f'{municipio}_casos_mm7d_{year}.txt', 'w') as file:
        file.write(' '.join(map(str, cases)))
    deaths = data[data['datahora'].dt.year == year]['obitos'].rolling(window=7).mean().fillna(method='bfill')
    deaths = deaths[deaths != 0]  # Remover zeros
    with open(f'{municipio}_obitos_mm7d_{year}.txt', 'w') as file:
        file.write(' '.join(map(str, deaths)))

# Salvar os dados para cada ano
for year in range(2020, 2023):
    save_cases_and_deaths(bauru_data, year, 'Bauru')
    save_cases_and_deaths(sao_paulo_data, year, 'sao_paulo')




# Função para plotar os dados
def plot_cases_and_deaths(year, tipo, municipio):
    data = np.loadtxt(f'{municipio}_{tipo}_mm7d_{year}.txt')
    if municipio == "sao_paulo" :
        municipio = "São Paulo"
    plt.figure()
    plt.plot(data)
    plt.xlabel(f'Dias de {year}')
    plt.ylabel(f'Número de {tipo.capitalize()} Confirmados')
    plt.title(f'Média Móvel de 7 Dias - {tipo.capitalize()} em {municipio} ({year})')

# Plotar os dados
for year in range(2020, 2023):
    plot_cases_and_deaths(year, 'casos', 'bauru')
    plot_cases_and_deaths(year, 'obitos', 'bauru')
    plot_cases_and_deaths(year, 'casos', 'sao_paulo')
    plot_cases_and_deaths(year, 'obitos', 'sao_paulo')