from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.core.exceptions import ObjectDoesNotExist

from django import forms
from django.template import RequestContext

from pchsi_recommends.populations.models import *
from pchsi_recommends.recommendations.models import *

from pchsi_recommends.recommendations.views import *

def home_page(request):
	return render_to_response('providers/home.html',{
		'screens':Screen.objects.all(),
		},context_instance=RequestContext(request))

def make_population_form():
	from django_countries.countries import COUNTRIES
	
	populations = []
	for population in Population.objects.all():
		populations.append((population.id,population.name))
	fields = {}
	fields['age'] = forms.IntegerField(
		required = False,
		label = 'Enter Age',
	)
	fields['country'] = forms.ChoiceField(
		required = False,
		label = 'Country of Birth',
		choices = [("","Select a Country")] + list(COUNTRIES),
		initial = "",
	)
	fields['populations'] = forms.MultipleChoiceField(
		required = False,
		label = 'Select Populations',
		widget = forms.CheckboxSelectMultiple,
		choices = populations
		)
	return type('PopulationForm',(forms.BaseForm,),{'base_fields':fields})
	
def population_test_form(request):
	form = make_population_form()()
	if request.method == 'POST':
		form = make_population_form()(request.POST)
		if form.is_valid():
			answers = form.cleaned_data
			populations = []
			for pop_id in answers['populations']:
				population = Population.objects.filter(id = pop_id)[0]
				if population:
					populations.append(population)
			age = False
			if answers['age']:
				age = answers['age']
			country = False
			if answers['country']:
				country = answers['country']
			return render_to_response('forms/population_test_form.html',{
				'form':form,
				'recommendations':populations_to_recomendations(populations,age,country)
				},context_instance=RequestContext(request))
	return render_to_response('forms/population_test_form.html',{
		'form':form,
		'recommendations':[]
		},context_instance=RequestContext(request))