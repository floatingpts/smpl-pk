from django.conf.urls import url
from microservices import views

urlpatterns = [
    url(r'^musicians/$', views.musician_list),
    url(r'^musicians/(?P<pk>[0-9]+)$', views.musician_detail),
    url(r'^sample_packs/$', views.samplePack_list),
    url(r'^sample_packs/(?P<pk>[0-9]+)$', views.samplePack_detail),
    url(r'^samples/$', views.sample_list)
    url(r'^samples/(?P<pk>[0-9]+)$', views.sample_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
