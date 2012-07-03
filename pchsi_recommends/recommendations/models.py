from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

# Create your models here.
class Screen(models.Model):
	"""(Types of screens and vaccines offered at Clinics)"""
	
	name = models.CharField(max_length=120)

	def __unicode__(self):
		return self.name

class Population(models.Model):
	"""(Population description)"""
	
	short = models.CharField(max_length=25)
	name = models.CharField(max_length=120)

	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __unicode__(self):
		return self.name

class Population_Relationship(models.Model):
	""" Relation model from populations to other types """
	inclusive = models.BooleanField(default=False)
	populations = models.ManyToManyField(Population,blank=True)
	min_age = models.IntegerField(blank=True, null=True)
	max_age = models.IntegerField(blank=True, null=True)

	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey('content_type','object_id')


class Recommendation(models.Model):
	"""(Recommendation description)"""
	
	screen = models.ForeignKey(Screen)
	weight = models.IntegerField(null=True)
	not_recommended = models.BooleanField(default=False)
	frequency = models.CharField(blank=True, max_length=100)
	populations = generic.GenericRelation(Population_Relationship)

	def __unicode__(self):
		return self.screen.name + ' (' + str(self.weight) + ') ' + self.frequency