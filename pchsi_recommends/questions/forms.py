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


class PatientForm(forms.Form):
    gender_at_birth = forms.ChoiceField(widget = forms.RadioSelect,choices = gender_at_birth)