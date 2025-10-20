from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_car_price, name='predict_car_price'),
    path('api/predict/', views.prediction_api, name='prediction_api'),
]