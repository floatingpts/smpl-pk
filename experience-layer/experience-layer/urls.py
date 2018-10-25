from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home),
    path('pack_detail/<int:pk>/', views.samplePack_details),
]
