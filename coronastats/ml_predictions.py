import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random
import math
import time
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error
import datetime
import operator


confirmed_cases = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
deaths_reported = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
recovered_cases = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
latest_data = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/10-27-2020.csv')

confirmed_cases['Country/Region'].replace({'US': 'United States', "Czechia": "Czech Republic", "Korea, South": "South Korea", "North Macedonia": "Macedonia"}, inplace=True)
deaths_reported['Country/Region'].replace({'US': 'United States', "Czechia": "Czech Republic", "Korea, South": "South Korea", "North Macedonia": "Macedonia"}, inplace=True)
recovered_cases['Country/Region'].replace({'US': 'United States', "Czechia": "Czech Republic", "Korea, South": "South Korea", "North Macedonia": "Macedonia"}, inplace=True)

latest_data['Country_Region'].replace({'US': 'United States', "Czechia": "Czech Republic", "Korea, South": "South Korea", "North Macedonia": "Macedonia"}, inplace=True)
cols = confirmed_cases.keys()

confirmed = confirmed_cases.loc[:, cols[4]:cols[-1]]
deaths = deaths_reported.loc[:, cols[4]:cols[-1]]
recoveries = recovered_cases.loc[:, cols[4]:cols[-1]]

dates = confirmed.keys()


def daily_increase(data):
    d = []
    for i in range(len(data)):
        if i == 0:
            d.append(data[0])
        else:
            d.append(data[i] - data[i-1])
    return d

def new_cases_ml(country_name):
	cases = []
	for i in dates:
		cases.append(confirmed_cases[confirmed_cases['Country/Region']==country_name][i].sum())
	last_cases = cases[len(cases) - 1]
	cases = daily_increase(cases)

	future = 30
	past = 250

	values = cases # keeping all the values form money.curs into a seperate array
	start = past
	end = len(values) - future

	raw_data = [] # keeping all the information needed to to make the predictions - the previous values and the next which will be used to test our ML model
	for i in range(start, end):
		pfv = values[(i - past):(i + future)]
		raw_data.append(list(pfv))

	past_columns = [] # keeping the previous values
	for i in range(past):
		past_columns.append("past_{}".format(i))
	future_columns = [] # keeping the next values
	for i in range(future):
		future_columns.append("future_{}".format(i))

	df = pd.DataFrame(raw_data, columns = (past_columns + future_columns))

	X = df[past_columns][:-1]
	y = df[future_columns][:-1]
	X_test = df[past_columns][-1:]
	y_test = df[future_columns][-1:]


	pred_X_test = df.iloc[:, len(df.columns) - past:]
	LinReg = LinearRegression()
	LinReg.fit(X, y)
	prediction = LinReg.predict(pred_X_test)[0]
	print('preidction: ', prediction)
	for i in range(len(prediction)):
		if prediction[i] < 0:
			prediction[i] = 0

	new_confirmed = 0
	for item in prediction[16:31]:
		new_confirmed += item




	plt.clf()
	plt.style.use('default')
	plt.style.use('dark_background')
	plt.plot(prediction[16:31], label = "Prediction")
	plt.gcf().autofmt_xdate()
	plt.title(f'New cases in {country_name}', size=100)
	plt.xlabel('Day', size=75)
	plt.ylabel('Cases', size=75)
	plt.xticks(size=50)
	plt.yticks(size=50)
	plt.grid(True)
	plt.tight_layout()
	plt.savefig('static/coronastats/prediction_new_cases.png')

	return str(int(last_cases + new_confirmed))

def new_deaths_ml(country_name):
	cases = []
	for i in dates:
		cases.append(deaths_reported[deaths_reported['Country/Region']==country_name][i].sum())
	last_cases = cases[len(cases) - 1]
	cases = daily_increase(cases)

	future = 30
	past = 250

	values = cases # keeping all the values form money.curs into a seperate array
	start = past
	end = len(values) - future

	raw_data = [] # keeping all the information needed to to make the predictions - the previous values and the next which will be used to test our ML model
	for i in range(start, end):
		pfv = values[(i - past):(i + future)]
		raw_data.append(list(pfv))

	past_columns = [] # keeping the previous values
	for i in range(past):
		past_columns.append("past_{}".format(i))
	future_columns = [] # keeping the next values
	for i in range(future):
		future_columns.append("future_{}".format(i))

	df = pd.DataFrame(raw_data, columns = (past_columns + future_columns))

	X = df[past_columns][:-1]
	y = df[future_columns][:-1]
	X_test = df[past_columns][-1:]
	y_test = df[future_columns][-1:]


	pred_X_test = df.iloc[:, len(df.columns) - past:]
	LinReg = LinearRegression()
	LinReg.fit(X, y)
	prediction = LinReg.predict(pred_X_test)[0]
	for i in range(len(prediction)):
		if prediction[i] < 0:
			prediction[i] = 0

	new_confirmed = 0
	for item in prediction[16:31]:
		new_confirmed += item



	plt.clf()
	plt.style.use('default')
	plt.style.use('dark_background')
	plt.plot(prediction[16:31], label = "Prediction")
	plt.gcf().autofmt_xdate()
	plt.title(f'New deaths in {country_name}', size=100)
	plt.xlabel('Day', size=75)
	plt.ylabel('Cases', size=75)
	plt.xticks(size=50)
	plt.yticks(size=50)
	plt.grid(True)
	plt.tight_layout()
	plt.savefig('static/coronastats/prediction_new_deaths.png')

	return str(int(last_cases + new_confirmed))

