from django.shortcuts import render
from . import plots

def home_view(request):
	plots.new_cases_by_country('United States')
	return render(request, 'coronastats/home.html', {})

