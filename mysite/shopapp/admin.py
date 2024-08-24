from django.contrib import admin
from .models import Game, GameImages, Order, OrderItem


class OrderInline(admin.TabularInline):
    model = OrderItem

class GameInline(admin.StackedInline):
    model = GameImages


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):

    inlines = [
        GameInline,
        OrderInline,
    ]


    list_display = "pk", "name", "description_short", "age_rating", "genre", "system_requirements", "preview"

    ordering = "name", "pk"

    search_fields = "name", "description", "age_rating", "genre"


    def description_short(self, obj: Game) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + '...'


class ProductInline(admin.StackedInline):
    model = OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    list_display = "pk", "created_at",  "user_verbose", "total_quantity", "total_price"

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related('items__game')

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

    def total_quantity(self, obj: Order) -> int:
        return sum(item.quantity for item in obj.items.all())
    total_quantity.short_description = 'total_quantity'

    def total_price(self, obj: Order) -> float:
        return sum(item.quantity * item.game.price for item in obj.items.all())  # Убедитесь, что у модели Game есть поле price
    total_price.short_description = 'total_price'