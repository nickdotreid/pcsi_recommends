from django.forms import CheckboxSelectMultiple
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.forms.widgets import flatatt
from itertools import chain

class CheckboxSelectMultipleWithHidden(CheckboxSelectMultiple):
	def render(self, name, value, attrs=None, choices=()):
		return mark_safe(
			'<input type="hidden" name="%s_present" value="true" />' % (name) 
			+ super(CheckboxSelectMultipleWithHidden,self).render(name,value,attrs,choices)
			)

	def value_from_datadict(self, data, files, name):
		value = super(CheckboxSelectMultipleWithHidden,self).value_from_datadict(data,files,name)
		if type(value) == list and len(value)<1:
			if name + '_present' not in data:
				return None
		if value is not None:
			return value
		return None