from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('pchsi_recommends.questions.views',
	url(r'^$','dynamic_form'),
)