from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.core.exceptions import ObjectDoesNotExist

from django import forms
from django.template import RequestContext

from pchsi_recommends.populations.models import *
from pchsi_recommends.recommendations.models import *

def screen_detail(request,screen_id):
	screen = get_object_or_404(Screen,pk=screen_id)
	if request.is_ajax():
		return HttpResponse(
			json.dumps({
				'name':screen.name,
				}),
			'application/json')
	return render_to_response('screens/detail.html',{
		'screen':screen,
		'notes':screen.notes.all(),
		'recommendations':screen.recommendation_set.all(),
		},context_instance=RequestContext(request))

def recommendation_detail(request,recommendation_id):
	recommendation = get_object_or_404(Recommendation,pk=recommendation_id)
	return render_to_response('recommendations/detail.html',{
		'recommendation':recommendation,
		},context_instance=RequestContext(request))

def populations_to_recomendations(populations=[], age=False, country=False):
	recommendations = []
	for screen in Screen.objects.all():
		recommend = get_recommendation_for(screen,populations,age,country)
		if recommend:
			recommendations.append(recommend)
	return recommendations

def get_recommendation_for(screen,populations,age=False,country=False):
	recommend = False
	recommendations = screen.recommendation_set.all()
	for recommendation in recommendations:
		for population_relationship in recommendation.populations.all():
			if population_relationship_matches(population_relationship,populations,age,country):
				if not recommend or recommend.weight > recommendation.weight:
					recommend = recommendation
	return recommend

def population_relationship_matches(population_relationship,populations,age,country):
	if population_relationship.country:
		if not country or country != population_relationship.country.code:
			return False
	if age_in_range(age,population_relationship.min_age,population_relationship.max_age):
		relationship_populations = population_relationship.populations.all()
		if len(relationship_populations)<1:
			return True
		if population_relationship.inclusive:
			for population in relationship_populations:
				if population in populations:
					return True
		else:
			for population in relationship_populations:
				if population not in populations:
					return False
			return True 
	return False

def age_in_range(age=False,min=False,max=False):
	if not min and not max:
		return True
	age = int(age)
	if not age:
		return False
	if min and max:
		if age >= min and age <= max:
			return True
		return False
	if min and age >= min:
		return True
	if max and age <= max:
		return True
	return False