from pchsi_recommends.notes.models import Note
from django.contrib.contenttypes.generic import GenericTabularInline, GenericStackedInline
from pchsi_recommends.populations.admin import PopulationRelationshipInline

from django.contrib import admin

class NoteInline(GenericTabularInline):
	model = Note
	fields = ("title","note_type","text","weight")
	sortable_field_name = "weight"
	extra = 1

class NoteAdmin(admin.ModelAdmin):
	inlines = [PopulationRelationshipInline]

admin.site.register(Note,NoteAdmin)