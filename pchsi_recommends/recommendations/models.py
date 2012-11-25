from django.db import models
from django.contrib.contenttypes import generic

from pchsi_recommends.populations.models import Population_Relationship

# Create your models here.
class Screen(models.Model):
	"""(Types of screens and vaccines offered at Clinics)"""
	
	name = models.CharField(max_length=120)
			
	class Meta:
		ordering = ['name']
		
	def get_recommendation(self,populations=[],age=False,country=False):
		recommendations = self.recommendation_set.all()
		for recommendation in recommendations:
			for population_relationship in recommendation.populations.all():
				if population_relationship.matches(
						populations = populations,
						age = age,
						country = country
						):
						return recommendation

	def __unicode__(self):
		return self.name

class Recommendation(models.Model):
	"""(Recommendation description)"""
	
	class Meta:
		ordering = ['position']
	
	screen = models.ForeignKey(Screen)
	not_recommended = models.BooleanField(default=False)
	
	frequency = models.CharField(blank=True, max_length=100)
	
	populations = generic.GenericRelation(Population_Relationship)
	
	position = models.PositiveSmallIntegerField(blank=True, null=True)

	def __unicode__(self):
		addition = ""
		if self.not_recommended:
			addition += " NOT RECOMMENDED"
		if self.frequency and self.frequency != "":
			addition += " " + self.frequency
		if self.populations.count() > 0:
			for pop in self.populations.all():
				addition += " (" + pop.__unicode__() + ")"
		return self.screen.name + addition