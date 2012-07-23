from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from pchsi_recommends.populations.models import Population_Relationship

class Note(models.Model):
	""" Reusable Notes Field That can be filtered by population types """
	
	NOTE_TYPES = (
		('information','Information'),
		('direction','Direction'),
		('warning','Warning')
	)
	
	title = models.CharField(blank=True, max_length=100)
	text = models.TextField(blank=True)
	
	note_type = models.CharField(blank=True, null=True, max_length=20, choices=NOTE_TYPES)
	
	weight = models.IntegerField(blank=True, null=True)
	
	populations = generic.GenericRelation(Population_Relationship)
	
	content_type = models.ForeignKey(ContentType, blank=True, null=True)
	object_id = models.PositiveIntegerField(blank=True, null=True)
	content_object = generic.GenericForeignKey('content_type','object_id')