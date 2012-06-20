from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect

from django import forms

from django.template import RequestContext

from forms import PatientForm
from pchsi_recommends.recommendations.models import *

def patient_form(request):
	form = PatientForm()
	if request.method == 'POST':
		form = PatientForm(request.POST)
		if form.is_valid():
			answers = form.cleaned_data
			# map answers to populations
			# loop through screens and pull recommendations
			return render_to_response('questions/recommendations.html')
	return render_to_response('questions/form.html',{'form':form},context_instance=RequestContext(request))