from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Game


class GameListView(ListView):
    template_name = "shopapp/games_list.html"
    context_object_name = "games"
    queryset = Game.objects.filter(archived=False)
