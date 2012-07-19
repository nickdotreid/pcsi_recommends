from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView
from models import Screen

urlpatterns = patterns('pchsi_recommends.recommendations.views',
	url(r'^$','population_test_form'),
#	url(r'^recommendation/$','recommendation_detail'),
	url(r'^screens/$',
		ListView.as_view(
			model=Screen,
			context_object_name="screen_list",
			template_name="screens/list.html",
		)),
	url(r'^screens/(?P<screen_id>\d+)/$','screen_detail'),
)
