import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random
import math
import time
import datetime
import operator
plt.style.use('fivethirtyeight')

# Извличане и обработване на данните 
confirmed_cases = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
deaths_reported = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
#recovered_cases = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
latest_data = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/11-23-2020.csv')

confirmed_cases['Country/Region'].replace({'US': 'United States', "Czechia": "Czech Republic", "Korea, South": "South Korea", "North Macedonia": "Macedonia"}, inplace=True)
deaths_reported['Country/Region'].replace({'US': 'United States', "Czechia": "Czech Republic", "Korea, South": "South Korea", "North Macedonia": "Macedonia"}, inplace=True)
#recovered_cases['Country/Region'].replace({'US': 'United States', "Czechia": "Czech Republic", "Korea, South": "South Korea", "North Macedonia": "Macedonia"}, inplace=True)
latest_data['Country_Region'].replace({'US': 'United States', "Czechia": "Czech Republic", "Korea, South": "South Korea", "North Macedonia": "Macedonia"}, inplace=True)

cols = confirmed_cases.keys()

confirmed = confirmed_cases.loc[:, cols[4]:cols[-1]]
deaths = deaths_reported.loc[:, cols[4]:cols[-1]]
#recoveries = recovered_cases.loc[:, cols[4]:cols[-1]]


# Обработване на данни за света
dates = confirmed.keys()
world_cases = []
total_deaths = []
mortality_rate = []
recovery_rate = []
total_recovered = []
total_active = []

for i in dates:
    confirmed_sum = confirmed[i].sum()
    death_sum = deaths[i].sum()
    #recovered_sum = recoveries[i].sum()
    
    world_cases.append(confirmed_sum)
    total_deaths.append(death_sum)
    #total_recovered.append(recovered_sum)
    #total_active.append(confirmed_sum - death_sum-recovered_sum)

# Функция, която служи за пресмятане на разликата в случаите на два последователни дни (покачването на случаите) 
def daily_increase(data):
    d = []
    for i in range(len(data)):
        if i == 0:
            d.append(data[0])
        else:
            d.append(data[i] - data[i-1])
    return d

world_daily_increase = daily_increase(world_cases)
world_daily_death = daily_increase(total_deaths)
#world_daily_recovery = daily_increase(total_recovered)

unique_countries = list(latest_data['Country_Region'].unique())

# Обработване на данни за конкретна държава
country_confirmed_cases = []
country_death_cases = []
country_active_cases = []
country_recovery_cases = []
country_mortality_rate = []

no_cases = []

for i in unique_countries:
    cases = latest_data[latest_data['Country_Region']==i]['Confirmed'].sum()
    if cases > 0:
        country_confirmed_cases.append(cases)
    else:
        no_cases.append(i)
        
for i in no_cases:
    unique_countries.remove(i)
    
unique_countries = [k for k, v in sorted(zip(unique_countries, country_confirmed_cases), key = operator.itemgetter(1), reverse=True)]
for i in range(len(unique_countries)):
    country_confirmed_cases[i] = latest_data[latest_data['Country_Region']==unique_countries[i]]['Confirmed'].sum()
    country_death_cases.append(latest_data[latest_data['Country_Region']==unique_countries[i]]['Deaths'].sum())
    country_recovery_cases.append(latest_data[latest_data['Country_Region']==unique_countries[i]]['Recovered'].sum())
    
    country_active_cases.append(country_confirmed_cases[i] - country_death_cases[i] - country_recovery_cases[i])
    country_mortality_rate.append(country_death_cases[i]/country_confirmed_cases[i])
    

# Обработване на данни за различните области/провинции
unique_provinces = list(latest_data['Province_State'].unique())

province_confirmed_cases = []
province_country = []
province_death_cases = []
province_recovery_cases = []
province_mortality_rate = []

no_cases = []
for i in unique_provinces:
    cases = latest_data[latest_data['Province_State']==i]['Confirmed'].sum()
    if cases > 0:
        province_confirmed_cases.append(cases)
    else:
        no_cases.append(i)
        
for i in no_cases:
    unique_provinces.remove(i)
    
unique_provinces = [k for k, v in sorted(zip(unique_provinces, province_confirmed_cases), key=operator.itemgetter(1), reverse=True)]
for i in range(len(unique_provinces)):
    province_confirmed_cases[i] = latest_data[latest_data['Province_State']==unique_provinces[i]]['Confirmed'].sum()
    province_country.append(latest_data[latest_data['Province_State']==unique_provinces[i]]['Country_Region'].unique()[0])
    province_death_cases.append(latest_data[latest_data['Province_State']==unique_provinces[i]]['Deaths'].sum())
    province_recovery_cases.append(latest_data[latest_data['Province_State']==unique_provinces[i]]['Recovered'].sum())
    province_mortality_rate.append(province_death_cases[i]/province_confirmed_cases[i])


nan_indices = []

for i in range(len(unique_provinces)):
    if type(unique_provinces[i]) == float:
        nan_indices.append(i)
        
unique_provinces = list(unique_provinces)
province_confirmed_cases = list(province_confirmed_cases)

for i in nan_indices:
    unique_provinces.pop(i)
    province_confirmed_cases.pop(i)

# Сравнение на потвърдените случаи в света със случаите в конкретна държава
def confirmed_country_vs_outside(country_name):
	#info = get_stats_by_country(country_name)
	confirmed = latest_data[latest_data['Country_Region']==country_name]['Confirmed'].sum() / info['population']
	outside_confirmed = np.sum(country_confirmed_cases) - confirmed
	plt.style.use('dark_background')
	plt.figure(figsize=(16, 9))
	plt.barh(country_name, confirmed)
	plt.barh(f'Outside {country_name}', outside_confirmed)
	plt.title('Number of Coronavirus Confirmed Cases', size=20)
	plt.xticks(size=29)
	plt.yticks(size=20)
	plt.tight_layout()
	plt.savefig('static/coronastats/confirmed_country_vs_outside.png')

# Сравнение на леталните случаи в света със случаите в конкретна държава
def deaths_country_vs_outside(country_name):
	deaths = latest_data[latest_data['Country_Region']==country_name]['Deaths'].sum()
	outside_deaths = np.sum(country_death_cases) - deaths
	plt.style.use('dark_background')
	plt.figure(figsize=(16, 9))
	plt.barh(country_name, deaths)
	plt.barh(f'Outside {country_name}', outside_deaths)
	plt.title('Number of Coronavirus Deaths', size=20)
	plt.xticks(size=29)
	plt.yticks(size=20)
	plt.tight_layout()
	plt.savefig('static/coronastats/deaths_country_vs_outside.png')

# Построяване на диаграма
def plot_pie_charts(x, y, title):
    c = random.choices(list(mcolors.TABLEAU_COLORS.values()), k=len(unique_countries))
    plt.style.use('dark_background')
    plt.figure(figsize=(40, 30))
    plt.title(title, size=100)
    plt.pie(y, colors=c)
    plt.legend(x, loc='best', fontsize=50)
    plt.tight_layout()
    plt.savefig('static/coronastats/regions.png')

# Построяване на диаграма за регионите
def plot_pie_country_with_regions(country_name, title):
    regions = list(latest_data[latest_data['Country_Region']==country_name]['Province_State'].unique())
    confirmed_cases = []
    no_cases = []
    for i in regions:
        cases = latest_data[latest_data['Province_State']==i]['Confirmed'].sum()
        if cases > 0:
            confirmed_cases.append(cases)
        else:
            no_cases.append(i)
            
    for i in no_cases:
        regions.remove(i)
            
    regions = [k for k, v in sorted(zip(regions, confirmed_cases), key=operator.itemgetter(1), reverse=True)]
        
    for i in range(len(regions)):
        confirmed_cases[i] = latest_data[latest_data['Province_State']==regions[i]]['Confirmed'].sum()
            
            
    if(len(regions)>10):
        regions_10 = regions[:10]
        regions_10.append('Others')
        confirmed_cases_10 = confirmed_cases[:10]
        confirmed_cases_10.append(np.sum(confirmed_cases[10:]))
        plot_pie_charts(regions_10, confirmed_cases_10, title)
    else:
        plot_pie_charts(regions, confirmed_cases, title)

# Проверка дали дадена държава съдържа информация за регионите в нея
def hasRegions(country_name):
    regions = list(latest_data[latest_data['Country_Region']==country_name]['Province_State'].unique())
    print(regions)
    print(len(regions))
    if len(regions) > 1:
        return True
    return False






