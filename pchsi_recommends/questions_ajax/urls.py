from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView

urlpatterns = patterns('pchsi_recommends.questions_ajax.views',
	url(r'^answer','ajax_answer_questions'),
)