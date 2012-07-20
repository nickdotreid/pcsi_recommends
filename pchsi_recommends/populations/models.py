from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django_countries import CountryField

class Population(models.Model):
	""" Population model used to describe groups of people """
	
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
	country = CountryField(blank=True, null=True)

	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey('content_type','object_id')