from pchsi_recommends.notes.models import Note
from pchsi_recommends.populations.admin import PopulationRelationshipInline

from django.contrib import admin

class NoteInline(admin.TabularInline):
	model = Note
	fields = ("title","text","weight")
	sortable_field_name = "weight"
	extra = 1

class NoteAdmin(admin.ModelAdmin):
	inlines = [PopulationRelationshipInline]

admin.site.register(Note,NoteAdmin)