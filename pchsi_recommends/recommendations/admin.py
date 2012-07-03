from pchsi_recommends.recommendations.models import Recommendation, Screen, Population, Population_Relationship
from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline, GenericStackedInline

class RecommendationInline(admin.TabularInline):
	model = Recommendation
	fields = ("weight","frequency","not_recommended")
	sortable_field_name = "weight"
	extra = 1

class ScreenAdmin(admin.ModelAdmin):
	inlines = [RecommendationInline]


admin.site.register(Screen,ScreenAdmin)
admin.site.register(Population)

class PopulationRelationshipInline(GenericTabularInline):
	model = Population_Relationship
	extra = 1

class RecommendationAdmin(admin.ModelAdmin):
	inlines = [PopulationRelationshipInline]

admin.site.register(Recommendation,RecommendationAdmin)