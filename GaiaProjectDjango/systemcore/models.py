# GaiaProjectDjango
# systemcore/models.py
# Django imports
from django.db import models  
from django.core.validators import RegexValidator
# from django.utils.translation import gettext_lazy as _  # For internationalization (optional)
# Create your models here.



class SystemCoreColourCode(models.Model):
    name = models.CharField(max_length=100, unique=True)   
    # This regex ensures the RGB value is in the format 'R,G,B' with each value between 0 and 255.
    rgb_validator = RegexValidator(
        regex=r'^(?:([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]),){2}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$',
        message="RGB value must be in the format 'R,G,B' where R, G, and B are integers between 0 and 255 inclusive."
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
        self.full_clean()  # Ensure all validations are run before saving
        # Capitalize the name before saving
        if self.name:
            self.name = self.name.title()
        super().save(*args, **kwargs)
        


class RJ45Pinout(models.Model):
    COLOR_CHOICES = [
        ('WHITE ORANGE', 'White Orange'),
        ('ORANGE', 'Orange'),
        ('WHITE GREEN', 'White Green'),
        ('BLUE', 'Blue'),
        ('WHITE BLUE', 'White Blue'),
        ('GREEN', 'Green'),
        ('WHITE BROWN', 'White Brown'),
        ('BROWN', 'Brown'),
    ]

    name = models.CharField(max_length=100)  # e.g., "T568A"
    pin_number = models.PositiveSmallIntegerField()  # 1 to 8
    color_code = models.CharField(max_length=20, choices=COLOR_CHOICES)

    class Meta:
        unique_together = (
            ('name', 'pin_number'),
            ('name', 'color_code'),  # Ensures color is only used once per pinout
        )
        verbose_name = "RJ45 Pinout"
        verbose_name_plural = "RJ45 Pinouts"

    def __str__(self):
        return f"{self.name} - Pin {self.pin_number}: {self.color_code}"
