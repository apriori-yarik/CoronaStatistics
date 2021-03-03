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

import torch

import os
from tqdm import tqdm
import seaborn as sns
from pylab import rcParams
from matplotlib import rc
from sklearn.preprocessing import MinMaxScaler
from pandas.plotting import register_matplotlib_converters
from torch import nn, optim

# Извличане и обработване на данните

#deaths_reported = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
#recovered_cases = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
#latest_data = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/11-23-2020.csv')

#df['Country/Region'].replace({'US': 'United States', "Czechia": "Czech Republic", "Korea, South": "South Korea", "North Macedonia": "Macedonia"}, inplace=True)
#deaths_reported['Country/Region'].replace({'US': 'United States', "Czechia": "Czech Republic", "Korea, South": "South Korea", "North Macedonia": "Macedonia"}, inplace=True)
#recovered_cases['Country/Region'].replace({'US': 'United States', "Czechia": "Czech Republic", "Korea, South": "South Korea", "North Macedonia": "Macedonia"}, inplace=True)


RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)

seq_length = 5

def create_sequences(data, seq_length):
    xs = []
    ys = []

    for i in range(len(data)-seq_length-1):
        x = data[i:(i+seq_length)]
        y = data[i+seq_length]
        xs.append(x)
        ys.append(y)

    return np.array(xs), np.array(ys)

def train_model(
  model, 
  train_data, 
  train_labels, 
  test_data=None, 
  test_labels=None
):
	loss_fn = torch.nn.MSELoss(reduction='sum')

	optimiser = torch.optim.Adam(model.parameters(), lr=1e-3)
	num_epochs = 1

	train_hist = np.zeros(num_epochs)
	test_hist = np.zeros(num_epochs)

	X_train, y_train = create_sequences(train_data, 5)
	#X_test, y_test = create_sequences(test_data, seq_length)

	X_train = torch.from_numpy(X_train).float()
	y_train = torch.from_numpy(y_train).float()

	for t in range(num_epochs):
		model.reset_hidden_state()

		y_pred = model(X_train)

		loss = loss_fn(y_pred.float(), y_train)

		if test_data is not None:
			with torch.no_grad():
				y_test_pred = model(X_test)
				test_loss = loss_fn(y_test_pred.float(), y_test)
			test_hist[t] = test_loss.item()

	if t % 2 == 0:  
		print(f'Epoch {t} train loss: {loss.item()} test loss: {test_loss.item()}')
	elif t % 2 == 0:
		print(f'Epoch {t} train loss: {loss.item()}')

	train_hist[t] = loss.item()
    
	optimiser.zero_grad()

	loss.backward()

	optimiser.step()
  
	return model.eval(), train_hist, test_hist

def new_cases(country_name):
	df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
	df['Country/Region'].replace({'US': 'United States', "Czechia": "Czech Republic", "Korea, South": "South Korea", "North Macedonia": "Macedonia"}, inplace=True)
	df = df[df['Country/Region']==country_name]
	df = df.iloc[:, 4:]
	daily_cases = df.sum(axis=0)
	daily_cases.index = pd.to_datetime(daily_cases.index)

	daily_cases = daily_cases.diff().fillna(daily_cases[0]).astype(np.int64)



	class CoronaVirusPredictor(nn.Module):

		def __init__(self, n_features, n_hidden, seq_len, n_layers=2):
			super(CoronaVirusPredictor, self).__init__()

			self.n_hidden = n_hidden
			self.seq_len = seq_len
			self.n_layers = n_layers

			self.lstm = nn.LSTM(
				input_size=n_features,
				hidden_size=n_hidden,
				num_layers=n_layers,
				dropout=0.5
			)

			self.linear = nn.Linear(in_features=n_hidden, out_features=1)

		def reset_hidden_state(self):
			self.hidden = (
				torch.zeros(self.n_layers, self.seq_len, self.n_hidden),
				torch.zeros(self.n_layers, self.seq_len, self.n_hidden)
			)

		def forward(self, sequences):
			lstm_out, self.hidden = self.lstm(
				sequences.view(len(sequences), self.seq_len, -1),
				self.hidden
			)
			last_time_step = \
				lstm_out.view(self.seq_len, len(sequences), self.n_hidden)[-1]
			y_pred = self.linear(last_time_step)
			return y_pred

	

	scaler = MinMaxScaler()

	scaler = scaler.fit(np.expand_dims(daily_cases, axis=1))

	all_data = scaler.transform(np.expand_dims(daily_cases, axis=1))


	X_all, y_all = create_sequences(all_data, 5)

	X_all = torch.from_numpy(X_all).float()
	y_all = torch.from_numpy(y_all).float()

	model = CoronaVirusPredictor(
		n_features=1, 
		n_hidden=512, 
		seq_len=seq_length, 
		n_layers=2
	)
	model, train_hist, _ = train_model(model, X_all, y_all)

	DAYS_TO_PREDICT = 14

	with torch.no_grad():
		test_seq = X_all[:1]
		preds = []
		for _ in range(DAYS_TO_PREDICT):
			y_test_pred = model(test_seq)
			pred = torch.flatten(y_test_pred).item()
			preds.append(pred)
			new_seq = test_seq.numpy().flatten()
			new_seq = np.append(new_seq, [pred])
			new_seq = new_seq[1:]
			test_seq = torch.as_tensor(new_seq).view(1, seq_length, 1).float()

	predicted_cases = scaler.inverse_transform(
		np.expand_dims(preds, axis=0)
	).flatten()

	coeff = daily_cases[len(daily_cases) - 1] - predicted_cases[0]
	for i in range(len(predicted_cases)):
		predicted_cases[i] += coeff



	plt.clf()
	plt.style.use('default')
	plt.style.use('dark_background')
	plt.plot(predicted_cases, label = "Prediction")
	plt.gcf().autofmt_xdate()
	plt.title(f'New deaths in {country_name}', size=100)
	plt.xlabel('Day', size=75)
	plt.ylabel('Cases', size=75)
	plt.xticks(size=50)
	plt.yticks(size=50)
	plt.grid(True)
	plt.tight_layout()
	plt.savefig('static/coronastats/prediction_new_cases.png')
