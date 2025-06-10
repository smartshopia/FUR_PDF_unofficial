from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class PDF(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class PDFUploadForm(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return self.title
    
# Profile model to store additional user information
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    magic_token = models.CharField(max_length=64, blank=True, null=True)
    token_created_at = models.DateTimeField(auto_now_add=True)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    def is_token_expired(self):
        return self.token_created_at < timezone.now() - timedelta(minutes=15)


