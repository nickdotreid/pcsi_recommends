from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django_countries import CountryField

class PopulationCatagory(models.Model):
	class Meta:
		ordering = ['position']
	
	short = models.CharField(max_length=25)
	name = models.CharField(max_length=120)
	
	multiple = models.BooleanField(default=True)
	
	position = models.PositiveSmallIntegerField(blank=True, null=True)
	
	def __unicode__(self):
		return self.name

class Population(models.Model):
	""" Population model used to describe groups of people """
	
	short = models.CharField(max_length=25)
	name = models.CharField(max_length=120)
	
	category = models.ForeignKey(PopulationCatagory, null=True, blank=True)

	class Meta:
		ordering = ['short']
	
	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __unicode__(self):
		return self.name

class Region(models.Model):
	name = models.CharField(max_length=120, blank=True, null=True)
	country = CountryField(blank=True, null=True)
	
	def __unicode__(self):
		if self.name:
			return self.name
		return self.country.code

class RegionCollection(models.Model):
	name = models.CharField(max_length=120, blank=True, null=True)
	exclude = models.BooleanField(default=False)
	regions = models.ManyToManyField(Region)
	
	def matches(self, country_code):
		match = False
		for region in self.regions.all():
			if region.name and region.name == country_code:
				match = True
			if region.country and region.country.code == country_code:
				match = True
		if self.exclude:
			return not match
		return match
	
	def __unicode__(self):
		elements = []
		if self.name:
			elements.append(self.name)
		if self.exclude:
			elements.append("EXCLUDE")
		return " ".join(elements) + " (" + str(self.regions.count()) + ")"
	

class Population_Relationship(models.Model):
	""" Relation model from populations to other types """
	inclusive = models.BooleanField(default=False)
	populations = models.ManyToManyField(Population,blank=True)
	
	min_age = models.IntegerField(blank=True, null=True)
	max_age = models.IntegerField(blank=True, null=True)
	
	min_year = models.IntegerField(blank=True, null=True)
	max_year = models.IntegerField(blank=True, null=True)	
	
	regions = models.ManyToManyField(RegionCollection, blank=True, null=True)

	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey('content_type','object_id')
	
	def matches(self, age=False, populations=[], country=False):
		if self.regions.count() > 0:
			if not country:
				return False
			for region in self.regions.all():
				if not region.matches(country):
					return False
					if self.inclusive:
						return True
			return True
		if age_in_range(age,self.min_age,self.max_age):
			relationship_populations = self.populations.all()
			if len(relationship_populations)<1:
				return True
			if self.inclusive:
				for population in relationship_populations:
					if population in populations:
						return True
			else:
				for population in relationship_populations:
					if population not in populations:
						return False
				return True
		return False
		
	def __unicode__(self):
		name = ''
		if self.populations.count() > 0:
			if self.inclusive:
				name += '&&'
			shorts = []
			for p in self.populations.all():
				shorts.append(p.short)
			name += ','.join(shorts)
		if self.min_age or self.max_age:
			name += '|| '
			if self.min_age:
				name += str(self.min_age)
			name += '<'
			if self.max_age:
				name += str(self.max_age)
			name += ' ||'
		if self.min_year or self.max_year:
			name += '|| '
			if self.min_year:
				name += str(self.min_year)
			name += '<'
			if self.max_year:
				name += str(self.max_year)
			name += ' ||'
		# list regions here?
		return name

def age_in_range(age=False,min=False,max=False):
	if not min and not max:
		return True
	age = int(age)
	if not age:
		return False
	if min and max:
		if age >= min and age <= max:
			return True
		return False
	if min and age >= min:
		return True
	if max and age <= max:
		return True
	return False