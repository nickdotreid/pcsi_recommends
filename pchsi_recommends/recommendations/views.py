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
			return render_to_response('forms/population_test_form.html',{
				'form':form,
				'recommendations':populations_to_recomendations(populations)
				},context_instance=RequestContext(request))
	return render_to_response('forms/population_test_form.html',{
		'form':form,
		'recommendations':[]
		},context_instance=RequestContext(request))
	

def populations_to_recomendations(populations):
	recommendations = []
	if len(populations) > 0:
		for screen in Screen.objects.all():
			recommend = get_recommendation_for(screen,populations)
			if recommend:
				recommendations.append(recommend)
	return recommendations

def get_recommendation_for(screen,populations):
	recommend = False
	for recommendation in screen.recommendation_set.all():
		for population in recommendation.populations.all():
			if population in populations:
				if not recommend or recommend.weight > recommendation.weight:
					recommend = recommendation
	return recommend