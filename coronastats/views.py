from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from .forms import CountryForm, CountryPageForm #CreateUserForm
from . import plots
from .models import Country
from .ml_predictions import new_cases_ml, new_deaths_ml
from .man_Hopkins_data import confirmed_country_vs_outside, deaths_country_vs_outside, plot_pie_country_with_regions, hasRegions

# Изглед за началната страница
def home_view(request):
	context = {
		'title': 'CoronaStatistics',
	}
	return render(request, 'coronastats/home.html', context)

# Изглед за началната страница от раздела "Данни за всяка една държава" - показване на форма
def stats_by_country_view(request):
	country = ""

	form2 = CountryPageForm()
	if request.method == 'POST':
		form2 = CountryPageForm(request.POST)
		if form2.is_valid():
			country = form2.cleaned_data['country']
			return redirect('country', name = country)
		else:
			form2 = CountryPageForm()
	
	context = {
		'title': 'By Country',
		'form2': form2,
		'country': country
	}
	return render(request, 'coronastats/stats_by_country.html', context)

# Изглед за раздела "Данни за света"
def world_view(request):
	total_cases_info = plots.get_15_total_cases()
	new_cases_info = plots.get_15_new_cases()
	deaths_info = plots.get_15_deaths()
	world_info = plots.get_start_info()
	context = {
		'title': 'World - CoronaStatistics',
		'total_cases': total_cases_info,
		'new_cases': new_cases_info,
		'deaths': deaths_info,
		'world_info': world_info
	}

	return render(request, 'coronastats/world.html', context)

# Изгледа за раздела "Данни за всяка една държава"
def country_view(request, name):
	confirmed_country_vs_outside(name)
	deaths_country_vs_outside(name)
	plot_pie_country_with_regions(name, f'COVID-19 Confirmed Cases in {name}')
	regions = hasRegions(name)
	context = plots.get_stats_by_country(name)
	context['hasRegions'] = regions
	context['title'] = 'By Country'
	print(context)
	return render(request, 'coronastats/country.html', context)

# Изглед за раздела "Прогнози" - показване на форма
def predictions_forms_view(request):
	country = ""
	form2 = CountryPageForm()
	if request.method == 'POST':
		form2 = CountryPageForm(request.POST)
		if form2.is_valid():
			country = form2.cleaned_data['country']
			return redirect('predictions', name = country)
		else:
			form2 = CountryPageForm()

	context = {
		'title': 'Predictions',
		'form': form2,
		'country': country
	}

	return render(request, 'coronastats/predictions.html', context)

# Изглед за раздела "Прогнози" -
def predictions_view(request, name):
	expected_confirmed = new_cases_ml(name)
	expected_deaths = new_deaths_ml(name)
	context = {
		'title': 'Predictions',
		'name': name,
		'expected_confirmed': expected_confirmed,
		'expected_deaths': expected_deaths
	}
	return render(request, 'coronastats/predictions-plots.html', context)



#def login_view(request):
#	context = {}
#	return render(request, 'coronastats/login.html', context)
#
#def register_view(request):
#	form = CreateUserForm()
#
#	if request.method == 'POST':
#		form = CreateUserForm(request.POST)
#		if form.is_valid:
#			form.save()
#	context = {'form': form}
#	return render(request, 'coronastats/register.html', context)


