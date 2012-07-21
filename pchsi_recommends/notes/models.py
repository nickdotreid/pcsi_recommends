from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from pchsi_recommends.populations.models import Population_Relationship

class Note(models.Model):
	""" Reusable Notes Field """
	title = models.CharField(blank=True, max_length=100)
	text = models.TextField(blank=True)
	
	weight = models.IntegerField(blank=True, null=True)
	
	populations = generic.GenericRelation(Population_Relationship)