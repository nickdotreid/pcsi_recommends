from django.template import Context, loader
from annoying.functions import get_object_or_None
from django.http import HttpResponse, HttpResponseBadRequest, Http404, HttpResponseRedirect
from django.utils import simplejson as json
from django.core.urlresolvers import reverse

from pchsi_recommends.questions.views import *
from pchsi_recommends.questions.forms import get_questions_for, sort_answers, make_form_for, make_email_form, make_sms_form, get_static_question_object, get_static_questions_choices, remove_unneeded_answers

def ajax_answer_questions(request):
	if not request.is_ajax():
		return answer_questions(request)
	if request.method != 'POST':
		return HttpResponseBadRequest(json.dumps({
				'error':'Use POST',
			}),
			mimetype="application/json")
	if 'answers' not in request.session:
		request.session['answers'] = {}
	answers = validate_answers(
		answers = request.session['answers'],
		new_answers = request.POST,
		)
	return HttpResponse(
		json.dumps(answers),
		mimetype="application/json")

# get questions

# get recommendations