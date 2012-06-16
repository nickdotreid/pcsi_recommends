from django.db import models

# Create your models here.
class Screen(models.Model):
	"""(Types of screens and vaccines offered at Clinics)"""
	
	name = models.CharField(max_length=120)

	def __unicode__(self):
		return u"Screen"

class Population(models.Model):
	"""(Population description)"""

	name = models.CharField(max_length=120)

	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __unicode__(self):
		return u"Population"


class Recommendation(models.Model):
	"""(Recommendation description)"""
	
	screen = models.ForeignKey(Screen)
	population = models.ForeignKey(Population)
	text = models.TextField(blank=True)
	frequency = models.CharField(blank=True, max_length=100)
	weight = models.IntegerField(blank=True, null=True)

	def __unicode__(self):
		return u"Recommendation"