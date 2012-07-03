from pchsi_recommends.questions.models import Questionnaire,Question,Answer
from pchsi_recommends.recommendations.admin import PopulationRelationshipInline
from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline, GenericStackedInline


class AnswerInline(admin.TabularInline):
	model = Answer
	extra = 2
	fields = ("position","populations","text")
	# define the sortable
	sortable_field_name = "position"

class QuestionAdmin(admin.ModelAdmin):
	inlines = [AnswerInline,PopulationRelationshipInline]

class QuestionInline(admin.TabularInline):
	model = Question
	extra = 1
	sortable_field_name = "position"

class QuestionnaireAdmin(admin.ModelAdmin):
	inlines = [QuestionInline]

admin.site.register(Questionnaire,QuestionnaireAdmin)
admin.site.register(Question,QuestionAdmin)