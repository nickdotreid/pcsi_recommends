from pchsi_recommends.recommendations.models import Recommendation, Screen, Population, Population_Relationship
from django.contrib import admin

admin.site.register(Screen)
admin.site.register(Population)

class PopulationRelationshipInline(admin.TabularInline):
	model = Population_Relationship
	extra = 1

class RecommendationAdmin(admin.ModelAdmin):
	inlines = [PopulationRelationshipInline]

admin.site.register(Recommendation,RecommendationAdmin)