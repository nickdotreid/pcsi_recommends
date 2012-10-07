from django.db import models
from django.contrib.contenttypes import generic

from adminsortable.models import Sortable

from pchsi_recommends.populations.models import Population_Relationship

# Create your models here.
class Screen(models.Model):
	"""(Types of screens and vaccines offered at Clinics)"""
	
	name = models.CharField(max_length=120)
			
	class Meta:
		ordering = ['name']

	def __unicode__(self):
		return self.name

class Recommendation(Sortable):
	"""(Recommendation description)"""
	
	class Meta(Sortable.Meta):
		pass
	
	screen = models.ForeignKey(Screen)
	not_recommended = models.BooleanField(default=False)
	
	frequency = models.CharField(blank=True, max_length=100)
	
	populations = generic.GenericRelation(Population_Relationship)

	def __unicode__(self):
		if self.not_recommended:
			return self.screen.name + " NOT RECOMMENDED"
		return self.screen.name + self.frequency