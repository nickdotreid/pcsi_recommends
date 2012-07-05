from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('pchsi_recommends.recommendations.views',
	url(r'^$','show_recommendations'),
	url(r'^direct$','population_test_form'),
)
