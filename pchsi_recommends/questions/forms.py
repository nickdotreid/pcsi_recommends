from django import forms
from django.contrib.localflavor.us.forms import USPhoneNumberField
from highlightselectwidget import HighlightedSelect
from pchsi_recommends.questions.models import *
from django.utils.datastructures import SortedDict

from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from logic import *

def sort_answers(answers):
	def cmp_answer_keys(a,b):
		if (type(b['key']) == str and type(a['key']) == str) or (type(a['key']) == int and type(b['key']==int)):
			if a['order'] < b['order']:
				return -1
			elif a['order'] > b['order']:
				return 1
		if type(a['key']) == str:
			return -1
		if type(b['key']) == str:
			return 1
		return 0
	return sorted(answers,cmp_answer_keys)

def get_questions_for(answers={},settings={}):
	questions = []
	if 'birth_year' not in answers or not answers['birth_year'] or 'include_answered' in settings:
		questions.append(('birth_year',get_question_field('birth_year')))
	if 'birth_country' not in answers or not answers['birth_country'] or 'include_answered' in settings:
		questions.append(('birth_country',get_question_field('birth_country')))
	if 'birth_sex' not in answers or not answers['birth_sex'] or 'include_answered' in settings:
		questions.append(('birth_sex',get_question_field('birth_sex')))
	if 'current_sex' not in answers or not answers['current_sex'] or 'include_answered' in settings:
		questions.append(('current_sex',get_question_field('current_sex')))
	if 'sex_partners' not in answers or not answers['sex_partners'] or 'include_answered' in settings:
		questions.append(('sex_partners',get_question_field('sex_partners')))
	
	if 'primary' in settings:
		return questions
	
	populations = get_populations(answers)
	age = get_age(answers)
	country = get_country(answers)
	
	for question in get_questions_for_(
		populations = populations,
		age = age,
		country = country,
		):
		if question.id not in answers or not answers[question.id] or 'include_answered' in settings:
			questions.append((question.id,question_to_field(question,
				populations=populations, 
				age=age, 
				country=country)))
	return questions
	
def get_questions_for_(populations=[], age=False, country=False):
	questions = []
	for question in Question.objects.all():
		if relation_matches_population(question.populations,
			populations = populations,
			age = age,
			country = country
			):
			questions.append(question)
	return questions
	
def remove_unneeded_answers(answers):
	to_remove = []

	populations = get_populations(answers)
	age = get_age(answers)
	country = get_country(answers)

	for key in answers:
		question = False
		try:
			question_id = int(key)
			question = get_object_or_None(Question,id=question_id)
		except ValueError:
			pass
		if question:
			if not relation_matches_population(question.populations,
				populations = populations,
				age = age,
				country = country
				):
				to_remove.append(key)
	for key in to_remove:
		del answers[key]
	return answers

	
def get_objects_where_matches(objects=[],match_values=[]):
	to_return = []
	for value in match_values:
		for obj in objects:
			if obj[0] == value:
				to_return.append(obj)
	return to_return
	
def list_years(amount=10):
	years = [("",'Select a Year')]
	from datetime import datetime
	year = datetime.now().timetuple().tm_year
	while len(years)<amount:
		years.append((year,year))
		year = year - 1
	return years

def get_static_question_object(key=""):
	static_answer_order = ['birth_year','birth_country','birth_sex','current_sex','sex_partners']
	if key == 'birth_year':
		return Question(
			text = 'What year were you born?',
			order = static_answer_order.index(key) + 1
		)
	if key == 'birth_country':
		return Question(
			text = 'What country were you born in?',
			order = static_answer_order.index(key) + 1
		)
	if key == 'birth_sex':
		return Question(
			text = 'What sex were you assigned at birth?',
			order = static_answer_order.index(key) + 1
		)
	if key == 'current_sex':
		return Question(
			text = 'What sex are you currently?',
			order = static_answer_order.index(key) + 1
		)
	if key == 'sex_partners':
		return Question(
			text = 'What is the gender of your sex partners?',
			description = 'Select all applicapable answers',
			order = static_answer_order.index(key) + 1
		)
	return False

def get_static_questions_choices(key=""):
	if key == 'birth_country':
		from django_countries.countries import COUNTRIES
		return [("","Select a Country")]+list(COUNTRIES)
	if key == 'birth_sex':
		return [
			('male','Male'),
			('female','Female'),
		]
	if key == 'current_sex':
		return [
			('male','Male'),
			('female','Female'),
			('transmale','Trans Male'),
			('transfemale','Trans Female'),
		]
	if key == 'sex_partners':
		return [
			('male','Men'),
			('female','Women'),
			('transmale','Trans Men'),
			('transfemale','Trans Women'),
		]
	return []

def get_static_questions_errors(key=""):
	if key == 'birth_year':
		return "How old you are determines many risk factors"
	if key == 'birth_country':
		return "Knowing country of birth helps us determine what you might have been exposed to or vaccinated against"
	if key == 'birth_sex':
		return "We need to know your sex at birth"
	if key == 'current_sex':
		return "We need to know if your sex has changed"
	if key == 'sex_partners':
		return "In San Francisco, your sexual behavior can highly impact your risk"
	return "This field is required"
	
def get_question_field(key="",settings={}):
	if key == 'birth_year':
		obj = get_static_question_object(key=key)
		now = datetime.now()
		return forms.IntegerField(
			label = obj.text,
			help_text = obj.description,
			initial = "",
			required = True,
			max_value = now.year,
			min_value = now.year - 120,
			error_messages = {
				'required': get_static_questions_errors(key)
			},
		)
	if key == 'birth_country':
		obj = get_static_question_object(key=key)
		choices = get_static_questions_choices(key=key)
		from django.conf import settings as django_settings
		preset_choices = []
		try:
			if django_settings.HIGHLIGHTED_COUNTRIES:
				preset_choices = django_settings.HIGHLIGHTED_COUNTRIES
		except:
			pass
		return forms.ChoiceField(
			widget = HighlightedSelect( 
				highlighted = get_objects_where_matches(choices,preset_choices)),
			label = obj.text,
			help_text = obj.description,
			choices = choices,
			initial = "",
			required = True,
			error_messages = {
				'required': get_static_questions_errors(key)
			},
		)
	if key == 'birth_sex':
		obj = get_static_question_object(key=key)
		return forms.ChoiceField(
			widget = forms.RadioSelect,
			label = obj.text,
			help_text = obj.description,
			choices = get_static_questions_choices(key=key),
			required = True,
			error_messages = {
				'required': get_static_questions_errors(key)
			},
		)
	if key == 'current_sex':
		obj = get_static_question_object(key=key)
		return forms.ChoiceField(
			widget = forms.RadioSelect,
			label = obj.text,
			help_text = obj.description,
			choices = get_static_questions_choices(key=key),
			required = True,
			error_messages = {
				'required': get_static_questions_errors(key)
			},
		)
	if key == 'sex_partners':
		obj = get_static_question_object(key=key)
		return forms.MultipleChoiceField(
			widget = forms.CheckboxSelectMultiple,
			label = obj.text,
			help_text = obj.description,
			choices = get_static_questions_choices(key=key),
			required = True,
			error_messages = {
				'required': get_static_questions_errors(key)
			},
		)
	return False

def question_to_field(question, populations=[], age=False, country=False):
	answers = []
	for answer in question.answer_set.all():
		if relation_matches_population(answer.population_relationships,
			populations = populations,
			age = age,
			country = country
			):
			answers.append((answer.id,answer.text))
	field = forms.ChoiceField(
					widget = forms.RadioSelect,
					label = question.text,
					help_text = question.description,
					choices = answers,
				)
	if question.multiple_choice:
		field = forms.MultipleChoiceField(
					widget = forms.CheckboxSelectMultiple,
					label = question.text,
					help_text = question.description,
					choices = answers,
					required = False,
				)
	return field

def relation_matches_population(relation_query, populations=[], age=False, country=False):
	if relation_query.count() < 1:
		return True
	for relationship in relation_query.all():
		if relationship.matches(
				populations = populations,
				age = age,
				country = country):
			return True
	return False

def make_form_for(questions=[],settings={}):
	fields = []
	for key,field in questions:
		fields.append(str(key))
	questions.append(('field_list',	forms.CharField(
					widget = forms.HiddenInput,
					initial = ','.join(fields),
				)))
	return make_question_form_from_fields(questions,settings)

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
	
def make_email_form(settings={}):
	class EmailForm(forms.Form):
		def __init__(self, *args, **kwargs):
			self.helper = FormHelper()
			self.helper.form_method = 'post'
			if 'form_action' in settings:
				self.helper.form_action = settings['form_action']
			if 'no_submit' not in settings:
				self.helper.add_input(Submit('submit', 'Submit'))
			super(EmailForm, self).__init__(*args, **kwargs)
		email = forms.EmailField(
			required = True
		)
	return EmailForm
	
def make_sms_form(settings={}):
	class SmsForm(forms.Form):
		def __init__(self, *args, **kwargs):
			self.helper = FormHelper()
			self.helper.form_method = 'post'
			if 'form_action' in settings:
				self.helper.form_action = settings['form_action']
			if 'no_submit' not in settings:
				self.helper.add_input(Submit('submit', 'SMS'))
			super(SmsForm, self).__init__(*args, **kwargs)
		phone_number = USPhoneNumberField()
	return SmsForm