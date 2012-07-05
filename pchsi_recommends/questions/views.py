from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils.datastructures import DotExpandedDict

from django import forms
import itertools

from django.template import RequestContext

from forms import make_base_question_form, make_additional_question_form
from pchsi_recommends.recommendations.models import *
from pchsi_recommends.questions.models import *

from logic import *

from pchsi_recommends.recommendations.views import populations_to_recomendations

def base_question_form(request):
	request.session['age'] = False
	request.session['populations'] = []
	request.session['questions_asked'] = []
	QuestionForm = make_base_question_form()
	form = QuestionForm()
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			answers = DotExpandedDict(form.cleaned_data)
			request.session['age'] = answers_to_age(answers)
			request.session['populations'] = answers_to_populations(answers)
			return redirect('/questions/more')
	return render_to_response('questions/form.html',{
		'form':form,
		},context_instance=RequestContext(request))

def additional_question_form(request):
	QuestionForm = make_additional_question_form(request.session['populations'],request.session['age'],request.session['questions_asked'])
	form = QuestionForm()
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			answers = DotExpandedDict(form.cleaned_data)
			request.session['age'] = answers_to_age(answers)
			request.session['populations'] = answers_to_populations(answers)
			request.session['questions_asked'] = list(set(itertools.chain(request.session['questions_asked'],answers['questions'].keys())))
			QuestionForm = make_additional_question_form(request.session['populations'],request.session['age'])
			form = QuestionForm(request.POST)
	if len(form.fields)<1:
		return redirect('/recomendations')
	return render_to_response('questions/form-2.html',{
		'form':form,
		},context_instance=RequestContext(request))