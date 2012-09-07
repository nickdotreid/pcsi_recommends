from django.db import models
from django.contrib.contenttypes import generic

from pchsi_recommends.populations.models import Population_Relationship

from pchsi_recommends.notes.models import Note

# Create your models here.
class Screen(models.Model):
	"""(Types of screens and vaccines offered at Clinics)"""
	
	name = models.CharField(max_length=120)
	notes = generic.GenericRelation(Note)
	
	def select_notes(self, age=False, populations=[], country=False):
		notes = []
		for note in self.notes.all():
			matches = False
			for pop in note.populations.all():
				if pop.matches(age=age, populations=populations, country=country):
					matches = True
			if matches or note.populations.count() < 1:
				found = False
				for num,n in enumerate(notes):
					if n.subject == note.subject:
						found = True
						if note.weight < n.weight:
							notes[num] = note
				if not found:
					notes.append(note)
		return notes
			
	class Meta:
		ordering = ['name']

	def __unicode__(self):
		return self.name

class Recommendation(models.Model):
	"""(Recommendation description)"""
	
	screen = models.ForeignKey(Screen)
	weight = models.IntegerField(null=True)
	not_recommended = models.BooleanField(default=False)
	
	now = models.BooleanField(default=False)
	frequency = models.CharField(blank=True, max_length=100)
	
	populations = generic.GenericRelation(Population_Relationship)

	def __unicode__(self):
		return self.screen.name + ' (' + str(self.weight) + ') ' + self.frequency