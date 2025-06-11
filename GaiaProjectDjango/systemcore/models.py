from django.db import models

# Create your models here.

class SystemCoreColourCode(models.Model):
    name = models.CharField(max_length=100, unique=True)
    hex_code = models.CharField(max_length=7, unique=True)  # e.g., '#FFFFFF' for white
    rgb_value = models.CharField(max_length=20, unique=True)  # e.g., '255,255,255' for white

    def __str__(self):
        return f"{self.name} ({self.hex_code})"
    
    class Meta:
        verbose_name = "System Core Colour Code"
        verbose_name_plural = "System Core Colour Codes" 