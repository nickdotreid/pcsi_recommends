from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils.datastructures import DotExpandedDict

from django import forms

from django.template import RequestContext

from forms import make_question_form
from pchsi_recommends.recommendations.models import *
from pchsi_recommends.questions.models import *

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
			populations = []
			age = False
			answers = DotExpandedDict(form.cleaned_data)
			if 'age' in answers:
				age = answers['age']
			if 'questions' in answers:
				questions = answers['questions']
				for question_id in questions:
					question = Question.objects.filter(id=question_id)[0]
					if question:
						answer_id_list = questions[question_id]
						if type(answer_id_list) != type([]):
							answer_id_list = [answer_id_list]
						for answer_id in answer_id_list:
							answer = question.answer_set.filter(id=answer_id)[0]
							if answer:
								for population in answer.populations.all():
									if population not in populations:
										populations.append(population)
			return render_to_response('recommendations/list.html',{
				'recommendations':populations_to_recomendations(populations,age)
				})
	return render_to_response('questions/form.html',{
		'form':form,
		'questionnaire':questionnaire,
		},context_instance=RequestContext(request))