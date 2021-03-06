from django.db import models
from django.contrib.contenttypes import generic
from pchsi_recommends.populations.models import Population,Population_Relationship

class Question(models.Model):
	""" Model for questions that are dynamically asked to patients """
	
	text = models.CharField(max_length=250)
	description = models.TextField(blank=True)
	
	multiple_choice = models.BooleanField(default=False)
	
	populations = generic.GenericRelation(Population_Relationship)
	
	position = models.PositiveSmallIntegerField(blank=True, null=True)
	
	class Meta:
		ordering = ['position']
	
	def __unicode__(self):
		return self.text
		
class Answer(models.Model):
	""" Answers that link patients to populations """
	
	question = models.ForeignKey(Question)
	populations = models.ManyToManyField(Population,blank=True)
	
	text = models.CharField(max_length=250)
	description = models.TextField(blank=True)
	
	population_relationships = generic.GenericRelation(Population_Relationship)
	
	position = models.PositiveSmallIntegerField(blank=True, null=True)
	
	class Meta:
		ordering = ['position']

	
	def __unicode__(self):
		return self.question.text + ": " + self.text
