from django.db import models
from django.contrib.auth.models import User

def game_preview_directory_path(instance: "Game", filename: str) -> str:
    return "games/game_{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Game(models.Model):
    name = models.CharField(max_length=255)  # Название
    description = models.TextField(null=False, blank=True)  # Описание
    age_rating = models.CharField(max_length=10, null=False, blank=True)  # Возрастной рейтинг
    genre = models.CharField(max_length=255, null=False, blank=True)  # Жанр
    system_requirements = models.TextField(null=False, blank=True)  # Системные требования
    created_at = models.DateTimeField(auto_now_add=True)  # Создание продукта
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    archived = models.BooleanField(default=False)  # Архив
    preview = models.ImageField(null=True, blank=True, upload_to=game_preview_directory_path) #Фото

    def __str__(self) -> str:
        return f"Product(pk={self.pk}, name={self.name!r})"


def game_images_directory_path(instance: "GameImages", filename: str) -> str:
    return "games/game_{pk}/images/{filename}".format(
        pk=instance.game.pk,
        filename=filename,
    )


class GameImages(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=game_images_directory_path)
    description = models.CharField(max_length=200, null=False, blank=True)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # Создание заказа
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    receipt = models.FileField(null=True, blank=True, upload_to='orders/receipts/')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()