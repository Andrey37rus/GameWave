from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=255)  # Название
    description = models.TextField(null=False, blank=True)  # Описание
    age_rating = models.CharField(max_length=10, null=False, blank=True)  # Возрастной рейтинг
    genre = models.CharField(max_length=255, null=False, blank=True)  # Жанр
    system_requirements = models.TextField(null=False, blank=True)  # Системные требования
    created_at = models.DateTimeField(auto_now_add=True)  # Создание продукта
    archived = models.BooleanField(default=False)  # Архив

    def __str__(self) -> str:
        return f"Product(pk={self.pk}, name={self.name!r})"
