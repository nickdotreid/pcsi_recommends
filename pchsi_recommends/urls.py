from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'static/home.html'}),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^questions/', include('pchsi_recommends.questions.urls')),
	url(r'^recomendations/', include('pchsi_recommends.recommendations.urls')),
)
