from django.conf.urls import url
from microservices import views

urlpatterns = [
    url(r'^musicians/$', views.musician_list),
    url(r'^musicians/(?P<pk>[0-9]+)$', views.musician_detail),
    url(r'^sample_packs/$', views.sample_pack_list),
    url(r'^sample_packs/(?P<pk>[0-9]+)$', views.sample_pack_detail),
    url(r'^samples/$', views.sample_list),
    url(r'^samples/(?P<pk>[0-9]+)$', views.sample_detail),
]
