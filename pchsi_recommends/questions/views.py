from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect

from django import forms

from django.template import RequestContext

from forms import PatientForm
from pchsi_recommends.recommendations.models import *
from pchsi_recommends.questions.models import *

def patient_form(request):
	form = PatientForm()
	if request.method == 'POST':
		form = PatientForm(request.POST)
		if form.is_valid():
			answers = form.cleaned_data
			# map answers to populations
			# loop through screens and pull recommendations
			return render_to_response('questions/recommendations.html')
	return render_to_response('questions/form.html',{'form':form},context_instance=RequestContext(request))

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
		recommendations = []
		if len(populations) > 0:
			for screen in Screen.objects.all():
				recommend = False
				for recommendation in screen.recommendation_set.all():
					for population in recommendation.populations.all():
						if population in populations:
							if not recommend or recommend.weight > recommendation.weight:
								recommend = recommendation
				if recommend:
					recommendations.append(recommend)
		return render_to_response('questions/recommendations.html',{'recommendations':recommendations})
	questions = Question.objects.all()
	return render_to_response('questions/dynamic.html',{'questions':questions},context_instance=RequestContext(request))