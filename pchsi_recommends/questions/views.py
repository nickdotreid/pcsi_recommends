from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404, redirect
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

from forms import get_questions_for, make_form_for
from pchsi_recommends.questions.models import *
from pchsi_recommends.recommendations.models import Recommendation
from pchsi_recommends.notes.models import notes_for_screen

from logic import *

from pchsi_recommends.recommendations.views import populations_to_recomendations
	
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
	if len(form.fields) < 1:
		form = False
	return render_to_response('questions/responses.html',{
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
	questions = get_questions_for(answers)
	QuestionForm = make_form_for(questions,{
		"form_action":reverse(answer_questions)
	})
	print request.POST
	form = QuestionForm(request.POST)
	for key,field in form.fields.items():
		valid = False
		if key in request.POST:
			try:
				clean = field.clean(request.POST[key])
				answers[key] = clean
				valid = True
			except ValidationError:
				valid = False
		if not valid:
			answers[key] = False
	request.session['answers'] = answers
	return redirect(reverse(recommendations_page))

def recommendation_detail(request,recommendation_id):
	if 'person_obj' not in request.session:
		return redirect(reverse(initial_page))
	person_obj = request.session['person_obj']
	recommendation = get_object_or_404(Recommendation,pk=recommendation_id)
	return render_to_response('questions/recommendation-detail.html',{
		'recommendations':fake_populations_to_recommendations(person_obj),
		'age':person_obj['age'],
		'gender':determine_gender(person_obj),
		'recommendation':recommendation,
		'notes':notes_for_screen(recommendation.screen,
			age = person_obj['age'],
			country = person_obj['country'],
			populations = person_obj['populations'],
			),
		},context_instance=RequestContext(request))
		
def all_questions(request):
	if 'person_obj' not in request.session:
		return redirect(reverse(initial_page))
	person_obj = request.session['person_obj']
	QuestionForm = make_question_form(person_obj,{
		'include_question_ids':person_obj['question_ids'],
		'primary':True,
		})
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			request.session['person_obj'] = person_obj_from_(form.cleaned_data,person_obj)
			return redirect(reverse(recommendations_page))
	form = QuestionForm(person_obj['answers'])
	return render_to_response('questions/change.html',{
		'recommendations':False,
		'form':form,
		},context_instance=RequestContext(request))
			
def fake_populations_to_recommendations(populations=[], age=False, country=False):
	recommendations = populations_to_recomendations(populations,age,country)
	for rec in recommendations:
		rec.notes = notes_for_screen(rec.screen,populations=populations,age=age,country=country)
	return recommendations	