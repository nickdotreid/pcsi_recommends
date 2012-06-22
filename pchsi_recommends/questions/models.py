from django.db import models
from pchsi_recommends.recommendations.models import Population

class Form(models.Model):
	''' Collects questions and has description '''
	title = models.CharField(blank=True, max_length=100)
	directions = models.TextField(blank=True)
	
	def __unicode__(self):
		return self.title

class Question(models.Model):
	"""(Question description)"""
	
	form = models.ForeignKey(Form)
	text = models.CharField(max_length=250)
	description = models.TextField(blank=True)
	
	weight = models.IntegerField(blank=True, null=True)
	
	def __unicode__(self):
		return self.text
		
class Answer(models.Model):
	
	question = models.ForeignKey(Question)
	populations = models.ManyToManyField(Population)
	
	text = models.CharField(max_length=250)
	description = models.TextField(blank=True)
	
	def __unicode__(self):
		return self.question.text + ": " + self.text
