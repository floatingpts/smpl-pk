from django.conf.urls import url
from microservices import views

urlpatterns = [
    url(r'^musicians/(?P<pk>[0-9]+)/$', views.musician_crud),
    url(r'^sample_packs/(?P<pk>[0-9]+)/$', views.samplePack_crud),
    url(r'^samples/(?P<pk>[0-9]+)/$', views.sample_crud),
]
