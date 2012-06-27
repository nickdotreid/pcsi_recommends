from django import forms
from pchsi_recommends.questions.models import *
from django.utils.datastructures import SortedDict

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
		
def _make_question_form(questionnaire_id):
	field_list = []
	questionnaire = Questionnaire.objects.filter(id=questionnaire_id)[0]
	if questionnaire:
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
			field_list.append((str(question.id),field))
	return type('QuestionForm',(forms.BaseForm,),{
		'base_fields':SortedDict(field_list),
		})

def make_question_form(questionnaire_id):
	QuestionForm = _make_question_form(questionnaire_id)
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