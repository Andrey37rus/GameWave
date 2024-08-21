from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import Game, Order, OrderItem


class GameListView(ListView):
    template_name = "shopapp/games_list.html"
    context_object_name = "games"
    queryset = Game.objects.filter(archived=False)


class GameDetailView(DetailView):
    template_name = "shopapp/games_details.html"
    context_object_name = "game"
    # queryset = Game.objects.filter(archived=False)
    queryset = Game.objects.prefetch_related("images")


class UserOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'shopapp/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__game')

class OrderCreateView(CreateView):
    model = Order
    template_name = 'shopapp/order_form.html'
    fields = []

    def form_valid(self, form):
        # Получаем данные из запроса
        game_id = self.request.POST.get('game_id')
        quantity = self.request.POST.get('quantity')

        # Получаем объект игры
        game = get_object_or_404(Game, pk=game_id)

        # Создаем новый ордер
        order = Order.objects.create(user=self.request.user)

        # Добавляем товар в ордер
        order_item = OrderItem.objects.create(order=order, game=game, quantity=quantity)

        messages.success(self.request, f'Товар "{game.name}" добавлен в корзину!')
        return redirect('shopapp:order_list')
