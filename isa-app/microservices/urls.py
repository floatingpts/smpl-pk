from django.urls import path
from microservices import views

app_name = 'microservices'
urlpatterns = [
    path('musicians/', views.musician_list),
    path('musicians/<int:pk>/', views.musician_detail),
    path('sample_packs/', views.sample_pack_list),
    path('sample_packs/<int:pk>/', views.sample_pack_detail),
    path('samples/', views.sample_list),
    path('samples/<int:pk>/', views.sample_detail),
    path('samples_in_pack/<int:pk>/', views.samples_in_pack),
    path('top5_packs/', views.top5_sample_packs),
]
