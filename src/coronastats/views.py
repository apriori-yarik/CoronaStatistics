from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CountryForm, CountryPageForm
from . import plots
from .models import Country


def home_view(request):
	context = {
		'title': 'CoronaStatistics',
	}
	return render(request, 'coronastats/home.html', context)

def stats_by_country_view(request):
	#image_name = ""
	#data = {}
	country = ""
	#form = CountryForm()
	#if request.method == 'POST':
	#	form = CountryForm(request.POST)
	#	if form.is_valid():
	#		image_name = "plots"
	#		country = form.cleaned_data['country']
	#		type_of_chart = form.cleaned_data['choice']
	#		plots.new_cases_by_country(country, type_of_chart)
	#		data = plots.get_info(country)
	#else:
	#	form = CountryForm()

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
		#'form': form,
		'form2': form2,
		#'img_name': image_name,
		#'data': data,
		'country': country
	}
	return render(request, 'coronastats/stats_by_country.html', context)

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

def country_view(request, name):
	context = plots.get_stats_by_country(name)
	print(context)
	return render(request, 'coronastats/country.html', context)

def predictions_forms_view(request):
	country = ""
	form2 = CountryForm()
	if request.method == 'POST':
		form2 = CountryForm(request.POST)
		if form2.is_valid():
			country = form2.cleaned_data['country']
			return redirect('predictions', name = country)
		else:
			form2 = CountryForm()

	context = {
		'title': 'Predictions',
		'form': form2,
		'country': country
	}

	return render(request, 'coronastats/predictions.html', context)

def predictions_view(request, name):
	return HttpResponse(f'<h1>{name}</h1>')



