from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    # Add any extra fields here if needed
    pass

def user_profile_pic_path(instance, filename):
    return f'profile_pics/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('notsay', "Prefer not to say"),
    ]
    user = models.OneToOneField('fur_pdf_editor.CustomUser', on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to=user_profile_pic_path, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='notsay')
    plan = models.CharField(max_length=20, default='Free')
    magic_token = models.CharField(max_length=64, blank=True, null=True)
    token_created_at = models.DateTimeField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def is_token_expired(self):
        if self.token_created_at:
            return self.token_created_at < timezone.now() - timedelta(minutes=15)
        return True

    def get_profile_pic_url(self):
        if self.profile_pic:
            return self.profile_pic.url
        if self.gender == 'male':
            return '/media/default_profile_male.png'
        elif self.gender == 'female':
            return '/media/default_profile_female.png'
        else:
            return '/media/default_profile.png'

class PDF(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

