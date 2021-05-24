from django.urls import path, re_path
from . import views

# URL mapování - seznam URL adres pro aplikaci movies
urlpatterns = [
    path('', views.index, name='index'),
    path('films/', views.FilmListView.as_view(), name='films'),
    #re_path(r'^films/genres/(?P<genre_name>[\w-]+)/:?(?P<order>[\w-]*)$', views.FilmListView.as_view(), name='film_genre'),
    path('films/genres/<str:genre_name>/', views.FilmListView.as_view(), name='film-genre'),
    path('films/<int:pk>/', views.FilmDetailView.as_view(), name='film-detail'),
    path('films/create/', views.FilmCreate.as_view(), name='film-create'),
    path('films/<int:pk>/update/', views.FilmUpdate.as_view(), name='film-update'),
    path('films/<int:pk>/delete/', views.FilmDelete.as_view(), name='film-delete'),
    #path('films/<int:pk>/edit/', views.edit_film, name='film-edit'),
    path('clear_cache/', views.clear_cache),
]

