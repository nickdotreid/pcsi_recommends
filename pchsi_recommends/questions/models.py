from django.db import models
from django.contrib.contenttypes import generic
from pchsi_recommends.recommendations.models import Population,Population_Relationship

class Questionnaire(models.Model):
	''' Collects questions and has description '''
	
	short = models.CharField(unique=True,max_length=50)
	title = models.CharField(blank=True, max_length=100)
	directions = models.TextField(blank=True)
	
	def __unicode__(self):
		return self.title

class Question(models.Model):
	"""(Question description)"""
	questionnaire = models.ForeignKey(Questionnaire)
	
	text = models.CharField(max_length=250)
	description = models.TextField(blank=True)
	
	multiple_choice = models.BooleanField(default=False)
	position = models.PositiveSmallIntegerField("Position")
	
	populations = generic.GenericRelation(Population_Relationship)

	class Meta:
		ordering = ['position']
	
	def __unicode__(self):
		return self.text + ": " + self.questionnaire.title
		
class Answer(models.Model):
	
	question = models.ForeignKey(Question)
	populations = models.ManyToManyField(Population)
	
	text = models.CharField(max_length=250)
	description = models.TextField(blank=True)
	
	position = models.PositiveSmallIntegerField("Position")
	
	class Meta:
		ordering = ['position']
	
	def __unicode__(self):
		return self.question.text + ": " + self.text
