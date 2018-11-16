from django.urls import path
from microservices import views

app_name = 'microservices'
urlpatterns = [
    path('musicians/', views.musician_list, name="musician-list"),
    path('musician_login/', views.musician_login),
    path('musicians/<int:pk>/', views.musician_detail, name="musician-detail"),
    path('sample_packs/', views.sample_pack_list, name="sample-pack-list"),
    path('sample_packs/<int:pk>/', views.sample_pack_detail, name="sample-pack-detail"),
    path('samples/', views.sample_list, name="samples-list"),
    path('samples/<int:pk>/', views.sample_detail, name="samples-detail"),
    path('samples_in_pack/<int:pk>/', views.samples_in_pack),
    path('top5_sample_packs/', views.top5_sample_packs),
    path('authenticators/', views.authenticator_list),
    path('authenticator/<int:pk>/', views.authenticator_detail)
]
