from django import forms
from pchsi_recommends.questions.models import *
from django.utils.datastructures import SortedDict

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

def primary_questions(questionnaire_id):
	questions = []
	questions.append(('age',forms.ChoiceField(
		label = 'What year were you born',
		choices = list_years(100)
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
	years = []
	year = 2012
	age = 0
	while len(years)<amount:
		years.append((age,year))
		age = age + 1
		year = year - 1
	return years

def make_question_form(questionnaire_id,show_base_form=True):
	field_list = []
	questionnaire = Questionnaire.objects.filter(id=questionnaire_id)[0]
	if questionnaire:
		if questionnaire.use_base_form and show_base_form:
			field_list = primary_questions(questionnaire_id)
		for question in questionnaire.question_set.all():
			answers = []
			for answer in question.answer_set.all():
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