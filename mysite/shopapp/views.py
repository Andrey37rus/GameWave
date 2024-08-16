from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Game


class GameListView(ListView):
    template_name = "shopapp/games_list.html"
    context_object_name = "games"
    queryset = Game.objects.filter(archived=False)


class GameDetailView(DetailView):
    template_name = "shopapp/games_details.html"
    context_object_name = "game"
    # queryset = Game.objects.filter(archived=False)
    queryset = Game.objects.prefetch_related("images")
