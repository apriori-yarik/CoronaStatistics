import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import datetime
from datetime import date


url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
data = pd.read_csv(url)

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

	# if another_country == "" or another_country == None:
	plt.clf()

	plt.style.use('dark_background')

	
		

	plt.plot_date(dates, cases, linestyle='solid', marker="")
	plt.gcf().autofmt_xdate()
	plt.title(f'{type_of_chart} in {country}')
	plt.xlabel('Date')
	plt.ylabel('Number of people')
	plt.grid(True)
	plt.tight_layout()
	plt.savefig('static/coronastats/01.png')
	print('yes!')

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

