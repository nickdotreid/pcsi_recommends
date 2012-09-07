from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView

urlpatterns = patterns('pchsi_recommends.questions.views',
	url(r'^$','initial_page'),
	url(r'^recommendations/(?P<recommendation_id>\d+)/$','recommendation_detail'),
	url(r'^recommendations$','recommendations_page'),
	url(r'^change$','all_questions'),
)