from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import CountryForm, CountryPageForm, NNImageForm, CreateUserForm

from . import plots
from .models import Country
from .ml_predictions import new_cases_ml, new_deaths_ml, new_cases_poly
from .man_Hopkins_data import confirmed_country_vs_outside, deaths_country_vs_outside, plot_pie_country_with_regions, hasRegions
from .nn.nn_handler import handler
#from .nn_predictions import new_cases

import os, datetime, random

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from CoronaStatistics.settings import MEDIA_ROOT

def handle_uploaded_file(f):
    name = str(datetime.datetime.now().strftime('%H%M%S')) + str(random.randint(0, 1000)) + str(f)
    path = default_storage.save(str(MEDIA_ROOT) + '/' + name,
                                ContentFile(f.read()))
    return os.path.join(MEDIA_ROOT, path), name



imageToPredict = ""

# Изглед за началната страница

@login_required(login_url='login')
def home_view(request):
	context = {
		'title': 'CoronaStatistics',
	}
	return render(request, 'coronastats/home.html', context)

# Изглед за началната страница от раздела "Данни за всяка една държава" - показване на форма

@login_required(login_url='login')
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

@login_required(login_url='login')
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
@login_required(login_url='login')
def country_view(request, name):
	#confirmed_country_vs_outside(name)
	#deaths_country_vs_outside(name)
	plots.comparison(name)
	plot_pie_country_with_regions(name, f'COVID-19 Confirmed Cases in {name}')
	regions = hasRegions(name)
	context = plots.get_stats_by_country(name)
	context['hasRegions'] = regions
	context['title'] = 'By Country'
	print(context)
	return render(request, 'coronastats/country.html', context)

# Изглед за раздела "Прогнози" - показване на форма
@login_required(login_url='login')
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

# Изглед за раздела "Прогнози"
@login_required(login_url='login')
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


@login_required(login_url='login')
def nn_form_view(request):
	image = ""
	form = NNImageForm()
	if request.method == 'POST':
		form = NNImageForm(request.POST, request.FILES)
		print('Success1')
		if form.is_valid():
			file1_path, file1_name = handle_uploaded_file(request.FILES['image'])
			print(file1_path)
			print(file1_name)
			return redirect('nn-result', file1_name)
		else:
			form = NNImageForm()

	context = {
		'title': 'Image Classifier',
		'form': form,
	}
	return render(request, 'coronastats/nn_forms.html', context)

@login_required(login_url='login')
def nn_view(request, file_name):
	output, normal_prob, pneumonia_prob, covid_prob = handler(file_name)
	result = ""
	if output == 0:
		result = 'Normal'
	elif output == 1:
		result = 'Viral Pneumonia'
	else: 
		result = 'COVID-19'

	context = {
		'result': result,
		'title': 'Image Classifier',
		'file_name': file_name,
		'path': str(MEDIA_ROOT) + '/' + file_name,
		'normal_prob': '{0:.2f}'.format(normal_prob * 100),
		'pneumonia_prob': '{0:.2f}'.format(pneumonia_prob * 100),
		'covid_prob': '{0:.2f}'.format(covid_prob * 100)
	}
	return render(request, 'coronastats/nn_results.html', context);


def loginView(request):
	if request.user.is_authenticated:
		return redirect('home')

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {'title': 'CoronaStatistics'}
	return render(request, 'coronastats/authentication/login.html', context)

def register(request):
	if request.user.is_authenticated:
		return redirect('home')

	form = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, "Account was created successfully for " + user)
			return redirect('login')
	context = {'form': form, 'title': 'CoronaStatistics'}
	return render(request, 'coronastats/authentication/register.html', context)

@login_required(login_url='login')
def logoutUser(request):
	logout(request)
	return redirect('login')