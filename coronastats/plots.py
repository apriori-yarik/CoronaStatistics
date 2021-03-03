import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import datetime
from datetime import date
from .models import Country
import sklearn
import math


url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
data = pd.read_csv(url)

def comparison(country):
	filt = (data['date']==(date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'))
	country_data = data.loc[filt]
	filt2 = (country_data['location']==country)
	filt3 = (country_data['location']=='World')
	country_data_info = country_data.loc[filt2]
	world_data_info = country_data.loc[filt3]
	to_million_country = country_data_info['total_cases_per_million']
	to_million_world = world_data_info['total_cases_per_million']

	plt.style.use('dark_background')
	plt.figure(figsize=(16, 9))
	plt.barh(country, to_million_country)
	plt.barh(f'Outside {country}', to_million_world)
	plt.title('Number of Coronavirus Confirmed Cases', size=20)
	plt.xticks(size=29)
	plt.yticks(size=20)
	plt.tight_layout()
	plt.savefig('static/coronastats/confirmed_country_vs_outside.png')

	to_million_world = world_data_info['total_deaths_per_million']
	to_million_country = country_data_info['total_deaths_per_million']
	comparison_deaths(to_million_world, to_million_country, country)

def comparison_deaths(to_million_world, to_million_country, country):
	plt.style.use('dark_background')
	plt.figure(figsize=(16, 9))
	plt.barh(country, to_million_country)
	plt.barh(f'Outside {country}', to_million_world)
	plt.title('Number of Coronavirus Confirmed Cases', size=20)
	plt.xticks(size=29)
	plt.yticks(size=20)
	plt.tight_layout()
	plt.savefig('static/coronastats/deaths_country_vs_outside.png')

# Създаване на графика по новите случаи
def new_cases_by_country(country, type_of_chart):
	print(type_of_chart)
	filt = (data['location'] == country)
	new_data = data.loc[filt, ['date', type_of_chart]]
	new_data.drop(index=new_data[new_data[type_of_chart] == 0.0].index, inplace=True)
	new_data.date = pd.to_datetime(new_data.date)
	new_data.sort_values('date', inplace=True)
	dates = new_data['date']
	cases = new_data[type_of_chart]
	type_of_chart = type_of_chart.capitalize()
	type_of_chart = type_of_chart.replace('_', ' ')

	plt.clf()

	plt.style.use('dark_background')

	plt.plot_date(dates, cases, linestyle='solid', marker="")
	plt.gcf().autofmt_xdate()
	plt.title(f'{type_of_chart} in {country}')
	plt.xlabel('Date')
	plt.ylabel('Value')
	plt.grid(True)
	plt.tight_layout()
	plt.savefig('static/coronastats/01.png')
	print('yes!')

# Извличане на информация за дадена държава
def get_info(country):
	filt = (data['location'] == country)
	collected = data.loc[filt, ['date', 'new_cases', 'total_cases', 'total_deaths', 'new_deaths', 'new_tests', 'total_tests']]
	collected.fillna(method='ffill', inplace=True)
	info = collected.tail(1)
	new_cases = info['new_cases'].values[0]
	print(new_cases)
	total_cases = info['total_cases'].values[0]
	new_deaths = info['new_deaths'].values[0]
	total_deaths = info['total_deaths'].values[0]
	new_tests = info['new_tests'].values[0]
	total_tests = info['total_tests'].values[0]
	return {
		'new_cases': new_cases,
		'total_cases': total_cases,
		'new_deaths': new_deaths,
		'total_deaths': total_deaths,
		'new_tests': new_tests,
		'total_tests': total_tests
	}

# Извличане на първите 15 държави по случаи на заразени от коронавирус
def get_15_total_cases():
	# data.fillna(method='ffill', inplace=True)
	filt = (data['date']==(date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'))
	df = data.loc[filt, ['location', 'total_cases']]
	sorted_df = df.sort_values('total_cases', ascending = False)
	countries = sorted_df['location'].head(15).to_list()
	cases = sorted_df['total_cases'].head(15).to_list()
	count = 0
	info = []
	for i in range(len(countries)):
		info.append({'country': countries[count], 'cases': cases[count]})
		count += 1
	print(info)
	return info

# Извличане на първите 15 държави по новозаразени
def get_15_new_cases():
	# data.fillna(method='ffill', inplace=True)
	filt = (data['date']==(date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'))
	df = data.loc[filt, ['location', 'new_cases']]
	sorted_df = df.sort_values('new_cases', ascending = False)
	countries = sorted_df['location'].head(15).to_list()
	cases = sorted_df['new_cases'].head(15).to_list()
	count = 0
	info = []
	for i in range(len(countries)):
		info.append({'country': countries[count], 'cases': cases[count]})
		count += 1
	print(info)
	return info

# Извличане на първите 15 държави по летални случаи
def get_15_deaths():
	filt = (data['date']==(date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'))
	df = data.loc[filt, ['location', 'total_deaths']]
	# df.fillna(method='ffill', inplace=True)
	sorted_df = df.sort_values('total_deaths', ascending = False)
	countries = sorted_df['location'].head(15).to_list()
	deaths = sorted_df['total_deaths'].head(15).to_list()
	count = 0
	info = []
	for i in range(len(countries)):
		info.append({'country': countries[count], 'deaths': deaths[count]})
		count += 1
	print(info)
	return info

def get_start_info():
	filt = (data['date']==(date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'))
	total_cases_data = data.loc[filt, ['location', 'total_cases']]
	new_cases_data = data.loc[filt, ['location', 'new_cases']]
	total_deaths_data = data.loc[filt, ['location', 'total_deaths']]
	total_cases = total_cases_data.iloc[total_cases_data.shape[0] - 2, 1]
	new_cases = new_cases_data.iloc[new_cases_data.shape[0] - 2, 1]
	total_deaths = total_deaths_data.iloc[total_deaths_data.shape[0] - 2, 1]
	return {'total_deaths': total_deaths, 'total_cases': total_cases, 'new_cases': new_cases}

# Създаване на графики за дадена държава и връщането на пълната информация за нея във вид на асоциативен масив
def get_stats_by_country(country_name):
	filt = (data['date']==(date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')) #and (data['location']==country_name))
	country_data = data.loc[filt]
	filt2 = (country_data['location']==country_name)
	country_data = country_data.loc[filt2]
	country = Country.objects.filter(name = country_name).first()
	get_plot_chart_new_cases(country_name)
	get_plot_chart_new_deaths(country_name)
	get_plot_chart_total_cases(country_name)
	get_plot_chart_total_deaths(country_name)

	print(country.name)
	print(country_data['gdp_per_capita'])
	return {	
		'gdp_per_capita': str(round(country_data['gdp_per_capita'].values[0], 2)), 
		'population': str(round(country_data['population'].values[0], 2)), 
		'total_cases': str(round(country_data['total_cases'].values[0], 2)),
		'new_cases': str(round(country_data['new_cases'].values[0], 2)),
		'new_deaths': str(round(country_data['new_deaths'].values[0], 2)),
		'total_deaths': str(round(country_data['total_deaths'].values[0], 2)),
		'total_cases_per_million': str(round(country_data['total_cases_per_million'].values[0], 2)),
		'total_deaths_per_million': str(round(country_data['total_deaths_per_million'].values[0], 2)),
		'total_tests_per_thousand': str(round(country_data['total_tests_per_thousand'].values[0], 2)),
		'total_tests': str(round(country_data['total_tests'].values[0], 2)),
		'new_tests': str(round(country_data['new_tests'].values[0], 2)),
		'median_age': str(round(country_data['median_age'].values[0], 2)),
		'life_expectancy': str(round(country_data['life_expectancy'].values[0], 2)),
		'human_development_index': str(round(country_data['human_development_index'].values[0], 2)),
		'country': country,
		'title': 'CoronaStatistcis - ' + country_name,
	}

# Построяване на графика за новозаразените
def get_plot_chart_new_cases(name):
	type_of_chart = 'new_cases'
	filt = data['location'] == name
	country_data = data.loc[filt, ['date', type_of_chart]]
	country_data.drop(index=country_data[country_data[type_of_chart] == 0.0].index, inplace=True)
	country_data.date = pd.to_datetime(country_data.date)
	country_data.sort_values('date', inplace=True)

	type_of_chart_text = type_of_chart.capitalize()
	type_of_chart_text = type_of_chart_text.replace('_', ' ')

	plt.clf()
	plt.style.use('default')
	plt.style.use('dark_background')
	plt.plot_date(country_data['date'], country_data[type_of_chart], linestyle='solid', marker="")
	plt.gcf().autofmt_xdate()
	plt.title(f'{type_of_chart_text} in {name}', size=100)
	plt.xlabel('Date', size=75)
	plt.ylabel('Value', size=75)
	plt.xticks(size=50)
	plt.yticks(size=50)
	plt.grid(True)
	plt.tight_layout()
	plt.savefig('static/coronastats/new_cases.png')

# Постровяне на графика за всички случаи общо
def get_plot_chart_total_cases(name):
	type_of_chart = 'total_cases'
	filt = data['location'] == name
	country_data = data.loc[filt, ['date', type_of_chart]]
	country_data.drop(index=country_data[country_data[type_of_chart] == 0.0].index, inplace=True)
	country_data.date = pd.to_datetime(country_data.date)
	country_data.sort_values('date', inplace=True)

	type_of_chart_text = type_of_chart.capitalize()
	type_of_chart_text = type_of_chart_text.replace('_', ' ')

	plt.clf()
	plt.style.use('default')
	plt.style.use('dark_background')
	plt.ticklabel_format(style = 'plain')
	plt.plot_date(country_data['date'], country_data[type_of_chart], linestyle='solid', marker="")
	plt.gcf().autofmt_xdate()
	plt.title(f'{type_of_chart_text} in {name}', size=100)
	plt.xlabel('Date', size=75)
	plt.ylabel('Value', size=75)
	plt.xticks(size=50)
	plt.yticks(size=50)
	plt.grid(True)
	plt.tight_layout()
	plt.savefig('static/coronastats/total_cases.png')

# Построяване на графика за леталните случаи
def get_plot_chart_total_deaths(name):
	type_of_chart = 'total_deaths'
	filt = data['location'] == name
	country_data = data.loc[filt, ['date', type_of_chart]]
	country_data.drop(index=country_data[country_data[type_of_chart] == 0.0].index, inplace=True)
	country_data.date = pd.to_datetime(country_data.date)
	country_data.sort_values('date', inplace=True)

	type_of_chart_text = type_of_chart.capitalize()
	type_of_chart_text = type_of_chart_text.replace('_', ' ')


	plt.clf()
	plt.style.use('default')
	plt.style.use('dark_background')
	plt.plot_date(country_data['date'], country_data[type_of_chart], linestyle='solid', marker="")
	plt.gcf().autofmt_xdate()
	plt.title(f'{type_of_chart_text} in {name}', size=100)
	plt.xlabel('Date', size=75)
	plt.ylabel('Value', size=75)
	plt.xticks(size=50)
	plt.yticks(size=50)
	plt.grid(True)
	plt.tight_layout()
	plt.savefig('static/coronastats/total_deaths.png')

# Построяване на графика за новите летални случаи
def get_plot_chart_new_deaths(name):
	type_of_chart = 'new_deaths'
	filt = data['location'] == name
	country_data = data.loc[filt, ['date', type_of_chart]]
	country_data.drop(index=country_data[country_data[type_of_chart] == 0.0].index, inplace=True)
	country_data.date = pd.to_datetime(country_data.date)
	country_data.sort_values('date', inplace=True)

	type_of_chart_text = type_of_chart.capitalize()
	type_of_chart_text = type_of_chart_text.replace('_', ' ')

	plt.clf()
	plt.style.use('default')
	plt.style.use('dark_background')
	plt.plot_date(country_data['date'], country_data[type_of_chart], linestyle='solid', marker="")
	plt.gcf().autofmt_xdate()
	plt.title(f'{type_of_chart_text} in {name}', size=100)
	plt.xlabel('Date', size=75)
	plt.ylabel('Value', size=75)
	plt.xticks(size=50)
	plt.yticks(size=50)
	plt.grid(True)
	plt.tight_layout()
	plt.savefig('static/coronastats/new_deaths.png')

def get_ml_graphs(name):
	country_data = data.loc[data['location']==name]
	ml_lin_reg_new_cases(country_data, name, 'new_cases')
	ml_lin_reg_new_deaths(country_data, name, 'new_deaaths')

	

