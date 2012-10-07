from pchsi_recommends.notes.models import Note,Subject
from adminsortable.admin import SortableAdmin,SortableTabularInline
from pchsi_recommends.populations.admin import PopulationRelationshipInline

from django.contrib import admin

admin.site.register(Subject)

class NoteInline(SortableTabularInline):
	model = Note
	fields = ("title","subject","text")
	extra = 1

class NoteAdmin(SortableAdmin):
	inlines = [PopulationRelationshipInline]

admin.site.register(Note,NoteAdmin)