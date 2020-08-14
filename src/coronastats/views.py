from django.shortcuts import render
from .forms import CountryForm
from . import plots

def home_view(request):
	context = {
		'title': 'CoronaStatistics',
	}
	return render(request, 'coronastats/home.html', context)

def stats_by_country_view(request):
	image_name = ""
	data = {}
	country = ""
	form = CountryForm()
	if request.method == 'POST':
		form = CountryForm(request.POST)
		if form.is_valid():
			image_name = "plots"
			country = form.cleaned_data['country']
			type_of_chart = form.cleaned_data['choice']
			plots.new_cases_by_country(country, type_of_chart)
			data = plots.get_info(country)
	else:
		form = CountryForm()
	
	context = {
		'title': 'By Country',
		'form': form,
		'img_name': image_name,
		'data': data,
		'country': country
	}
	return render(request, 'coronastats/stats_by_country.html', context)

def world_view(request):
	total_cases_info = plots.get_15_total_cases()
	new_cases_info = plots.get_15_new_cases()
	deaths_info = plots.get_15_deaths()
	context = {
		'title': 'World - CoronaStatistics',
		'total_cases': total_cases_info,
		'new_cases': new_cases_info,
		'deaths': deaths_info
	}

	return render(request, 'coronastats/world.html', context)

