from django.db import models
from django.contrib.auth.models import User


def profile_preview_directory_path(instance: "Profile", filename: str) -> str:
    return f"profile_avatar/avatar_id_{instance.user.id}/preview/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preview = models.ImageField(null=True, blank=True, upload_to=profile_preview_directory_path)

