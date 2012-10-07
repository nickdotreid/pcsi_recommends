from django.db import models
from django.contrib.contenttypes import generic
from pchsi_recommends.populations.models import Population,Population_Relationship

from adminsortable.models import Sortable

class Question(Sortable):
	""" Model for questions that are dynamically asked to patients """
	
	text = models.CharField(max_length=250)
	description = models.TextField(blank=True)
	
	multiple_choice = models.BooleanField(default=False)
	
	populations = generic.GenericRelation(Population_Relationship)

	class Meta(Sortable.Meta):
		pass
	
	def __unicode__(self):
		return self.text
		
class Answer(Sortable):
	""" Answers that link patients to populations """
	
	question = models.ForeignKey(Question)
	populations = models.ManyToManyField(Population,blank=True)
	
	text = models.CharField(max_length=250)
	description = models.TextField(blank=True)
	
	population_relationships = generic.GenericRelation(Population_Relationship)
	
	class Meta(Sortable.Meta):
		pass
	
	def __unicode__(self):
		return self.question.text + ": " + self.text
