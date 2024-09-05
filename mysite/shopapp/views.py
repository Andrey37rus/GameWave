from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from decimal import Decimal
from django.db.models import F, ExpressionWrapper, DecimalField
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Game, Order, OrderItem


class GameListView(ListView):
    template_name = "shopapp/games_list.html"
    context_object_name = "games"

    def get_queryset(self):
        return Game.objects.filter(archived=False).annotate(
            discounted_price=ExpressionWrapper(
                F('price') * (1 - F('discount') / 100),
                output_field=DecimalField(max_digits=8, decimal_places=2)
            )
        )


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


def calculate_total_price(game, quantity):
    discount = Decimal(game.discount) / Decimal(100) if game.discount else Decimal(0)
    total_price = Decimal(game.price) * Decimal(quantity) * (Decimal(1) - discount)
    return total_price

@method_decorator(login_required, name='dispatch')
class OrderCreateView(CreateView):
    model = Order
    template_name = 'shopapp/order_list.html'
    fields = []

    def form_valid(self, form):
        # Получаем данные из запроса
        game_id = self.request.POST.get('game_id')
        quantity = self.request.POST.get('quantity')

        # Получаем объект игры
        game = get_object_or_404(Game, pk=game_id)

        # Создаем новый ордер
        order = Order.objects.create(user=self.request.user)

        # Вычисляем цену с учетом скидки
        total_price_value = calculate_total_price(game, quantity)

        # Добавляем товар в ордер
        order_item = OrderItem.objects.create(order=order, game=game, quantity=quantity, total_price=total_price_value)

        messages.success(self.request, f'Товар "{game.name}" добавлен в корзину!')
        return redirect('shopapp:order_list')

class OrderUpdateView(UpdateView):
    model = OrderItem
    fields = ["quantity"]
    template_name = "shopapp/order_update_form.html"

    def form_valid(self, form):
        quantity = form.cleaned_data['quantity']
        if form.cleaned_data['quantity'] < 1:
            form.add_error('quantity', 'The quantity must be at least 1')
            return self.form_invalid(form)

        # Получаем объект игры
        game = self.object.game

        # Вычисляем новую цену с учетом скидки
        total_price_value = calculate_total_price(game, quantity)

        # Обновляем количество и общую цену
        self.object.quantity = quantity
        self.object.total_price = total_price_value
        self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("shopapp:order_list")


class OrderDeleteView(DeleteView):
    model = OrderItem
    template_name = "shopapp/order_confirm_delete.html"
    success_url = reverse_lazy("shopapp:order_list")

    @receiver(post_delete, sender=OrderItem)
    def delete_order_if_no_items(sender, instance, **kwargs):
        order = instance.order
        if not order.items.exists():
            order.delete()


