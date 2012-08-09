from django import forms
from highlightselectwidget import HighlightedSelect
from pchsi_recommends.questions.models import *
from django.utils.datastructures import SortedDict

from pchsi_recommends.recommendations.views import population_relationship_matches

from django.core.exceptions import ObjectDoesNotExist

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

def make_question_form(person_obj={},settings={}):
	field_list = []
	if ( 'populations' in person_obj and len(person_obj['populations'])>0 ) or 'age' in person_obj:
		questions = []
		if 'include_question_ids' in settings:
			for qid in settings['include_question_ids']:
				try:
					questions.append(Question.objects.filter(id=qid).get())
				except ObjectDoesNotExist:
					qid = False
		else:
			questions = get_questions_for_(person_obj)
		if 'exclude_question_ids' in settings:
			new_questions = []
			for question in questions:
				if question.id not in settings['exclude_question_ids']:
					new_questions.append(question)
			questions = new_questions
		field_list = questions_to_fields(questions,person_obj)
	if ( 'populations' not in person_obj or 'age' not in person_obj or 'country' not in person_obj ) or 'primary' in settings:
		field_list = primary_questions() + field_list
	return make_question_form_from_fields(field_list,settings)

def primary_questions():
	questions = []
	questions.append(('birth_year',forms.CharField(
		label = 'What year were you born?',
		initial = "",
		required = True,
	)))
	from django_countries.countries import COUNTRIES
	questions.append(('birth_country',forms.ChoiceField(
		widget = HighlightedSelect( highlighted = [
			COUNTRIES[12],
			COUNTRIES[99],
		]),
		label = 'What country were you born in?',
		choices = [("","Select a Country")]+list(COUNTRIES),
		initial = "",
		required = True,
	)))
	questions.append(('birth_sex',forms.ChoiceField(
		widget = forms.RadioSelect,
		label = 'What sex were you assigned at birth?',
		choices = [
			('male','Male'),
			('female','Female'),
		]
	)))
	questions.append(('current_sex',forms.ChoiceField(
		widget = forms.RadioSelect,
		label = 'What sex are you currently?',
		choices = [
			('male','Male'),
			('female','Female'),
			('transmale','Transmale'),
			('transfemale','Transfemale'),
		]
	)))
	questions.append(('sex_partners',forms.MultipleChoiceField(
		widget = forms.CheckboxSelectMultiple,
		label = 'What is the gender of your sex partners?',
		choices = [
			('male','Men'),
			('female','Women'),
			('transmale','Transmen'),
			('transfemale','Transwomen'),
		],
		required = True,
	)))
	return questions

def list_years(amount=10):
	years = [("",'Select a Year')]
	year = 2012 #this should be dynamic
	while len(years)<amount:
		years.append((year,year))
		year = year - 1
	return years
	
def get_questions_for_(person_obj):
	questions = []
	for question in Question.objects.all():
		if relation_matches_population(question.populations,person_obj):
			questions.append(question)
	return questions
	
def questions_to_fields(questions=[],person_obj=False):
	field_list = []
	for question in questions:
		answers = []
		for answer in question.answer_set.all():
			if not person_obj or relation_matches_population(answer.population_relationships,person_obj):
				answers.append((answer.id,answer.text))
		field = forms.ChoiceField(
						widget = forms.RadioSelect,
						label = question.text,
						choices = answers,
					)
		if question.multiple_choice:
			field = forms.MultipleChoiceField(
						widget = forms.CheckboxSelectMultiple,
						label = question.text,
						choices = answers,
						required = False,
					)
		field_list.append(('questions.'+str(question.id),field))
	return field_list

def get_additional_questions(person_obj,exclude_question_ids=[]):
	field_list = []
	for question in Question.objects.all():
		if question.id not in exclude_question_ids and relation_matches_population(question.populations,person_obj):
			answers = []
			for answer in question.answer_set.all():
				if relation_matches_population(answer.population_relationships,person_obj):
					answers.append((answer.id,answer.text))
			field = forms.ChoiceField(
							widget = forms.RadioSelect,
							label = question.text,
							choices = answers,
						)
			if question.multiple_choice:
				field = forms.MultipleChoiceField(
							widget = forms.CheckboxSelectMultiple,
							label = question.text,
							choices = answers,
							required = False,
						)
			field_list.append(('questions.'+str(question.id),field))
	return field_list

def relation_matches_population(relation_query,person_obj):
	if relation_query.count() < 1:
		return True
	populations = []
	if 'populations' in person_obj:
		populations = person_obj['populations']
	age = False
	if 'age' in person_obj:
		age = person_obj['age']
	country = False
	if 'country' in person_obj:
		country = person_obj['country']
	for relationship in relation_query.all():
		if population_relationship_matches(relationship,populations,age,country):
			return True
	return False

def make_question_form_from_fields(field_list,settings):
	QuestionForm = type('QuestionForm',(forms.BaseForm,),{
				'base_fields':SortedDict(field_list),
				})
	class QuestionForm(QuestionForm):
		def __init__(self, *args, **kwargs):
			self.helper = FormHelper()
			self.helper.form_method = 'post'
			if 'form_id' in settings:
				self.helper.form_id = settings['form_id']
			if 'form_class' in settings:
				self.helper.form_class = settings['form_class']
			if 'form_action' in settings:
				self.helper.form_action = settings['form_action']
			if 'form_tag' in settings:
				self.helper.form_tag = settings['form_tag']
			if 'no_submit' not in settings:
				self.helper.add_input(Submit('submit', 'Submit'))
			super(QuestionForm, self).__init__(*args, **kwargs)
	return QuestionForm