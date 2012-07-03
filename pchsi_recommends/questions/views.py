from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils.datastructures import DotExpandedDict

from django.core.exceptions import ObjectDoesNotExist

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
	
def get_population_sex_dict():
	sex_dict = {}
	try:
		sex_dict['male'] = Population.objects.get(short__iexact='male')
	except ObjectDoesNotExist:
		sex_dict['male'] = False
	try:
		sex_dict['female'] = Population.objects.get(short__iexact='female')
	except ObjectDoesNotExist:
		sex_dict['female'] = False
	try:
		sex_dict['transmale'] = Population.objects.get(short__iexact='transmale')
	except ObjectDoesNotExist:
		sex_dict['transmale'] = False
	try:
		sex_dict['transfemale'] = Population.objects.get(short__iexact='transfemale')
	except ObjectDoesNotExist:
		sex_dict['transfemale'] = False
	return sex_dict

def determine_sex(current_sex,birth_sex=False):
	if current_sex and not birth_sex:
		pop = Population.objects.get(short__iexact = current_sex)
		if pop:
			return pop
	sex_dict = get_population_sex_dict()
	if birth_sex == 'male' and current_sex == 'male' and sex_dict['male']:
		return sex_dict['male']
	if birth_sex == 'female' and current_sex == 'female' and sex_dict['female']:
		return sex_dict['female']
	if sex_dict['transfemale'] and (current_sex == 'transfemale' or (current_sex == 'female' and birth_sex == 'male')):
		return sex_dict['transfemale']
	if sex_dict['transmale'] and (current_sex == 'transmale' or (current_sex == 'male' and birth_sex == 'female')):
		return sex_dict['transmale']
	return False

def determine_sexual_orientation(sex,sex_partners={}):
	sex_dict = get_population_sex_dict()
	if sex in [sex_dict['male'],sex_dict['transfemale'],sex_dict['transmale']] and ('male' in sex_partners or 'transmale' in sex_partners or 'transfemale' in sex_partners):
		try:
			pop = Population.objects.get(short__iexact='msm')
			if pop:
				return pop
		except ObjectDoesNotExist:
			return False
	return False

def questionnaire_form(request,questionnaire_id):
	questionnaire = get_object_or_404(Questionnaire,pk=questionnaire_id)
	QuestionForm = make_question_form(questionnaire.id)
	form = QuestionForm()
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			populations = []
			age = False
			sex = False
			answers = DotExpandedDict(form.cleaned_data)
			if 'age' in answers:
				age = answers['age']
			if 'birth_sex' in answers and 'current_sex' in answers:
				sex = determine_sex(answers['current_sex'],answers['birth_sex'])
				if sex:
					populations.append(sex)
			elif 'current_sex' in answers:
				sex = determine_sex(answers['current_sex'])
				if sex:
					populations.append(sex)
			if sex and 'sex_partners' in answers:
				pop = determine_sexual_orientation(sex,answers['sex_partners'])
				if pop:
					populations.append(pop)
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
			return render_to_response('questions/responses.html',{
				'questionnaire':questionnaire,
				'age':age,
				'populations':populations,
				'recommendations':populations_to_recomendations(populations,age),
				})
	return render_to_response('questions/form.html',{
		'form':form,
		'questionnaire':questionnaire,
		},context_instance=RequestContext(request))