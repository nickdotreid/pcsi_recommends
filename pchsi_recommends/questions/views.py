from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404, redirect
from annoying.functions import get_object_or_None
from django.http import HttpResponse, HttpResponseBadRequest, Http404, HttpResponseRedirect
from django.utils import simplejson as json
from django.core.urlresolvers import reverse
from django.utils.datastructures import DotExpandedDict

from django.core.exceptions import ObjectDoesNotExist

from django import forms
from django.forms import ValidationError
import itertools

from django.template import RequestContext
from django.template.loader import render_to_string

from forms import get_questions_for, make_form_for, get_static_question_object, get_static_questions_choices
from pchsi_recommends.questions.models import *
from pchsi_recommends.recommendations.models import Recommendation
from pchsi_recommends.notes.models import notes_for_screen

from logic import *

from pchsi_recommends.recommendations.views import populations_to_recomendations

from django.forms.util import ErrorList
	
def initial_page(request):
#	request.session.flush()
	request.session['answers'] = {}
	questions = get_questions_for(answers = request.session['answers'], settings = {
		'primary': True
	})
	QuestionForm = make_form_for(questions = questions, settings = {
		"form_action":reverse(answer_questions)
	})
	form = QuestionForm()
	return render_to_response('questions/form.html',{
		'form':form,
		},context_instance=RequestContext(request))

def recommendations_page(request):
	if 'answers' not in request.session:
		return redirect(reverse(initial_page))
	answers = request.session['answers']
	questions = get_questions_for(answers = answers)
	QuestionForm = make_form_for(questions = questions, settings = {
		"form_action":reverse(answer_questions)
	})
	form = QuestionForm()
	for key,field in form.fields.items():
		if key in answers and not answers[key]:
			pass # this would be a good place to set an error message (this field is required, please give answer)
	_answers = []
	for key,items in answers.items():
		if items:
			answer = get_answered_question_object(key,items)
			_answers.append(answer)
	if len(form.fields) < 1:
		form = False
	return render_to_response('questions/responses.html',{
		'answers': _answers,
		'recommendations':fake_populations_to_recommendations(
			populations=get_populations(answers),
			age = get_age(answers),
			country = get_country(answers)),
		'form':form,
		'age':get_age(answers),
		'gender':get_gender(answers),
		},context_instance=RequestContext(request))

def answer_questions(request,question_id=False):
	if request.method != 'POST':
		return redirect(reverse(recommendations_page))
	if 'answers' not in request.session:
		return redirect(reverse(initial_page))
	answers = request.session['answers']
	questions = get_questions_for(answers, settings={
		'include_answered':True,
	})
	QuestionForm = make_form_for(questions,{
		"form_action":reverse(answer_questions)
	})
	form = QuestionForm(request.POST)
	for key,field in form.fields.items():
		valid = False
		if str(key) in request.POST:
			try:
				value = field.widget.value_from_datadict(request.POST,True,str(key))
				clean = field.clean(value)
				answers[key] = clean
				valid = True
			except ValidationError:
				valid = False
		if not valid and key not in answers:
			answers[key] = False
	request.session['answers'] = answers
	return redirect(reverse(recommendations_page))

def recommendation_detail(request,recommendation_id):
	recommendation = get_object_or_404(Recommendation,pk=recommendation_id)
	answers = {}
	if 'answers' in request.session:
		answers = request.session['answers']
	populations = get_populations(answers)
	age = get_age(answers)
	country = get_country(answers)
	# should bounce if recomendation is not for user??
	return render_to_response('questions/recommendation-detail.html',{
		'recommendations':fake_populations_to_recommendations(
			populations=populations,
			age = age,
			country = country,
			),
		'age':age,
		'gender':get_gender(answers),
		'recommendation':recommendation,
		'notes':notes_for_screen(recommendation.screen,
			age = age,
			country = country,
			populations = populations,
			),
		},context_instance=RequestContext(request))
		
def all_questions(request):
	answers = {}
	if 'answers' in request.session:
		answers = request.session['answers']
	questions = get_questions_for(answers = answers, settings = {
		'include_answered': True
	})
	QuestionForm = make_form_for(questions = questions, settings = {
		"form_action":reverse(answer_questions)
	})
	form = QuestionForm(answers)
	return render_to_response('questions/change.html',{
		'recommendations':False,
		'form':form,
		},context_instance=RequestContext(request))
		
def get_answered_question_object(key,answers):
	question = None
	from_model = False
	if type(key) == int:
		question = get_object_or_None(Question, id=key)
		from_model = True
	if type(key) == str:
		question = get_static_question_object(key)
	if not question:
		return False
	if type(answers) != list:
		answers = [answers]
	if from_model:
		_answers = []
		for answer_id in answers:
			answer = get_object_or_None(Answer, id=answer_id)
			if answer:
				_answers.append(answer.text)
		answers = _answers
	else:
		choices = get_static_questions_choices(key)
		_answers = []
		for answer_short in answers:
			found = False
			for short, name in choices:
				if short == answer_short:
					_answers.append(name)
					found = True
			if not found:
				_answers.append(answer_short)
		answers = _answers
	return {
		'text':question.text,
		'values':answers,
	}
			
def fake_populations_to_recommendations(populations=[], age=False, country=False):
	recommendations = populations_to_recomendations(populations,age,country)
	for rec in recommendations:
		rec.notes = notes_for_screen(rec.screen,populations=populations,age=age,country=country)
	return recommendations	