from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.core.exceptions import ObjectDoesNotExist

from django import forms
from django.template import RequestContext

from pchsi_recommends.notes.models import notes_for
from pchsi_recommends.populations.models import *
from pchsi_recommends.recommendations.models import *

def screen_detail(request,screen_id,recommendation_id=False):
	screen = get_object_or_404(Screen,pk=screen_id)
	if request.is_ajax():
		return HttpResponse(
			json.dumps({
				'name':screen.name,
				}),
			'application/json')
	recommendations = screen.recommendation_set.all().reverse()
	recommendation = False
	if len(recommendations) > 0:
		recommendation = recommendations[0]
	if recommendation_id:
		recommendation = get_object_or_404(Recommendation,pk=recommendation_id)
	return render_to_response('screens/detail.html',{
		'screens':Screen.objects.all(),
		'screen':screen,
		'notes':notes_for(screen=screen,recommendation=recommendation),
		'recommendation':recommendation,
		'recommendations':recommendations,
		},context_instance=RequestContext(request))

def recommendation_detail(request,recommendation_id):
	recommendation = get_object_or_404(Recommendation,pk=recommendation_id)
	return render_to_response('recommendations/detail.html',{
		'recommendation':recommendation,
		'notes':recommendation.screen.notes.all(),
		},context_instance=RequestContext(request))

def populations_to_recomendations(populations=[], age=False, country=False):
	recommendations = []
	for screen in Screen.objects.all():
		recommend = get_recommendation_for(screen,populations,age,country)
		if recommend:
			recommendations.append(recommend)
	return recommendations

def get_recommendation_for(screen,populations,age=False,country=False):
	return screen.get_recommendation(
		populations=populations,
		age=age,
		country=country
		)
