from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView

from models import Questionnaire

urlpatterns = patterns('pchsi_recommends.questions.views',
	url(r'^$',
		ListView.as_view(
			model=Questionnaire,
			context_object_name="questionnaire_list",
		)),
	url(r'^(?P<questionnaire_id>\d+)/$','questionnaire_form'),
)