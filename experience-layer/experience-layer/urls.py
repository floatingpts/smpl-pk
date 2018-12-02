from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home),
    path('pack_detail/<int:pk>/', views.samplePack_details),
    path('musician_detail/<int:pk>/', views.musician_detail),
    path('login/', views.login, name='login'),
    path('create_account/', views.create_account),
    path('create_listing/', views.create_listing),
    path('logout/', views.logout),
    path('search/', views.search),
]
