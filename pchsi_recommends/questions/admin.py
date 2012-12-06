from pchsi_recommends.questions.models import Question,Answer
from pchsi_recommends.populations.admin import PopulationRelationshipInline

from django.contrib import admin


class AnswerInline(admin.StackedInline):
	model = Answer
	extra = 2
	fields = ("populations","text","position")

class QuestionAdmin(admin.ModelAdmin):
	inlines = [AnswerInline,PopulationRelationshipInline]
	
admin.site.register(Question,QuestionAdmin)

class AnswerAdmin(admin.ModelAdmin):
	inlines = [PopulationRelationshipInline]

admin.site.register(Answer,AnswerAdmin)