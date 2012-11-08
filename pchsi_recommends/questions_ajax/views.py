from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404, redirect
from annoying.functions import get_object_or_None
from django.http import HttpResponse, HttpResponseBadRequest, Http404, HttpResponseRedirect
from django.utils import simplejson as json
from django.core.urlresolvers import reverse

from pchsi_recommends.questions.views import *

def ajax_answer_questions(request):
	if not request.is_ajax():
		return answer_questions(request)
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			answers = []
			for question,answer in form.cleaned_data.items():
				answers.append(answer)
			message = ""
			for answer in answers_for_form(form):
				message = render_to_string("questions/answered.html",{
					"answer":answer,
					})
			return HttpResponse(json.dumps({
				"answers":answers,
				"message":message,
				}),
			                mimetype="application/json")
	return HttpResponseBadRequest(json.dumps("answered"),
	                mimetype="application/json")

# get questions

# get recommendations