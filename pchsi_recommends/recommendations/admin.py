from pchsi_recommends.recommendations.models import Recommendation, Screen
from pchsi_recommends.populations.admin import PopulationRelationshipInline
from pchsi_recommends.notes.admin import NoteInline

from django.contrib import admin

class RecommendationInline(admin.TabularInline):
	model = Recommendation
	fields = ("frequency","not_recommended","position")
	extra = 1
	sortable_field_name = "position"

class ScreenAdmin(admin.ModelAdmin):
	inlines = [RecommendationInline,NoteInline]


admin.site.register(Screen,ScreenAdmin)

class RecommendationAdmin(admin.ModelAdmin):
	inlines = [PopulationRelationshipInline]

admin.site.register(Recommendation,RecommendationAdmin)