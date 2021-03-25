from django.urls import path, re_path
from . import views

# URL mapování - seznam URL adres pro aplikaci movies
urlpatterns = [
    path('', views.index, name='index'),
    path('films/', views.FilmListView.as_view(), name='films'),
    #re_path(r'^films/genres/(?P<genre_name>[\w-]+)/:?(?P<order>[\w-]*)$', views.FilmListView.as_view(), name='film_genre'),
    path('films/genres/<str:genre_name>/', views.FilmListView.as_view(), name='film_genre'),
    path('films/<int:pk>/', views.FilmDetailView.as_view(), name='film_detail'),
]
