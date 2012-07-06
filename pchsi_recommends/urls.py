from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
#	url(r'^questions/', include('pchsi_recommends.questions.urls')),
	url(r'^recs/', include('pchsi_recommends.recommendations.urls')),
	url(r'^', include('pchsi_recommends.questions.urls')),
)
