from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView

urlpatterns = patterns('pchsi_recommends.questions.views',
	url(r'^$','initial_page'),
	url(r'^recommendations/print/$','print_recommendations'),
	url(r'^recommendations/(?P<recommendation_id>\d+)/$','recommendation_detail'),
	url(r'^recommendations$','recommendations_page'),
	url(r'^answer/(?P<question_id>\d+)','answer_questions'),
	url(r'^answer','answer_questions'),
	url(r'^change$','all_questions'),
)