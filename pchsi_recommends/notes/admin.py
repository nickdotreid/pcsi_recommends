from pchsi_recommends.notes.models import Note,Subject
from django.contrib.contenttypes.generic import GenericTabularInline, GenericStackedInline
from pchsi_recommends.populations.admin import PopulationRelationshipInline

from django.contrib import admin

admin.site.register(Subject)

class NoteInline(GenericTabularInline):
	model = Note
	fields = ("title","subject","text","weight")
	sortable_field_name = "weight"
	extra = 1

class NoteAdmin(admin.ModelAdmin):
	inlines = [PopulationRelationshipInline]

admin.site.register(Note,NoteAdmin)