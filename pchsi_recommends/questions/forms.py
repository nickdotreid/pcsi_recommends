from django import forms
from pchsi_recommends.questions.models import *
from django.utils.datastructures import SortedDict
		
def make_question_form(questionnaire_id):
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