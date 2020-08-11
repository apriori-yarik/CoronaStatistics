import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt


url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
data = pd.read_csv(url)

def new_cases_by_country(country):
	filt = (data['location'] == country)
	new_cases = data.loc[filt, ['date', 'new_cases']]
	new_cases.drop(index=new_cases[new_cases['new_cases'] == 0.0].index, inplace=True)
	new_cases.date = pd.to_datetime(new_cases.date)
	new_cases.sort_values('date', inplace=True)
	dates = new_cases['date']
	cases = new_cases['new_cases']

	plt.plot_date(dates, cases, linestyle='solid', marker="")
	plt.gcf().autofmt_xdate()
	plt.tight_layout()
	plt.savefig('static/coronastats/01.png')
	print('yes!')

