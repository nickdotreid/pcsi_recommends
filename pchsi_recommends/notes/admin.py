from pchsi_recommends.notes.models import Note,Subject
from pchsi_recommends.populations.admin import PopulationRelationshipInline

from django.contrib import admin

admin.site.register(Subject)

class NoteInline(admin.StackedInline):
	model = Note
	fields = ("title","subject","text","position","recommendation")
	sortable_field_name = "position"
	extra = 1

class NoteAdmin(admin.ModelAdmin):
	pass

admin.site.register(Note,NoteAdmin)