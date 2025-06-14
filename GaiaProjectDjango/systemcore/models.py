# GaiaProjectDjango
# systemcore/models.py
# Django imports
from django.db import models, transaction, IntegrityError
from django.core.validators import RegexValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string
from decimal import Decimal
from django.urls import reverse
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
        validators=[rgb_validator],
        verbose_name="RGB Value",
        help_text="Enter a valid RGB value in the format 'R,G,B' (e.g., '255,255,255')."
    )  # e.g., '255,255,255' for white

    hex_validator = RegexValidator(
        regex=r'^#[0-9A-Fa-f]{6}$',
        message="Enter a valid hex color code (e.g., '#FFFFFF')."
    )
    hex_code = models.CharField(
        max_length=7,
        validators=[hex_validator],
        unique=True,
        verbose_name="Hex Code",
        help_text="Enter a valid hex color code (e.g., '#FFFFFF')."
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
    name = models.CharField(max_length=100, unique=True)  # e.g., "T568A"
    image = models.ImageField(upload_to='rj45pinout_images/', blank=True, null=True, verbose_name="Pinout Image")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    standards = models.CharField(max_length=255, blank=True, null=True, verbose_name="Standards")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "RJ45 Pinout"
        verbose_name_plural = "RJ45 Pinouts"
        ordering = ['name']

    def __str__(self):
        return self.name

class RJ45Pin(models.Model):
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

    pinout = models.ForeignKey(RJ45Pinout, on_delete=models.CASCADE, related_name='pins', verbose_name="Pinout")
    pin_number = models.PositiveSmallIntegerField()  # 1 to 8
    color_code = models.CharField(max_length=20, choices=COLOR_CHOICES)

    class Meta:
        unique_together = (('pinout', 'pin_number'),)
        ordering = ['pinout', 'pin_number']
        verbose_name = "RJ45 Pin"
        verbose_name_plural = "RJ45 Pins"

    def __str__(self):
        return f"{self.pinout.name} - Pin {self.pin_number}: {self.color_code}"
    
 

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
    def get_absolute_url(self):
        return reverse('systemcore:supplier_detail', kwargs={'pk': self.supplier_code})

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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product Code")
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

class Terminal(models.Model):
    name = models.CharField(max_length=100, verbose_name="Terminal Name")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product Code")

    class Meta:
        verbose_name = "Terminal"
        verbose_name_plural = "Terminals"
        ordering = ['name']

    def __str__(self):
        return self.name

class TerminalInput(models.Model):
    terminal = models.ForeignKey(Terminal, on_delete=models.CASCADE, related_name='inputs', verbose_name="Terminal")
    input_number = models.PositiveSmallIntegerField(verbose_name="Input Number")  # 1 to 48
    catrj45 = models.ForeignKey(CatRJ45, on_delete=models.CASCADE, verbose_name="RJ45 Connector")

    class Meta:
        verbose_name = "Terminal Input"
        verbose_name_plural = "Terminal Inputs"
        ordering = ['terminal', 'input_number']
        unique_together = ('terminal', 'input_number')  # Prevent duplicate input numbers per terminal

    def __str__(self):
        return f"{self.terminal.name} - Input {self.input_number}: {self.catrj45.name}"

def generate_system_build_number():
    prefix = ''.join(random.choices(string.ascii_uppercase, k=3))
    mid = ''.join(random.choices(string.digits, k=4))
    end = ''.join(random.choices(string.digits, k=5))
    return f"{prefix}-{mid}-{end}"

def generate_code_sequence():
    part1 = ''.join(random.choices(string.digits, k=3))
    part2 = ''.join(random.choices(string.digits, k=3))
    return f"{part1}-{part2}"

class SystemBuilder(models.Model):
    systemBuildNumber = models.CharField(max_length=50, primary_key=True, editable=False, verbose_name="System Build Number")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    date_created = models.DateTimeField(default=timezone.now, verbose_name="Date Created")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    is_complete = models.BooleanField(default=False, verbose_name="Is Complete")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    designer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Designer")

    class Meta:
        verbose_name = "System Build"
        verbose_name_plural = "System Builds"
        ordering = ['-date_created']

    def save(self, *args, **kwargs):
        if not self.systemBuildNumber:
            for _ in range(10):
                code = generate_system_build_number()
                if not SystemBuilder.objects.filter(systemBuildNumber=code).exists():
                    self.systemBuildNumber = code
                    break
            else:
                raise ValueError("Could not generate a unique system build number after 10 attempts.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"System Build {self.systemBuildNumber} for {self.client.name}"

    def generate_purchase_order(self, user=None):
        if not self.is_complete:
            raise ValueError("System build must be marked as complete before generating a purchase order.")
        if hasattr(self, 'systempurchaseorder'):
            raise ValueError("Purchase order already exists for this build.")

        po = SystemPurchaseOrder.objects.create(
            system_builder=self,
            created_by=user
        )
        for conn in self.connections.all():
            # Add cable
            SystemPurchaseOrderItem.objects.create(
                purchase_order=po,
                product=conn.cable.product,
                supplier=conn.cable.product.supplier,
                amount=1,
                unit_price=conn.cable.product.price,
                cable_length=getattr(conn, 'cable_length', None),  # If you add this field
                description=f"Cable for {conn.label}"
            )
            # Add terminals
            for terminal in [conn.terminal_a, conn.terminal_b]:
                SystemPurchaseOrderItem.objects.create(
                    purchase_order=po,
                    product=terminal.product,
                    supplier=terminal.product.supplier,
                    amount=1,
                    unit_price=terminal.product.price,
                    description=f"Terminal for {conn.label}"
                )
        return po

class SystemBuilderConnection(models.Model):
    system_builder = models.ForeignKey(SystemBuilder, on_delete=models.CASCADE, related_name='connections', verbose_name="System Build")
    code_sequence = models.CharField(max_length=7, verbose_name="Connection Code Sequence")  # e.g., 123-456
    terminal_a = models.ForeignKey(Terminal, on_delete=models.CASCADE, related_name='terminal_a_connections', verbose_name="Terminal A")
    terminal_b = models.ForeignKey(Terminal, on_delete=models.CASCADE, related_name='terminal_b_connections', verbose_name="Terminal B")
    cable = models.ForeignKey(Cable, on_delete=models.CASCADE, verbose_name="Cable")
    label = models.CharField(max_length=100, verbose_name="Label (e.g. TV, Port 1)")

    class Meta:
        verbose_name = "System Build Connection"
        verbose_name_plural = "System Build Connections"
        unique_together = ('system_builder', 'code_sequence')  # Unique per build

    def save(self, *args, **kwargs):
        if not self.code_sequence:
            for _ in range(10):
                code = generate_code_sequence()
                if not SystemBuilderConnection.objects.filter(system_builder=self.system_builder, code_sequence=code).exists():
                    self.code_sequence = code
                    break
            else:
                raise ValueError("Could not generate a unique code sequence for this build after 10 attempts.")
        super().save(*args, **kwargs)

    def clean(self):
        # Ensure a cable always has two terminals
        if not self.terminal_a or not self.terminal_b:
            raise ValidationError("Each cable must have two terminal points.")

    def __str__(self):
        return f"{self.label} ({self.code_sequence}) in {self.system_builder}"

def generate_purchase_order_number():
    prefix = ''.join(random.choices(string.ascii_uppercase, k=3))
    mid = ''.join(random.choices(string.digits, k=4))
    end = ''.join(random.choices(string.digits, k=5))
    return f"{prefix}-{mid}-{end}"

class SystemPurchaseOrder(models.Model):
    purchase_order_number = models.CharField(max_length=50, primary_key=True, editable=False, verbose_name="Purchase Order Number")
    system_builder = models.OneToOneField(SystemBuilder, on_delete=models.CASCADE, verbose_name="System Build")
    date_created = models.DateTimeField(default=timezone.now, verbose_name="Date Created")
    is_ordered = models.BooleanField(default=False, verbose_name="Is Ordered")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Created By")

    class Meta:
        verbose_name = "System Purchase Order"
        verbose_name_plural = "System Purchase Orders"
        ordering = ['-date_created']

    def save(self, *args, **kwargs):
        if not self.purchase_order_number:
            for _ in range(10):
                code = generate_purchase_order_number()
                if not SystemPurchaseOrder.objects.filter(purchase_order_number=code).exists():
                    self.purchase_order_number = code
                    break
            else:
                raise ValueError("Could not generate a unique purchase order number after 10 attempts.")
        super().save(*args, **kwargs)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"PO {self.purchase_order_number} for {self.system_builder}"
    def generate_client_invoice(self, user=None):
        if not self.is_ordered:
            raise ValueError("Purchase order must be marked as ordered before generating an invoice.")
        if SystemClientInvoice.objects.filter(system_builder=self.system_builder).exists():
            raise ValueError("Invoice already exists for this purchase order.")

        invoice = SystemClientInvoice.objects.create(
            client=self.system_builder.client,
            system_builder=self.system_builder,
            created_by=user
        )
        for item in self.items.all():
            SystemClientInvoiceItem.objects.create(
                invoice=invoice,
                product=item.product,
                amount=item.amount,
                unit_price=item.unit_price,
                description=item.description,
                cable_length=item.cable_length
            )
        return invoice

class SystemPurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(SystemPurchaseOrder, on_delete=models.CASCADE, related_name='items', verbose_name="Purchase Order")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Supplier")
    amount = models.PositiveIntegerField(default=1, verbose_name="Amount")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Unit Price")
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total Price")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="Description")
    # For cables, store length (meters)
    cable_length = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name="Cable Length (m)")

    class Meta:
        verbose_name = "System Purchase Order Item"
        verbose_name_plural = "System Purchase Order Items"

    def save(self, *args, **kwargs):
        # Calculate total price
        if self.cable_length and self.product.unit == 'meter':
            self.total = self.unit_price * self.cable_length * self.amount
        else:
            self.total = self.unit_price * self.amount
        super().save(*args, **kwargs)

    def total_price(self):
        return self.total

    def __str__(self):
        return f"{self.product.name} x{self.amount} ({self.purchase_order})"

def generate_invoice_number():
    prefix = ''.join(random.choices(string.ascii_uppercase, k=3))
    mid = ''.join(random.choices(string.digits, k=4))
    end = ''.join(random.choices(string.digits, k=5))
    return f"{prefix}-{mid}-{end}"

class SystemClientInvoice(models.Model):
    invoice_number = models.CharField(max_length=50, primary_key=True, editable=False, verbose_name="Invoice Number")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    system_builder = models.OneToOneField(SystemBuilder, on_delete=models.CASCADE, verbose_name="System Build")
    date_created = models.DateTimeField(default=timezone.now, verbose_name="Date Created")
    is_sent = models.BooleanField(default=False, verbose_name="Is Sent")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Created By")

    class Meta:
        verbose_name = "System Client Invoice"
        verbose_name_plural = "System Client Invoices"
        ordering = ['-date_created']

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            for _ in range(10):
                code = generate_invoice_number()
                if not SystemClientInvoice.objects.filter(invoice_number=code).exists():
                    self.invoice_number = code
                    break
            else:
                raise ValueError("Could not generate a unique invoice number after 10 attempts.")
        super().save(*args, **kwargs)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Invoice {self.invoice_number} for {self.client.name}"
    
    def generate_client_invoice(self, user=None):
        if not self.is_ordered:
            raise ValueError("Purchase order must be marked as ordered before generating an invoice.")
        if SystemClientInvoice.objects.filter(system_builder=self.system_builder).exists():
           raise ValueError("Invoice already exists for this purchase order.")

        invoice = SystemClientInvoice.objects.create(
            client=self.system_builder.client,
            system_builder=self.system_builder,
            created_by=user
        )
        for item in self.items.all():
            SystemClientInvoiceItem.objects.create(
                invoice=invoice,
                product=item.product,
                amount=item.amount,
                unit_price=item.unit_price,
                description=item.description,
                cable_length=item.cable_length
            )
        return invoice

class SystemClientInvoiceItem(models.Model):
    invoice = models.ForeignKey(SystemClientInvoice, on_delete=models.CASCADE, related_name='items', verbose_name="Invoice")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    amount = models.PositiveIntegerField(default=1, verbose_name="Amount")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Unit Price")
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total Price")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="Description")
    cable_length = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name="Cable Length (m)")

    class Meta:
        verbose_name = "System Client Invoice Item"
        verbose_name_plural = "System Client Invoice Items"

    def save(self, *args, **kwargs):
        if self.cable_length and self.product.unit == 'meter':
            self.total = self.unit_price * self.cable_length * self.amount
        else:
            self.total = self.unit_price * self.amount
        super().save(*args, **kwargs)

    def total_price(self):
        return self.total

    def __str__(self):
        return f"{self.product.name} x{self.amount} ({self.invoice})"

class SystemAccount(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Account Name")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "System Account"
        verbose_name_plural = "System Accounts"

    def __str__(self):
        return self.name

    def balance(self):
        # Sum of all credits minus all debits
        credits = self.transactions.filter(type__in=['INVOICE_PAYMENT', 'CREDIT']).aggregate(total=models.Sum('amount'))['total'] or 0
        debits = self.transactions.filter(type__in=['PURCHASE_ORDER_PAYMENT', 'BILL']).aggregate(total=models.Sum('amount'))['total'] or 0
        return credits - debits

TRANSACTION_TYPE_CHOICES = [
    ('INVOICE_PAYMENT', 'Invoice Payment (Money In)'),
    ('PURCHASE_ORDER_PAYMENT', 'Purchase Order Payment (Money Out)'),
    ('BILL', 'Bill (Money Out)'),
    ('CREDIT', 'Credit (Money In)'),
    # Add more as needed
]

class SystemAccountTransaction(models.Model):
    account = models.ForeignKey(SystemAccount, on_delete=models.CASCADE, related_name='transactions', verbose_name="Account")
    type = models.CharField(max_length=32, choices=TRANSACTION_TYPE_CHOICES, verbose_name="Transaction Type")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Amount")
    date = models.DateTimeField(default=timezone.now, verbose_name="Date")
    related_invoice = models.ForeignKey(SystemClientInvoice, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Related Invoice")
    related_purchase_order = models.ForeignKey(SystemPurchaseOrder, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Related Purchase Order")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="Description")

    class Meta:
        verbose_name = "System Account Transaction"
        verbose_name_plural = "System Account Transactions"
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_type_display()} - {self.amount} on {self.date.date()}"

# Optionally, you can add models for Bills and Credits if you want to store more details:
class SystemBill(models.Model):
    account = models.ForeignKey(SystemAccount, on_delete=models.CASCADE, related_name='bills', verbose_name="Account")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Amount")
    date = models.DateTimeField(default=timezone.now, verbose_name="Date")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="Description")
    is_paid = models.BooleanField(default=False, verbose_name="Is Paid")

    class Meta:
        verbose_name = "System Bill"
        verbose_name_plural = "System Bills"

    def __str__(self):
        return f"Bill {self.amount} on {self.date.date()}"

class SystemCredit(models.Model):
    account = models.ForeignKey(SystemAccount, on_delete=models.CASCADE, related_name='credits', verbose_name="Account")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Amount")
    date = models.DateTimeField(default=timezone.now, verbose_name="Date")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="Description")
    is_used = models.BooleanField(default=False, verbose_name="Is Used")

    class Meta:
        verbose_name = "System Credit"
        verbose_name_plural = "System Credits"

    def __str__(self):
        return f"Credit {self.amount} on {self.date.date()}"



