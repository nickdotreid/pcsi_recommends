from django.db import models
from pchsi_recommends.recommendations.models import Population

class Question(models.Model):
	"""(Question description)"""
	
	text = models.TextField(blank=True)
	
	class Admin:
		pass

	def __unicode__(self):
		return self.text
		
class Answer(models.Model):
	
	question = models.ForeignKey(Question)
	populations = models.ManyToManyField(Population)
	text = models.TextField(blank=True)
	
	def __unicode__(self):
		return self.question.text + ": " + self.text
