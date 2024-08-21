from django.urls import path
from .views import (
    GameListView,
    GameDetailView,
    UserOrderListView,
    OrderCreateView
)
app_name = "shopapp"

urlpatterns = [
    path("games/", GameListView.as_view(), name="games_list"),
    path("games/<int:pk>/", GameDetailView.as_view(), name="games_details"),
    path('orders/', UserOrderListView.as_view(), name='order_list'),
    path('add_to_cart/', OrderCreateView.as_view(), name='add_to_cart'),
]
