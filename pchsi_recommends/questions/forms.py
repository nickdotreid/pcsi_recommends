from django import forms


gender_at_birth = (
    ('male', 'Male'),
    ('female', 'Female'),
)

gender_current = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('transmale', 'Trans Male'),
    ('transfemale', 'Trans Female'),
)

sexual_orientation = (
	('bisexual','BiSexual'),
	('gay','Gay'),
	('lesbian','Lesbian'),
	('straight','Straight'),
)

health_conditions = (
	('pregnant','Pregnant'),
	('tb','Tuberculosis'),
	('hepb','Hepatitis B'),
	('hepc','Hepatitis C'),
	('hiv','HIV/AIDS'),
)


class PatientForm(forms.Form):
	gender_at_birth = forms.ChoiceField(
		label = 'What was your gender at birth',
		widget = forms.RadioSelect,
		choices = gender_at_birth
		)
	
	gender_current = forms.ChoiceField(
		label = 'What is your gender',
		widget = forms.RadioSelect,
		choices = gender_current
		)
	
	sexual_orientation = forms.ChoiceField(
		label = 'What is your sexual orientation',
		widget = forms.RadioSelect,
		choices = sexual_orientation
		)
	
	health_conditions = forms.MultipleChoiceField(
		required = False,
		label = 'Do you have any of the following health conditions',
		widget = forms.CheckboxSelectMultiple,
		choices = health_conditions
		)