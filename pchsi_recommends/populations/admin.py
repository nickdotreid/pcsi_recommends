from pchsi_recommends.populations.models import PopulationCatagory, Population, Population_Relationship, Region, RegionCollection
from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline, GenericStackedInline
from adminsortable.admin import SortableAdmin

admin.site.register(Population)
admin.site.register(RegionCollection)
admin.site.register(Region)

class PopulationInline(admin.TabularInline):
	model = Population
	fields = ('short','name')
	extra = 1

class PopulationCatagoryAdmin(SortableAdmin):
	inlines = [PopulationInline]
	
admin.site.register(PopulationCatagory,PopulationCatagoryAdmin)

class PopulationRelationshipInline(GenericTabularInline):
	model = Population_Relationship
	extra = 1