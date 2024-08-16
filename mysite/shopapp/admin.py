from django.contrib import admin
from .models import Game, GameImages


class GameInline(admin.StackedInline):
    model = GameImages


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):

    inlines = [
        GameInline,
    ]

    list_display = "pk", "name", "description", "age_rating", "genre", "system_requirements", "preview"

    ordering = "name", "pk"

    search_fields = "name", "description", "age_rating", "genre"
