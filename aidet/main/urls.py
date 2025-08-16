from django.urls import path
from . import views
from .views import run_my_code
from .views import detect_view
urlpatterns = [
    path('', views.index),
    path('detection/', views.detection, name='detection'),
    path('run/', run_my_code),
    path('detect/', detect_view, name='detect'),
]   