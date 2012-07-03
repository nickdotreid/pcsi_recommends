from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('pchsi_recommends.recommendations.views',
	url(r'^$','from_url_string'),
	url(r'^direct$','population_test_form'),
)
