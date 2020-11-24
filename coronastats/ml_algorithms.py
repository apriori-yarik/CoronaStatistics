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
from sklearn.preprocessing import PolynomialFeatures

plt.style.use('fivethirtyeight')


# Извличане и обработване на данни
confirmed_cases = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
deaths_reported = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
recovered_cases = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
latest_data = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/11-23-2020.csv')

cols = confirmed_cases.keys()
confirmed = confirmed_cases.loc[:, cols[4]:cols[-1]]
deaths = deaths_reported.loc[:, cols[4]:cols[-1]]
recoveries = recovered_cases.loc[:, cols[4]:cols[-1]]

dates = confirmed.keys()

days_in_future = 20
future_forecast = np.array([i for i in range(len(dates)+days_in_future)]).reshape(-1, 1)
adjusted_dates = future_forecast[:-20]

def daily_increase(data):
    d = []
    for i in range(len(data)):
        if i == 0:
            d.append(data[0])
        else:
            d.append(data[i] - data[i-1])
    return d

# Функция за построяване на графики
def plot_predictions(x, y, pred, algo_name, color):
    plt.figure(figsize=(16, 9))
    #plt.plot(x, y)
    plt.plot(future_forecast[-20:], pred, linestyle='dashed', color=color)
    plt.title('Number of coronavirus cases over time', size=30)
    #plt.xlabel('Days since 1/22/2020', size=30)
    plt.ylabel('NUmber of Cases', size=30)
    plt.legend(['Confirmed cases', algo_name], prop={'size': 20})
    plt.xticks(size=20)
    plt.yticks(size=20)
    plt.savefig('static/coronastats/prediction_new_cases.png')

# Функция, осъществяваща създаването на прогноза
def new_cases_prediction(country):
	cases = []
	for i in dates:
		cases.append(confirmed_cases[confirmed_cases['Country/Region']==country][i].sum())
	cases = daily_increase(cases)
	days_since_1_22 = np.array([i for i in range(len(dates))]).reshape(-1,1)
	cases = np.array(cases).reshape(-1, 1)

	
	# Подготвяне на тренировъчните и тестовите данни
	X_train_confirmed, X_test_confirmed, y_train_confirmed, y_test_confirmed = train_test_split(days_since_1_22, cases, test_size=0.25, shuffle=False)
	
	# Използване на полиномна регресия
	poly = PolynomialFeatures(degree=3)
	poly_X_train_confirmed = poly.fit_transform(X_train_confirmed)
	poly_X_test_confirmed = poly.fit_transform(X_test_confirmed)
	poly_future_forecast = poly.fit_transform(future_forecast)

	linear_model = LinearRegression(normalize=True, fit_intercept=False)
	linear_model.fit(poly_X_train_confirmed, y_train_confirmed)
	test_linear_pred = linear_model.predict(poly_X_test_confirmed)
	linear_pred = linear_model.predict(poly_future_forecast)

	diff = abs(cases[len(cases) - 1] - linear_pred[len(linear_pred)-1])

	if cases[len(cases) - 1] > linear_pred[len(cases) - 1]:
		for i in range(len(cases), len(cases) + 20):
			linear_pred[i] += diff
	else:
		for i in range(len(cases), len(cases) + 20):
			linear_pred[i] -= diff

	plot_predictions(adjusted_dates[-20:], cases[-20:], linear_pred[-20:], 'Polynomial Regression', 'red')