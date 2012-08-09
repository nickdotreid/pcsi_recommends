from django.forms import Select
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.forms.widgets import flatatt
from itertools import chain

class HighlightedSelect(Select):
	"""A widget that displays JSON Key Value Pairs
	as a list of text input box pairs

	Usage (in forms.py) :
	examplejsonfield = forms.CharField(label  = "Example JSON Key Value Field", required = False,
	widget = JsonPairInputs(val_attrs={'size':35},
	                        key_attrs={'class':'large'}))

	"""

	def __init__(self, *args, **kwargs):
		"""
		highlighted - touples to show as radio buttons
		"""
	
		self.highlighted = []
		if "highlighted" in kwargs:
			self.highlighted = kwargs.pop("highlighted")
		Select.__init__(self, *args, **kwargs)

	def render(self, name, value, attrs=None, choices=()):
		if value is None: value = ''
		highlight_vals = []
		output = []
		for val,label in self.highlighted:
			highlight_vals.append(val)
			output.append(self.render_radio_input(name+'_highlight',val,label,value,attrs))
		for val,label in chain(self.choices,choices):
			if val != '' and val not in highlight_vals and val == value:
				highlight_vals.append(val)
				output.append(self.render_radio_input(name+'_highlight',val,label,value,attrs))
		final_attrs = self.build_attrs(attrs, name=name)		
		output.append(u'<select%s>' % flatatt(final_attrs))
		_choices = []
		if len(choices) < 1:
			choices = self.choices
		for val,label in choices:
			if val not in highlight_vals:
				_choices.append((val,label))
		self.choices = _choices # i don't love this line
		options = self.render_options([], [value])
		if options:
			output.append(options)
		output.append(u'</select>')
		return mark_safe(u'\n'.join(output))
	
	def render_radio_input(self,name,value,label,selected_value,attrs):
		highlight_attrs = self.build_attrs(attrs, name=name, value=value)
		if value == selected_value:
			highlight_attrs['checked'] = 'checked'
		return  u'<label class="radio"><input type="radio" %s />' % flatatt(highlight_attrs) + unicode(label) + '</label>'

	def value_from_datadict(self, data, files, name):
		"""
		Look for _other in options 
		"""
		if name+'_highlight' in data:
			return data.get(name+'_highlight', None)
		return data.get(name, None)