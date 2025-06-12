# GaiaProjectDjango
# systemcore/models.py
# Django imports
from django.db import models, transaction, IntegrityError
from django.core.validators import RegexValidator
import random
import string
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

def generate_supplier_code():
    prefix = ''.join(random.choices(string.ascii_uppercase, k=3))
    mid = ''.join(random.choices(string.digits, k=4))
    end = ''.join(random.choices(string.digits, k=5))
    return f"{prefix}-{mid}-{end}"

class Supplier(models.Model):
    supplier_code = models.CharField(max_length=50, primary_key=True, editable=False)
    name = models.CharField(max_length=255, unique=True)
    legal_name = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    tax_id = models.CharField(max_length=100, blank=True, null=True)
    is_manufacturer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Supplier / Manufacturer"
        verbose_name_plural = "Suppliers / Manufacturers"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.supplier_code:
            for _ in range(10):  # Try up to 10 times to avoid rare collisions
                code = generate_supplier_code()
                try:
                    with transaction.atomic():
                        if not Supplier.objects.filter(supplier_code=code).exists():
                            self.supplier_code = code
                            break
                except IntegrityError:
                    continue
            else:
                raise ValueError("Could not generate a unique supplier code after 10 attempts.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

