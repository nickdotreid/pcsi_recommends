from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest, Http404, HttpResponseRedirect
from django.utils import simplejson as json
from django.core.urlresolvers import reverse
from django.utils.datastructures import DotExpandedDict

from django.core.exceptions import ObjectDoesNotExist

from django import forms
import itertools

from django.template import RequestContext
from django.template.loader import render_to_string

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
			request.session['person_obj'] = person_obj_from_(form.cleaned_data)
			return redirect(reverse(recommendations_page))
	return render_to_response('questions/form.html',{
		'form':form,
		},context_instance=RequestContext(request))

def recommendations_page(request):
	if request.is_ajax():
		return ajax_answer_questions(request)
	if 'person_obj' not in request.session:
		return redirect(reverse(initial_page))
	person_obj = request.session['person_obj']
	QuestionForm = make_question_form(person_obj,{
		'exclude_question_ids':person_obj['question_ids'],
		'form_class':'questions ajax',
	})
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			request.session['person_obj'] = person_obj_from_(form.cleaned_data,person_obj)
			return redirect(reverse(recommendations_page))
	form = QuestionForm()
	if len(form.fields) < 1:
		form = False
	return render_to_response('questions/responses.html',{
		'recommendations':fake_populations_to_recommendations(person_obj),
		'form':form,
		'age':person_obj['age'],
		'gender':determine_gender(person_obj),
		'answers':show_answered_questions(person_obj),
		},context_instance=RequestContext(request))
		
def all_questions(request):
	if 'person_obj' not in request.session:
		return redirect('/')
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
	return render_to_response('questions/responses.html',{
		'recommendations':False,
		'form':form,
		},context_instance=RequestContext(request))
		
def ajax_answer_questions(request):
	if 'person_obj' not in request.session:
		return HttpResponseBadRequest(json.dumps({"message":"No Session"}),
		                mimetype="application/json")
	person_obj = request.session['person_obj']
	post_data = DotExpandedDict(request.POST)
	if 'questions' not in post_data:
		return HttpResponseBadRequest(json.dumps({"message":"No Questions"}),
		                mimetype="application/json")
	QuestionForm = make_question_form(person_obj,{
		'include_question_ids':list(map(int,post_data['questions'].keys())),
	})
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			answers = []
			for question,answer in form.cleaned_data.items():
				answers.append(answer)
			message = ""
			for answer in answers_for_form(form):
				message = render_to_string("questions/answered.html",{
					"answer":answer,
					})
			return HttpResponse(json.dumps({
				"answers":answers,
				"message":message,
				}),
			                mimetype="application/json")
	return HttpResponseBadRequest(json.dumps("answered"),
	                mimetype="application/json")

def ajax_update_answer(request):
	if 'person_obj' not in request.session or request.method != 'POST':
		return HttpResponseBadRequest(json.dumps({"message":"Bad Input"}),
		                mimetype="application/json")
	person_obj = request.session['person_obj']
	post_data = DotExpandedDict(request.POST)
	QuestionForm = make_question_form(person_obj,{
		'include_question_ids':list(map(int,post_data['questions'].keys())),
	})
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			request.session['person_obj'] = person_obj_from_(form.cleaned_data,person_obj)
			return HttpResponse(json.dumps({"message":"Saved"}),
				mimetype="application/json")
	return HttpResponseBadRequest(json.dumps({"message":"Fail"}),
	                mimetype="application/json")
	

def ajax_more_questions(request):
	if 'person_obj' not in request.session:
		return HttpResponseBadRequest(json.dumps({"message":"No Session"}),
		                mimetype="application/json")
	person_obj = request.session['person_obj']
	QuestionForm = make_question_form(person_obj,{
		'exclude_question_ids':person_obj['question_ids'],
		'form_class':'questions ajax',
		'form_tag':False,
	})
	form = QuestionForm()
	if len(form.fields) < 1:
		return HttpResponseBadRequest(json.dumps({"message":"No Questions"}),
		                mimetype="application/json")
	return HttpResponse(json.dumps({
		"questions":render_to_string("questions/form_solo.html",{
			"form":form,
			}),
		}),
	    mimetype="application/json")

def ajax_update_recommendations(request):
	return HttpResponse(json.dumps("answered"),
	                mimetype="application/json")
			
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
	if 'answers' in person_obj:
		FullQuestionForm = make_question_form(person_obj,{
			'primary':True,
			'include_question_ids':person_obj['question_ids'],
			})
		return answers_for_form(FullQuestionForm(person_obj['answers']))
	return []

def answers_for_form(form):
	answers = []
	for key in form.fields.keys():
		field = form[key]
		ans = []
		values = field.value()
		if not isinstance(values,list):
			values = [values]
		for value in values:
			for val,text in field.field.choices:
				if str(val) == str(value):
					if isinstance(text,str) or isinstance(text,unicode):
						ans.append(text)
					elif isinstance(text,int):
						ans.append(str(text))
					else:
						ans.append(value)
		if ans>1:
			ans = ",".join(ans)
		answers.append({
			'label':field.label,
			'value':ans,
		})
	return answers
		
def determine_gender(person_obj):
	if 'populations' in person_obj:
		for population in person_obj['populations']:
			if population.short in ['male','female','transfemale','transmale']:
				return population.name
	return False

def person_obj_from_(org_answers,person_obj = False):
	answers = DotExpandedDict(org_answers)
	if not person_obj:
		#set defaults
		person_obj = {}
		person_obj['age'] = False
		person_obj['country'] = False
		person_obj['populations'] = []
		person_obj['answers'] = {}
		person_obj['question_ids'] = []
	person_obj['answers'] = dict( person_obj['answers'].items() + org_answers.items() )
	age = answers_to_age(answers)
	if age:
		person_obj['age'] = age
	country = answers_to_country(answers)
	if country:
		person_obj['country'] = country
	for population in answers_to_populations(answers):
		if population not in person_obj['populations']:
			person_obj['populations'].append(population)
	if 'questions' in answers:
		for qid in answers['questions'].keys():
			qid = int(qid)
			if qid not in person_obj['question_ids']:
				person_obj['question_ids'].append(qid)
	return person_obj
