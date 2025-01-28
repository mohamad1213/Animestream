from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path('search/', views.search_anime, name='search_anime'),
    path('anime/<str:anime_id>/', views.anime_detail_view, name='anime_detail'),
    path('anime/watch/2025/01/<str:anime_id>/', views.watch_anime, name='watch_anime'),
]