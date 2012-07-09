from django import forms
from pchsi_recommends.questions.models import *
from django.utils.datastructures import SortedDict

from pchsi_recommends.recommendations.views import population_relationship_matches

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

def primary_questions():
	questions = []
	questions.append(('age',forms.ChoiceField(
		label = 'What year were you born',
		choices = list_years(100),
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
		label = 'Which sexes are your sex partners?',
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
	year = 2012
	age = 0
	while len(years)<amount:
		years.append((age,year))
		age = age + 1
		year = year - 1
	return years

def make_base_question_form():
	field_list = primary_questions()
	return make_question_form_from_fields(field_list)

def make_additional_question_form(populations=[],age=False,exclude_question_ids=[]):
	field_list = []
	for question in Question.objects.all():
		if str(question.id) not in exclude_question_ids and relation_matches_population(question.populations,populations,age):
			answers = []
			for answer in question.answer_set.all():
				if relation_matches_population(answer.population_relationships,populations,age):
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
	return make_question_form_from_fields(field_list)

def relation_matches_population(relation_query,populations,age):
	if relation_query.count() < 1:
		return True
	for relationship in relation_query.all():
		if population_relationship_matches(relationship,populations,age):
			return True
	return False
			

def make_question_form_from_fields(field_list):
	QuestionForm = type('QuestionForm',(forms.BaseForm,),{
				'base_fields':SortedDict(field_list),
				})
	class QuestionForm(QuestionForm):
		def __init__(self, *args, **kwargs):
			self.helper = FormHelper()
			self.helper.form_id = 'id-exampleForm'
			self.helper.form_class = 'blueForms'
			self.helper.form_method = 'post'
			#self.helper.form_action = 'submit_survey'

			self.helper.add_input(Submit('submit', 'Submit'))
			super(QuestionForm, self).__init__(*args, **kwargs)
	return QuestionForm