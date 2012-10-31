from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from adminsortable.models import Sortable

from pchsi_recommends.populations.models import Population_Relationship
from pchsi_recommends.recommendations.models import Screen

class Subject(models.Model):
	title = models.CharField(blank=True, max_length=100)
	
	def __unicode__(self):
		return self.title

class Note(Sortable):
	class Meta(Sortable.Meta):
		pass

	title = models.CharField(blank=True, max_length=100)
	text = models.TextField(blank=True)
	
	subject = models.ForeignKey(Subject)
		
	populations = generic.GenericRelation(Population_Relationship)
	
	screen = models.ForeignKey(Screen, blank=True, null=True,related_name='notes')
	
	def __unicode__(self):
		name = ""
		if self.screen:
			name += "%s" % (self.screen.name)
		if self.populations.count() > 0:
			for pop in self.populations.all():
				name += " (" + pop.__unicode__() + ")"
		return name + "%s: %s" % (self.subject.title,self.title)
		
def notes_for_screen(screen, age=False, populations=[], country=False):
	notes = []
	for note in screen.notes.all():
		matches = False
		for pop in note.populations.all():
			if pop.matches(age=age, populations=populations, country=country):
				matches = True
		if matches or note.populations.count() < 1:
			found = False
			for num,n in enumerate(notes):
				if n.subject == note.subject:
					found = True
					if note.order < n.order:
						notes[num] = note
			if not found:
				notes.append(note)
	return notes