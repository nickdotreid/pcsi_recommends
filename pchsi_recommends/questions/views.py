from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect

from django import forms

from django.template import RequestContext

from forms import PatientForm
from pchsi_recommends.recommendations.models import *
from pchsi_recommends.questions.models import *

from pchsi_recommends.recommendations.views import populations_to_recomendations

def patient_form(request):
	form = PatientForm()
	if request.method == 'POST':
		form = PatientForm(request.POST)
		if form.is_valid():
			answers = form.cleaned_data
			populations = []
			if answers['gender_at_birth'] == 'male':
				populations = add_population(populations,'male')
			if answers['gender_at_birth'] == 'female':
				populations = add_population(populations,'male')
			
			if answers['gender_current'] == 'transmale' or (answers['gender_at_birth'] == 'female' and answers['gender_current'] == 'male'):
				populations = add_population(populations,'transmale')
			if answers['gender_current'] == 'transfemale' or (answers['gender_at_birth'] == 'male' and answers['gender_current'] == 'female'):
				populations = add_population(populations,'transmale')
			
			if answers['sexual_orientation'] == 'bisexual' and answers['gender_current'] == 'male':
				populations = add_population(populations,'msm')
			if answers['sexual_orientation'] == 'gay':
				populations = add_population(populations,'msm')
				
			for condition in answers['health_conditions']:
				populations = add_population(populations,condition)
			
			# map answers to populations
			print populations
			return render_to_response('questions/recommendations.html',{
				'recommendations':populations_to_recomendations(populations)
				})
	return render_to_response('questions/form.html',{'form':form},context_instance=RequestContext(request))

def add_population(populations,term):
	pops = Population.objects.filter(name=term)
	if len(pops) > 0 and pops[0] not in populations:
		populations.append(pops[0])
	return populations

def dynamic_form(request):
	if request.method == 'POST':
		populations = []
		for key in request.POST:
			if key != 'csrfmiddlewaretoken':
				question = Question.objects.filter(id=key)[0]
				if question:
					answer = question.answer_set.filter(id=request.POST[key])[0]
					if answer:
						for population in answer.populations.all():
							if population not in populations:
								populations.append(population)
		return render_to_response('questions/recommendations.html',{
			'recommendations':populations_to_recomendations(populations)
			})
	questions = Question.objects.all()
	return render_to_response('questions/dynamic.html',{'questions':questions},context_instance=RequestContext(request))