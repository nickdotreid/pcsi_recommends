from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView

urlpatterns = patterns('pchsi_recommends.questions.views',
	url(r'^$','base_question_form'),
	url(r'^recommendations$','show_recommendations'),
	url(r'^change$','all_questions'),
)