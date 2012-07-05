from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils.datastructures import DotExpandedDict

from django import forms

from django.template import RequestContext

from forms import make_question_form
from pchsi_recommends.recommendations.models import *
from pchsi_recommends.questions.models import *

from logic import *

from pchsi_recommends.recommendations.views import populations_to_recomendations

def add_population(populations,term):
	pops = Population.objects.filter(name=term)
	if len(pops) > 0 and pops[0] not in populations:
		populations.append(pops[0])
	return populations

def questionnaire_form(request,questionnaire_id):
	questionnaire = get_object_or_404(Questionnaire,pk=questionnaire_id)
	QuestionForm = make_question_form(questionnaire.id)
	form = QuestionForm()
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			answers = DotExpandedDict(form.cleaned_data)
			age = answers_to_age(answers)
			populations = answers_to_populations(answers)
			return render_to_response('questions/responses.html',{
				'questionnaire':questionnaire,
				'age':age,
				'populations':populations,
				})
	return render_to_response('questions/form.html',{
		'form':form,
		'questionnaire':questionnaire,
		},context_instance=RequestContext(request))