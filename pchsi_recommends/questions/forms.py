from django import forms
from pchsi_recommends.questions.models import *
		
def make_question_form():
	fields = {}
	for question in Question.objects.all():
		answers = []
		for answer in question.answer_set.all():
			answers.append((answer.id,answer.text))
		fields[question.id] = forms.ChoiceField(
			widget = forms.RadioSelect,
			label = question.text,
			choices = answers
		)
	return type('QuestionForm',(forms.BaseForm,),{'base_fields':fields})