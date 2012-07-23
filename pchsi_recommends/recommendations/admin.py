from pchsi_recommends.recommendations.models import Recommendation, Screen
from pchsi_recommends.populations.admin import PopulationRelationshipInline
from pchsi_recommends.notes.admin import NoteInline

from django.contrib import admin

class RecommendationInline(admin.TabularInline):
	model = Recommendation
	fields = ("weight","frequency","not_recommended")
	sortable_field_name = "weight"
	extra = 1

class ScreenAdmin(admin.ModelAdmin):
	inlines = [RecommendationInline,NoteInline]


admin.site.register(Screen,ScreenAdmin)

class RecommendationAdmin(admin.ModelAdmin):
	inlines = [PopulationRelationshipInline]

admin.site.register(Recommendation,RecommendationAdmin)