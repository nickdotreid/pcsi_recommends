from pchsi_recommends.questions.models import Question,Answer
from pchsi_recommends.populations.admin import PopulationRelationshipInline

from django.contrib import admin
from adminsortable.admin import SortableAdmin,SortableTabularInline


class AnswerInline(SortableTabularInline):
	model = Answer
	extra = 2
	fields = ("populations","text")

class QuestionAdmin(SortableAdmin):
	inlines = [AnswerInline,PopulationRelationshipInline]
	
admin.site.register(Question,QuestionAdmin)

class AnswerAdmin(SortableAdmin):
	inlines = [PopulationRelationshipInline]

admin.site.register(Answer,AnswerAdmin)