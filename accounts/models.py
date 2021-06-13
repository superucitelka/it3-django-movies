from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user/{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to=user_directory_path, blank=True, null=True, verbose_name="Avatar")
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.mode in ("RGBA", "P"): img = img.convert("RGB")
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()