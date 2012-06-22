from pchsi_recommends.questions.models import Questionnaire,Question,Answer
from django.contrib import admin

class AnswerInline(admin.StackedInline):
	model = Answer
	extra = 2

class QuestionAdmin(admin.ModelAdmin):
	inlines = [AnswerInline]

admin.site.register(Questionnaire)
admin.site.register(Question,QuestionAdmin)