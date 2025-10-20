from django.urls import path,include
from . import views

urlpatterns = [
    path('home/',views.home,name="home"),
    path('',include("django.contrib.auth.urls"),),
    path('register/',views.register,name="register"),
    path('create_profile/',views.createProfile,name="Create your profile"),
    path('car_listings/', views.car_listings, name='car_listings'),
    path('cars/add/', views.add_car, name='add_car'),
    path('cars/edit/<int:car_id>/', views.edit_car, name='edit_car'),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
]

