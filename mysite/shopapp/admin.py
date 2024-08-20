from django.contrib import admin
from .models import Game, GameImages, Order


class OrderInline(admin.TabularInline):
    model = Game.orders.through

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
    model = Order.games.through

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    list_display = "created_at",  "user_verbose",

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("games")

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username