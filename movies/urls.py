from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('movie/<movie_name>/', views.movie),
    path('show/', views.show),
    path('book/', views.book),
    path('booking_info/', views.booking_info),
]