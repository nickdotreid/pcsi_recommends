from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.datastructures import DotExpandedDict

from django import forms
import itertools

from django.template import RequestContext

from forms import make_question_form
from pchsi_recommends.questions.models import *

from logic import *

from pchsi_recommends.recommendations.views import populations_to_recomendations

def reset_session(request):
	request.session['person_obj'] = default_person_obj()
	request.session['questions_asked'] = []
	request.session['answers'] = {}

def default_person_obj():
	return {
		'populations':[],
		'questions_asked':[],
	}

def base_question_form(request):
	reset_session(request)
	QuestionForm = make_question_form(settings = {
		'form_action':reverse(base_question_form),
	})
	form = QuestionForm()
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			request.session['person_obj'] = question_answer(form,request.POST)
			return redirect('/recommendations')
	return render_to_response('questions/form.html',{
		'form':form,
		},context_instance=RequestContext(request))

def show_recommendations(request):
	person_obj = default_person_obj()
	if 'person_obj' in request.session:
		person_obj = request.session['person_obj']
	QuestionForm = make_question_form(person_obj,{
		'form_action':reverse(show_recommendations),
		'exclude_question_ids':request.session['questions_asked'],
		})
	form = QuestionForm()
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			person_obj = question_answer(form,request.POST,person_obj)
			request.session['person_obj'] = person_obj
	# recreate form so it asks new questions
	QuestionForm = make_question_form(person_obj,{
		'form_action':reverse(show_recommendations),
		'exclude_question_ids':request.session['questions_asked'],
		})
	form = QuestionForm()
	if len(form.fields)<1:
		form = False
	answers = show_answered_questions(person_obj)
	age = False
	if 'age' in person_obj:
		age = person_obj['age']
	gender = False
	populations = False
	if 'populations' in person_obj:
		populations = person_obj['populations']
		gender = determine_gender(person_obj['populations'])
	country = False
	if 'country' in person_obj:
		country = person_obj['country']
	# clear session
	return render_to_response('questions/responses.html',{
		'recommendations':populations_to_recomendations(populations,age,country),
		'form':form,
		'answers':answers,
		'age':age,
		'gender':gender
		},context_instance=RequestContext(request))
		
def show_answered_questions(person_obj=default_person_obj()):
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
		
def determine_gender(populations=[]):
	for population in populations:
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

def question_answer(form,post_data,person_obj=default_person_obj()):
	if 'answers' not in person_obj:
		person_obj['answers'] = post_data
	else:
		person_obj['answers'] = dict( person_obj['answers'].items() + post_data.items() )
	answers = DotExpandedDict(form.cleaned_data)
	person_obj['age'] = answers_to_age(answers)
	person_obj['country'] = answers_to_country(answers)
	person_obj['populations'] = list(set(itertools.chain(person_obj['populations'],answers_to_populations(answers))))
	if 'questions' in answers:
		request.session['questions_asked'] = list(set(itertools.chain(person_obj['questions_asked'],answers['questions'].keys())))
	return person_obj