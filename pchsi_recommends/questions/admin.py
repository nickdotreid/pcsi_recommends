from pchsi_recommends.questions.models import Questionnaire,Question,Answer
from django.contrib import admin

class AnswerInline(admin.TabularInline):
	model = Answer
	extra = 2
	fields = ("position","populations","text")
	# define the sortable
	sortable_field_name = "position"

class QuestionAdmin(admin.ModelAdmin):
	inlines = [AnswerInline]

class QuestionInline(admin.TabularInline):
	model = Question
	extra = 1
	sortable_field_name = "position"

class QuestionnaireAdmin(admin.ModelAdmin):
	inlines = [QuestionInline]

admin.site.register(Questionnaire,QuestionnaireAdmin)
admin.site.register(Question,QuestionAdmin)