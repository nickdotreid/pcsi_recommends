from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect

from django import forms

from django.template import RequestContext

from forms import PatientForm

def patient_form(request):
	if request.method == 'POST':
		form = PatientForm(request.POST)
		if form.is_valid():
			return render_to_response('questions/recommendations.html')
	form = PatientForm()
	return render_to_response('questions/form.html',{'form':form},context_instance=RequestContext(request))