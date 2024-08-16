from django.urls import path
from .views import (
    GameListView,
    GameDetailView
)
app_name = "shopapp"

urlpatterns = [
    path("games/", GameListView.as_view(), name="games_list"),
    path("games/<int:pk>/", GameDetailView.as_view(), name="games_details")
]
