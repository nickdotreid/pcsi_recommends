from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect

from django import forms
from django.template import RequestContext

from pchsi_recommends.recommendations.models import *

def make_population_form():
	populations = []
	for population in Population.objects.all():
		populations.append((population.id,population.name))
	fields = {}
	fields['age'] = forms.IntegerField(
		required = False,
		label = 'Enter Age',
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
			return render_to_response('forms/population_test_form.html',{
				'form':form,
				'recommendations':populations_to_recomendations(populations,age)
				},context_instance=RequestContext(request))
	return render_to_response('forms/population_test_form.html',{
		'form':form,
		'recommendations':[]
		},context_instance=RequestContext(request))
	

def populations_to_recomendations(populations=[], age=False):
	recommendations = []
	for screen in Screen.objects.all():
		recommend = get_recommendation_for(screen,populations,age)
		if recommend:
			recommendations.append(recommend)
	return recommendations

def get_recommendation_for(screen,populations,age=False):
	recommend = False
	recommendations = screen.recommendation_set.all()
	for recommendation in recommendations:
		for population_relationship in recommendation.population_relationship_set.all():
			if population_relationship_matches(population_relationship,populations,age):
				if not recommend or recommend.weight > recommendation.weight:
					recommend = recommendation
	return recommend

def population_relationship_matches(population_relationship,populations,age):
	if age_in_range(age,population_relationship.min_age,population_relationship.max_age):
		if population_relationship.inclusive:
			for population in population_relationship.populations.all():
				if population in populations:
					return True
		else:
			for population in population_relationship.populations.all():
				if population not in populations:
					return False
			return True 
	return False

def age_in_range(age,min,max):
	if not age:
		return False
	if min and max:
		if age >= min and age <= max:
			return True
	if min and age >= min:
		return True
	if max and age <= max:
		return True
	return False