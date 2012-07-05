from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView

from models import Questionnaire

urlpatterns = patterns('pchsi_recommends.questions.views',
	url(r'^$','base_question_form'),
	url(r'^more$','additional_question_form'),
)