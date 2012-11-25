from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from pchsi_recommends.populations.models import Population_Relationship
from pchsi_recommends.recommendations.models import Screen, Recommendation

class Subject(models.Model):
	title = models.CharField(blank=True, max_length=100)
	
	def __unicode__(self):
		return self.title

class Note(models.Model):
	class Meta:
		ordering = ['position']

	title = models.CharField(blank=True, max_length=100)
	text = models.TextField(blank=True)
	
	subject = models.ForeignKey(Subject)
		
	recommendation = models.ForeignKey(Recommendation, blank=True, null=True,related_name='notes')
	screen = models.ForeignKey(Screen, blank=True, null=True,related_name='notes')
	
	position = models.PositiveSmallIntegerField(blank=True, null=True)
	
	def __unicode__(self):
		name = []
		if self.recommendation:
			name.append(str(self.recommendation))
		elif self.screen:
			name.append(self.screen.name)
		name.append("%s: %s" % (self.subject.title,self.title))
		return " - ".join(name)
		
def notes_for(screen=False, recommendation=False):
	notes = []
	_notes = []
	if screen:
		_notes = screen.notes.all()
	elif recommendation:
		_notes = recommendation.notes.all()
	for note in _notes:
		if not note.recommendation or recommendation == note.recommendation:
			found = False
			for num,n in enumerate(notes):
				if n.subject == note.subject:
					found = True
					if note.order < n.order:
						notes[num] = note
			if not found:
				notes.append(note)
	return notes