from django.db import models

# Create your models here.
class Email(models.Model):
    email = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Emails"
    
    def __str__(self):
        return self.email