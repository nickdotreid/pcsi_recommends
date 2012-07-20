from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils.datastructures import DotExpandedDict

from django import forms
import itertools

from django.template import RequestContext

from forms import make_question_form
from pchsi_recommends.questions.models import *

from logic import *

from pchsi_recommends.recommendations.views import populations_to_recomendations

def reset_session(request):
	request.session['age'] = False
	request.session['populations'] = []
	request.session['questions_asked'] = []
	request.session['answers'] = {}
	request.session['country'] =False

def base_question_form(request):
	reset_session(request)
	QuestionForm = make_question_form()
	form = QuestionForm()
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			answers = DotExpandedDict(form.cleaned_data)
			request.session['age'] = answers_to_age(answers)
			request.session['populations'] = answers_to_populations(answers)
			return redirect('/recommendations')
	return render_to_response('questions/form.html',{
		'form':form,
		},context_instance=RequestContext(request))

def show_recommendations(request):
	if 'populations' not in request.session or 'age' not in request.session:
		return redirect('/')
	QuestionForm = make_question_form(request.session['populations'],request.session['age'],request.session['questions_asked'])
	form = QuestionForm()
	if len(form.fields)<1:
		form = False
	answers = []
	if 'answers' in request.session:
		FullQuestionForm = make_question_form(request.session['populations'],request.session['age'],[],True)
		full_form = FullQuestionForm(request.session['answers'])
		for key in full_form.fields.keys():
			if not form or key not in form.fields.keys():
				field = full_form[key]
				answers.append({
					'label':field.label,
					'value':field.value(),
				})
	# clear session
	return render_to_response('questions/responses.html',{
		'recommendations':populations_to_recomendations(request.session['populations'],request.session['age'],request.session['country']),
		'form':form,
		'answers':answers,
		'age':request.session['age'],
		},context_instance=RequestContext(request))

def all_questions(request):
	if 'populations' not in request.session or 'age' not in request.session or 'answers' not in request.session:
		return redirect('/')
	QuestionForm = make_question_form(request.session['populations'],request.session['age'],[],True)
	form = QuestionForm(request.session['answers'])
	reset_session(request)
	return render_to_response('questions/responses.html',{
		'recommendations':False,
		'form':form,
		},context_instance=RequestContext(request))

def question_answer(request):
	if request.method == 'POST':
		if 'populations' not in request.session or 'age' not in request.session:
			QuestionForm = make_question_form()
		else:
			QuestionForm = make_question_form(request.session['populations'],request.session['age'],request.session['questions_asked'])
		form = QuestionForm(request.POST)
		if form.is_valid():
			if 'answers' not in request.session:
				request.session['answers'] = request.POST
			else:
				request.session['answers'] = dict( request.session['answers'].items() + request.POST.items() )
			answers = DotExpandedDict(form.cleaned_data)
			request.session['age'] = answers_to_age(answers)
			request.session['country'] = answers_to_country(answers)
			request.session['populations'] = list(set(itertools.chain(request.session['populations'],answers_to_populations(answers))))
			if 'questions' in answers:
				request.session['questions_asked'] = list(set(itertools.chain(request.session['questions_asked'],answers['questions'].keys())))
	return redirect('/recommendations')