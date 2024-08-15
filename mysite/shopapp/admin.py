from django.contrib import admin
from .models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "description", "age_rating", "genre", "system_requirements"

    ordering = "name", "pk"

    search_fields = "name", "description", "age_rating", "genre"
