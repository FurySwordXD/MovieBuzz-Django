from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.sign_in),
    path('logout/', views.sign_out),
    path('edit_profile/', views.edit_profile),
    path('register/', views.register)
]