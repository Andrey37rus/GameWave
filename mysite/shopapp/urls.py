from django.urls import path
from .views import (
    GameListView
)
app_name = "shopapp"

urlpatterns = [
    path("games/", GameListView.as_view(), name="games_list"),
]
