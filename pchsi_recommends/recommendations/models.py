from django.db import models
from django.contrib.contenttypes import generic

from pchsi_recommends.populations.models import Population_Relationship

# Create your models here.
class Screen(models.Model):
	"""(Types of screens and vaccines offered at Clinics)"""
	
	name = models.CharField(max_length=120)
			
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