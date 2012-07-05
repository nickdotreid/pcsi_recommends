from pchsi_recommends.populations.models import Population, Population_Relationship
from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline, GenericStackedInline

admin.site.register(Population)

class PopulationRelationshipInline(GenericTabularInline):
	model = Population_Relationship
	extra = 1