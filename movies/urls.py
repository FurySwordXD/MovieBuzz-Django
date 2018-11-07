from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('movie/<movie_name>/', views.movie),
    path('theatre/<theatre_id>/', views.theatre),
    path('show/', views.show),
    path('book/', views.book),
    path('booking_info/', views.booking_info),
]