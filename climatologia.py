# -*- coding: utf-8 -*-
"""CodNovo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BUfbQgQ4sLrYYXXKfoRg8aSFA4-oUmj8
"""

# Commented out IPython magic to ensure Python compatibility.
# PREPARANDO AS BIBLIOTECAS
import pandas as pd
import seaborn as sns
import numpy as np

import matplotlib.pyplot as plt
# %matplotlib inline

import warnings
warnings.filterwarnings('ignore')

"""# Temperatura média por estação

Vamos ver como a temperatura mudou entre cada estação de 1750 e 2015
"""

global_temp = pd.read_csv('GlobalTemperatures.csv') # Seleciona a tabela excel que será usada

# Apagar colunas desnecessárias
global_temp = global_temp[['dt', 'LandAverageTemperature']]

global_temp['dt'] = pd.to_datetime(global_temp['dt'])
global_temp['year'] = global_temp['dt'].map(lambda x: x.year)
global_temp['month'] = global_temp['dt'].map(lambda x: x.month)

#DEFINIR AS ESTAÇÕES DO ANO
def get_season(month):
    if month >= 3 and month <= 5:
        return 'spring'
    elif month >= 6 and month <= 8:
        return 'summer'
    elif month >= 9 and month <= 11:
        return 'autumn'
    else:
        return 'winter'

min_year = global_temp['year'].min()
max_year = global_temp['year'].max()
years = range(min_year, max_year + 1)

global_temp['season'] = global_temp['month'].apply(get_season)

spring_temps = []
summer_temps = []
autumn_temps = []
winter_temps = []

for year in years:
    curr_years_data = global_temp[global_temp['year'] == year]
    spring_temps.append(curr_years_data[curr_years_data['season'] == 'spring']['LandAverageTemperature'].mean())
    summer_temps.append(curr_years_data[curr_years_data['season'] == 'summer']['LandAverageTemperature'].mean())
    autumn_temps.append(curr_years_data[curr_years_data['season'] == 'autumn']['LandAverageTemperature'].mean())
    winter_temps.append(curr_years_data[curr_years_data['season'] == 'winter']['LandAverageTemperature'].mean())

# FORMA O GRÁFICO
sns.set(style="whitegrid")
sns.set_color_codes("pastel")
f, ax = plt.subplots(figsize=(10, 6))

#DEFINE O NOME DAS LINHAS
plt.plot(years, summer_temps, label='Temperaura média do Verão', color='orange')
plt.plot(years, autumn_temps, label='Temperatura média do Outono', color='r')
plt.plot(years, spring_temps, label='Temperatura média da Primavera', color='g')
plt.plot(years, winter_temps, label='Temperatura média do Inverno', color='b')

plt.xlim(min_year, max_year)

ax.set_ylabel('Temperatura Média')
ax.set_xlabel('Ano')
ax.set_title('Temperatura Média por Estação')
legend = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, borderpad=1, borderaxespad=1)

"""Está aquecendo? Sim, está.

# Países com as maiores diferenças de temperatura

Agora, vamos dar uma olhada nos 15 países que têm as maiores variações de temperatura. A variação de temperatura é a diferença entre a temperatura mais alta e a mais baixa.
"""

temp_by_country = pd.read_csv('GlobalLandTemperaturesByCountry.csv')
countries = temp_by_country['Country'].unique()

max_min_list = []

# Pegar temps min e máx.
for country in countries:
    curr_temps = temp_by_country[temp_by_country['Country'] == country]['AverageTemperature']
    max_min_list.append((curr_temps.max(), curr_temps.min()))

# limpeza de NaN
res_max_min_list = []
res_countries = []

for i in range(len(max_min_list)):
    if not np.isnan(max_min_list[i][0]):
        res_max_min_list.append(max_min_list[i])
        res_countries.append(countries[i])

# calcular diferença
differences = []

for tpl in res_max_min_list:
    differences.append(tpl[0] - tpl[1])

# ordenação
differences, res_countries = (list(x) for x in zip(*sorted(zip(differences, res_countries), key=lambda pair: pair[0], reverse=True)))


f, ax = plt.subplots(figsize=(8, 8)) # Cria uma 'moldura' para o gráfico
sns.barplot(x=differences[:15], y=res_countries[:15], palette=sns.color_palette("coolwarm", 25), ax=ax)

texts = ax.set(ylabel="", xlabel="Diferença de temperatura", title="Países com as maiores diferenças de temperatura")