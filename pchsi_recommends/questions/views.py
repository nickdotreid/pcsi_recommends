from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.datastructures import DotExpandedDict

from django.core.exceptions import ObjectDoesNotExist

from django import forms
import itertools

from django.template import RequestContext

from forms import make_question_form
from pchsi_recommends.questions.models import *

from logic import *

from pchsi_recommends.recommendations.views import populations_to_recomendations
	
def initial_page(request):
	request.session.flush()
	QuestionForm = make_question_form()
	form = QuestionForm()
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			request.session['person_obj'] = question_answer(DotExpandedDict(form.cleaned_data))
			settings = form_settings_from_(DotExpandedDict(request.POST))
			return redirect(reverse(recommendations_page))
	return render_to_response('questions/form.html',{
		'form':form,
		},context_instance=RequestContext(request))

def recommendations_page(request):
	person_obj = False
	if 'person_obj' in request.session:
		person_obj = request.session['person_obj']
	elif request.method == 'POST':
		person_obj = person_obj_from_(DotExpandedDict(request.POST))
	if not person_obj:
		return redirect(reverse(initial_page))
	QuestionForm = make_question_form(
		person_obj = person_obj,
		settings = {},
	)
	form = QuestionForm()
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			request.session['person_obj'] = question_answer(DotExpandedDict(form.cleaned_data))
			settings = {}
			return redirect(reverse(recommendations_page))
	request.session.flush()	
	return render_to_response('questions/responses.html',{
		'recommendations':fake_populations_to_recommendations(person_obj),
		'form':form,
		'age':person_obj['age'],
		'gender':determine_gender(person_obj),
		},context_instance=RequestContext(request))
			
def fake_populations_to_recommendations(person_obj):
	populations = []
	if 'populations' in person_obj:
		populations = person_obj['populations']
	age = False
	if 'age' in person_obj:
		age = person_obj['age']
	country = False
	if 'country' in person_obj:
		country = person_obj['country']
	return populations_to_recomendations(populations,age,country)	
		
def show_answered_questions(person_obj):
	return []
	answers = []
	if 'answers' in request.session:
		FullQuestionForm = make_question_form({
			'populations':request.session['populations'],
			'age':request.session['age'],
			},{
			'all':True,
			})
		full_form = FullQuestionForm(request.session['answers'])
		for key in full_form.fields.keys():
			if not form or key not in form.fields.keys():
				field = full_form[key]
				answers.append({
					'label':field.label,
					'value':field.value(),
				})
		
def determine_gender(person_obj):
	if 'populations' in person_obj:
		for population in person_obj['populations']:
			if population.short in ['male','female','transfemale','transmale']:
				return population.name
	return False

def all_questions(request):
	if 'populations' not in request.session or 'age' not in request.session or 'answers' not in request.session:
		return redirect('/')
	QuestionForm = make_question_form({
		'populations':request.session['populations'],
		'age':request.session['age']
		},{
		'all':True
		})
	form = QuestionForm(request.session['answers'])
	reset_session(request)
	return render_to_response('questions/responses.html',{
		'recommendations':False,
		'form':form,
		},context_instance=RequestContext(request))
		
def person_obj_from_(post_data):
	person_obj = {}
	if 'age' in post_data:
		# check age is number
		person_obj['age'] = post_data['age']
	if 'populations' in post_data:
		person_obj['populations'] = get_if_population_from_(post_data['populations'])
	if 'country' in post_data:
		# check country so that it is in list
		person_obj['country'] = post_data['country']
	return person_obj

def form_settings_from_(post_data):
	return {}

def question_answer(answers):
	person_obj = {}
	person_obj['age'] = answers_to_age(answers)
	person_obj['country'] = answers_to_country(answers)
	person_obj['populations'] = answers_to_populations(answers)
	return person_obj
	
	
"""
if 'answers' not in person_obj:
	person_obj['answers'] = post_data
else:
	person_obj['answers'] = dict( person_obj['answers'].items() + post_data.items() )

if 'questions' in answers:
	person_obj['questions_asked'] = list(set(itertools.chain(person_obj['questions_asked'],answers['questions'].keys())))

"""