from django.conf.urls import url
from experiences-layer import views

urlpatterns = [
    url(r'^home/$', views.home),
    url(r'^pack_detail/(?P<pk>[0-9]+)?/$', views.samplePack_details),
]
