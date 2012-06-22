from django import forms
from pchsi_recommends.questions.models import *
		
def make_question_form(questionnaire_id):
	field_list = []
	fields = {}
	questionnaire = Questionnaire.objects.filter(id=questionnaire_id)[0]
	if questionnaire:
		for question in questionnaire.question_set.order_by('weight'):
			answers = []
			for answer in question.answer_set.all():
				answers.append((answer.id,answer.text))
			fields[question.short] = forms.ChoiceField(
					widget = forms.RadioSelect,
					label = question.text,
					choices = answers
				)
	return type('QuestionForm',(forms.BaseForm,),{'base_fields':fields})