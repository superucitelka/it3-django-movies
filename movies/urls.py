from django.urls import path
from . import views

# URL mapování - seznam URL adres pro aplikaci movies
urlpatterns = [
    path('', views.index, name='index'),
    path('topten', views.topten, name='topten'),
]
