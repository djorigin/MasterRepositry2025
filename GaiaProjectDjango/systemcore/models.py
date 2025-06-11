# GaiaProjectDjango
# systemcore/models.py
# Django imports
from django.db import models  
from django.core.validators import RegexValidator
# from django.utils.translation import gettext_lazy as _  # For internationalization (optional)
# Create your models here.



class SystemCoreColourCode(models.Model):
    name = models.CharField(max_length=100, unique=True)   
    rgb_validator = RegexValidator(
        regex=r'^(?:[0-9]{1,3},){2}[0-9]{1,3}$',
        message="RGB value must be in the format 'R,G,B' where R, G, and B are integers between 0 and 255."
    )
    rgb_value = models.CharField(
        max_length=20,
        unique=True,
        validators=[rgb_validator]
    )  # e.g., '255,255,255' for white

    hex_validator = RegexValidator(
        regex=r'^#[0-9A-Fa-f]{6}$',
        message="Enter a valid hex color code (e.g., '#FFFFFF')."
    )
    hex_code = models.CharField(
        max_length=7,
        validators=[hex_validator]
    )  # e.g., '#FFFFFF' for white

    def __str__(self):
        return f"{self.name} ({self.hex_code}, RGB: {self.rgb_value})"
    
    class Meta:
        verbose_name = "System Core Color Code"
        verbose_name_plural = "System Core Color Codes"

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.capitalize()
        super().save(*args, **kwargs)