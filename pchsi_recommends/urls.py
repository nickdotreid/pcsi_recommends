from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^', include('pchsi_recommends.questions_ajax.urls')),
	url(r'^', include('pchsi_recommends.questions.urls')),
	url(r'^', include('pchsi_recommends.recommendations.urls')),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^grappelli/', include('grappelli.urls')),
	url(r'^providers/', include('pchsi_recommends.provider_form.urls')),
)
