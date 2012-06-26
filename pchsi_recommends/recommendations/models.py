from django.db import models

# Create your models here.
class Screen(models.Model):
	"""(Types of screens and vaccines offered at Clinics)"""
	
	name = models.CharField(max_length=120)

	def __unicode__(self):
		return self.name

class Population(models.Model):
	"""(Population description)"""

	name = models.CharField(max_length=120)

	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __unicode__(self):
		return self.name


class Recommendation(models.Model):
	"""(Recommendation description)"""
	
	screen = models.ForeignKey(Screen)
	
	populations = models.ManyToManyField(Population,blank=True)
	add_populations = models.BooleanField(default=False)
	
	weight = models.IntegerField(null=True)
	min_age = models.IntegerField(blank=True, null=True)
	max_age = models.IntegerField(blank=True, null=True)
	
	not_recommended = models.BooleanField(default=False)
	
	frequency = models.CharField(blank=True, max_length=100)

	def __unicode__(self):
		return self.screen.name + ' (' + str(self.weight) + ') ' + self.frequency