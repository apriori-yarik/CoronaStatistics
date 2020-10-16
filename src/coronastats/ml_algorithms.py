import matplotlib.pyplot as plt
import datetime
from datetime import date
import sklearn
from sklearn.linear_model import LinearRegression


def ml_lin_reg_new_cases(data, name, type_of_chart):
	values = data[type_of_chart]
	future = 40
	past = 180
	start = past
	end = len(values) - future
	raw_data = [] # keeping all the information needed to to make the predictions - the previous values and the next which will be used to test our ML model
	for i in range(start, end):
   	    pfv = values[(i - past):(i + future)]
   	    raw_data.append(list(pfv))
    
	past_columns = []
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
	l = range(1, future + 1)

	LinReg = LinearRegression()
	LinReg.fit(X, y)
	prediction = LinReg.predict(X_test)[0]

	type_of_chart_text = type_of_chart.capitalize()
	type_of_chart_text = type_of_chart_text.replace('_', ' ')

	# plotting the prediciton
	plt.clf()
	plt.style.use('dark_background')
	plt.plot_date(l, prediction, linestyle='solid', marker="", label='prediction')
	plt.gcf().autofmt_xdate()
	plt.title(f'{type_of_chart} prediction in {name}')
	plt.xlabel('Day')
	plt.ylabel('Value')
	plt.legend()
	plt.grid(True)
	plt.tight_layout()

	plt.savefig('static/coronastats/new_cases_ml.png')


def ml_lin_reg_new_deaths(data, name, type_of_chart):
	values = data[type_of_chart]
	future = 40
	past = 180
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
	l = range(1, future + 1)

	LinReg = LinearRegression()
	LinReg.fit(X, y)
	prediction = LinReg.predict(X_test)[0]

	type_of_chart_text = type_of_chart.capitalize()
	type_of_chart_text = type_of_chart_text.replace('_', ' ')

	# plotting the prediciton
	plt.clf()
	plt.style.use('dark_background')
	plt.plot_date(l, prediction, linestyle='solid', marker="", label='prediction')
	plt.gcf().autofmt_xdate()
	plt.title(f'{type_of_chart} prediction in {name}')
	plt.xlabel('Day')
	plt.ylabel('Value')
	plt.legend()
	plt.grid(True)
	plt.tight_layout()

	plt.savefig('static/coronastats/new_deaths_ml.png')
