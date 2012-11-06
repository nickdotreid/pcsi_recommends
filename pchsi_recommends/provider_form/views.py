from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from annoying.functions import get_object_or_None
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
	for catagory in PopulationCatagory.objects.all():
		populations = []
		if catagory.population_set.count() > 0:
			for population in catagory.population_set.all():
				populations.append((population.id,population.name))
			fields[catagory.short] = forms.MultipleChoiceField(
				required = False,
				label = 'Select ' + catagory.name,
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
			for catagory in PopulationCatagory.objects.all():
				if answers[catagory.short]:
					for pop_id in answers[catagory.short]:
						population = get_object_or_None(Population,pk=pop_id)
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