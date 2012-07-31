from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView

urlpatterns = patterns('pchsi_recommends.questions.views',
	url(r'^$','initial_page'),
	url(r'^recommendations$','recommendations_page'),
	url(r'^change$','all_questions'),
	url(r'^ajax/save$','ajax_save_answer'),
	url(r'^ajax/questions$','ajax_get_questions'),
	url(r'^ajax/update$','ajax_get_recommendations'),
)