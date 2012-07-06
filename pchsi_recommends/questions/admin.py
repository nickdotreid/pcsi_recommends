from pchsi_recommends.questions.models import Question,Answer
from pchsi_recommends.populations.admin import PopulationRelationshipInline

from django.contrib import admin


class AnswerInline(admin.TabularInline):
	model = Answer
	extra = 2
	fields = ("position","populations","text")
	# define the sortable
	sortable_field_name = "position"

class QuestionAdmin(admin.ModelAdmin):
	inlines = [AnswerInline,PopulationRelationshipInline]
	
admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer)