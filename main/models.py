# main/models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

# Existing UploadedFile model
# main/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    upload_date = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=100, blank=True, null=True)
    file_size = models.PositiveIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.file_type:
            # Access the content type from the file instance
            self.file_type = self.file.file.content_type

        if not self.file_size:
            # Access the size from the file instance
            self.file_size = self.file.file.size

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"
