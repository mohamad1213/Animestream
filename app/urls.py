from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path('anime/<int:anime_id>/', views.anime_detail_view, name='anime_detail'),
    path('anime/watch/<int:anime_id>/', views.watch_anime, name='watch_anime'),
]