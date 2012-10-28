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

from forms import get_questions_for, make_form_for, make_email_form, get_static_question_object, get_static_questions_choices, remove_unneeded_answers
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
	recommendations = fake_populations_to_recommendations(
			populations=get_populations(answers),
			age = get_age(answers),
			country = get_country(answers))
	recommendation_ids = []
	for rec in recommendations:
		recommendation_ids.append(str(rec.id))
	print_url = reverse(print_recommendations)
	print_url += '?' + 'recommendations=' + ','.join(recommendation_ids)
	email_url = reverse(email_recommendations)
	email_url += '?' + 'recommendations=' + ','.join(recommendation_ids)
	return render_to_response('questions/responses.html',{
		'answers': _answers,
		'recommendations':recommendations,
		'print_url':print_url,
		'email_url':email_url,
		'form':form,
		'age':get_age(answers),
		'gender':get_gender(answers),
		},context_instance=RequestContext(request))

def answer_questions(request,question_id=False):
	if request.method != 'POST':
		return redirect(reverse(recommendations_page))
	fields = []
	if 'field_list' in request.POST:
		fields = request.POST['field_list'].split(',')
	if len(fields) < 1:
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
		if str(key) in fields:
			valid = False
			value = field.widget.value_from_datadict(request.POST,True,str(key))
			if value or (type(value) == list and len(value) < 1):
				try:
					clean = field.clean(value)
					if type(key) == int and type(clean) == list:
						new_clean = []
						for item in clean:
							new_clean.append(int(item))
						clean = new_clean
					if type(value) == list and len(value) < 1:
						clean = [False]
					answers[key] = clean
					valid = True
				except ValidationError:
					valid = False
			if not valid:
				answers[key] = False
	request.session['answers'] = remove_unneeded_answers(answers)
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
	recommendations = fake_populations_to_recommendations(
		populations=populations,
		age = age,
		country = country,
		)
	recommendation_ids = []
	for rec in recommendations:
		recommendation_ids.append(str(rec.id))
	print_url = reverse(print_recommendations)
	print_url += '?' + 'recommendations=' + ','.join(recommendation_ids)
	email_url = reverse(email_recommendations)
	email_url += '?' + 'recommendations=' + ','.join(recommendation_ids)
	return render_to_response('questions/recommendation-detail.html',{
		'recommendations':recommendations,
		'print_url':print_url,
		'email_url':email_url,
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
	# funky that I need to set the answers here too
	field_list = []
	for key,field in questions:
		field_list.append(str(key))
	answers['field_list'] = ','.join(field_list)
	form = QuestionForm(format_answers(answers))
	return render_to_response('questions/change.html',{
		'recommendations':False,
		'form':form,
		},context_instance=RequestContext(request))
		
def get_recommendations_from_(request):
	if 'recommendations' in request.REQUEST:
		rec_ids = request.REQUEST['recommendations'].split(',')
		for id in rec_ids:
			recommendation = get_object_or_None(Recommendation,id=id)
			if recommendation:
				yield recommendation

def print_recommendations(request):
	recommendations = get_recommendations_from_(request)
	return render_to_response('recommendations/print.html',{
		'recommendations':recommendations,
		},context_instance=RequestContext(request))
		
def email_recommendations(request):
	message = False
	emailForm = make_email_form()
	form = emailForm()
	recommendations = get_recommendations_from_(request)
	if request.method == 'POST':
		form = emailForm(request.POST)
		if form.is_valid() and 'email' in form.cleaned_data:
			if send_recommendation_email(form.cleaned_data['email'],recommendations):
				form = emailForm()
				message = "Your email has been sent"
	if 'answers' not in request.session:
		return redirect(reverse(initial_page))
	answers = request.session['answers']
	recommendation_ids = []
	recommendations = fake_populations_to_recommendations(
			populations=get_populations(answers),
			age = get_age(answers),
			country = get_country(answers))
	for rec in recommendations:
		recommendation_ids.append(str(rec.id))
	print_url = reverse(print_recommendations)
	print_url += '?' + 'recommendations=' + ','.join(recommendation_ids)
	email_url = reverse(email_recommendations)
	email_url += '?' + 'recommendations=' + ','.join(recommendation_ids)
	return render_to_response('questions/recommendations-email.html',{
		'recommendations':recommendations,
		'print_url':print_url,
		'email_url':email_url,
		'form':form,
		'message':message,
		},context_instance=RequestContext(request))

def send_recommendation_email(email,recommendations):
	from django.core.mail import send_mail
	subject = "Recommendations from JustAskSF" # lets not hard code this here
	message = render_to_string("recommendations/email.html",{
		"recommendations": recommendations,
		})
	send_mail(subject, message, 'no-reply@justasksf.org', [email], fail_silently=False)
	return True

def format_answers(answers):
	for key in answers:
		answer = answers[key]
		if type(key) == int and type(answer) == list:
			_answer = []
			for item in answer:
				_answer.append(int(item))
			answers[key] = _answer
	return answers
		
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