from pchsi_recommends.recommendations.models import Recommendation, Screen
from pchsi_recommends.populations.admin import PopulationRelationshipInline
from pchsi_recommends.notes.admin import NoteInline

from django.contrib import admin
from adminsortable.admin import SortableAdmin,SortableTabularInline

class RecommendationInline(SortableTabularInline):
	model = Recommendation
	fields = ("frequency","not_recommended")
	extra = 1

class ScreenAdmin(admin.ModelAdmin):
	inlines = [RecommendationInline,NoteInline]


admin.site.register(Screen,ScreenAdmin)

class RecommendationAdmin(SortableAdmin):
	inlines = [PopulationRelationshipInline]

admin.site.register(Recommendation,RecommendationAdmin)