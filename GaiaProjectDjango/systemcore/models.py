# GaiaProjectDjango
# systemcore/models.py
# Django imports
from django.db import models, transaction, IntegrityError
from django.core.validators import RegexValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import random
import string
from decimal import Decimal
# from django.utils.translation import gettext_lazy as _  # For internationalization (optional)
# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Country Name")  # e.g., 'United States', 'Canada'
    iso_code = models.CharField(max_length=5, unique=True, verbose_name="ISO-CODE")  # e.g., 'USA', 'GBR'

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ['name']

    def __str__(self):
        return self.name

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
    supplier_code = models.CharField(max_length=50, primary_key=True, editable=False, verbose_name="Supplier Code")
    name = models.CharField(max_length=255, unique=True, verbose_name="Supplier Name")
    legal_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Legal Name")
    website = models.URLField(blank=True, null=True, verbose_name="Website")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name="Phone")
    street_address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Street Address")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="City")
    state = models.CharField(max_length=100, blank=True, null=True, verbose_name="State/Province")
    postal_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="Postal Code")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Country")
    tax_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tax ID")
    is_manufacturer = models.BooleanField(default=False, verbose_name="Is Manufacturer")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

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

def generate_product_code():
    prefix = ''.join(random.choices(string.ascii_uppercase, k=3))
    mid = ''.join(random.choices(string.digits, k=4))
    end = ''.join(random.choices(string.digits, k=5))
    return f"{prefix}-{mid}-{end}"

class Product(models.Model):
    product_code = models.CharField(max_length=50, primary_key=True, editable=False, verbose_name="Product Code")
    name = models.CharField(max_length=255, verbose_name="Product Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Supplier")
    supplier_product_code = models.CharField(max_length=100, blank=True, null=True, verbose_name="Supplier Product Code")
    manufacturer = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='manufactured_products', verbose_name="Manufacturer")
    manufacturer_product_code = models.CharField(max_length=100, blank=True, null=True, verbose_name="Manufacturer Product Code")
    image = models.ImageField(upload_to='product_images/', blank=True, null=True, verbose_name="Product Image")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], verbose_name="Unit Price")
    quantity_per_unit = models.PositiveIntegerField(default=1, verbose_name="Quantity Per Unit (e.g. per pack)")
    unit = models.CharField(max_length=50, default="pcs", verbose_name="Unit (e.g. pcs, pack, box)")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.product_code:
            for _ in range(10):
                code = generate_product_code()
                if not Product.objects.filter(product_code=code).exists():
                    self.product_code = code
                    break
            else:
                raise ValueError("Could not generate a unique product code after 10 attempts.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.product_code})"

def generate_client_id():
    prefix = ''.join(random.choices(string.ascii_uppercase, k=3))
    mid = ''.join(random.choices(string.digits, k=4))
    end = ''.join(random.choices(string.digits, k=5))
    return f"{prefix}-{mid}-{end}"

class Client(models.Model):
    client_id = models.CharField(max_length=50, primary_key=True, editable=False, verbose_name="Client ID")
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="User Account")
    name = models.CharField(max_length=255, unique=True, verbose_name="Client Name")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name="Phone")
    street_address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Street Address")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="City")
    state = models.CharField(max_length=100, blank=True, null=True, verbose_name="State/Province")
    postal_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="Postal Code")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Country")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Client / Customer"
        verbose_name_plural = "Clients / Customers"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.client_id:
            for _ in range(10):
                code = generate_client_id()
                if not Client.objects.filter(client_id=code).exists():
                    self.client_id = code
                    break
            else:
                raise ValueError("Could not generate a unique client ID after 10 attempts.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Cable(models.Model):
    CABLE_TYPE_CHOICES = [
        ('CAT5', 'Cat 5'),
        ('CAT5E', 'Cat 5e'),
        ('CAT6', 'Cat 6'),
        ('CAT6A', 'Cat 6a'),
        ('CAT7', 'Cat 7'),
        ('CAT8', 'Cat 8'),
        # Add more types as needed
    ]

    name = models.CharField(max_length=100, verbose_name="Cable Name")
    type = models.CharField(max_length=10, choices=CABLE_TYPE_CHOICES, verbose_name="Cable Type")
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name="Product Code")
    color = models.ForeignKey(SystemCoreColourCode, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Color Code")
    gbps = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Speed (Gbps)")
    mbps = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name="Speed (Mbps)")

    class Meta:
        verbose_name = "Cable"
        verbose_name_plural = "Cables"
        ordering = ['name']

    def clean(self):
        # Ensure at least one of gbps or mbps is provided
        if self.gbps is None and self.mbps is None:
            raise ValidationError("You must provide either Gbps or Mbps.")

        # If only one is provided, calculate the other
        if self.gbps is not None and self.mbps is None:
            self.mbps = self.gbps * 1000
        elif self.mbps is not None and self.gbps is None:
            self.gbps = self.mbps / 1000

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.type}) - {self.gbps} Gbps / {self.mbps} Mbps"

class CatRJ45(models.Model):
    RJ45_TYPE_CHOICES = [
        ('FEMALE', 'RJ45 Female'),
        ('MALE', 'RJ45 Male'),
    ]

    type = models.CharField(max_length=6, choices=RJ45_TYPE_CHOICES, verbose_name="Connector Type")
    name = models.CharField(max_length=100, verbose_name="Connector Name")
    pinout = models.ForeignKey(RJ45Pinout, on_delete=models.CASCADE, verbose_name="Pinout")

    class Meta:
        verbose_name = "Cat RJ45 Connector"
        verbose_name_plural = "Cat RJ45 Connectors"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

