from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'pchsi_recommends.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^questions/', include('pchsi_recommends.questions.urls')),
	url(r'^recomendations/', include('pchsi_recommends.recommendations.urls')),
)
