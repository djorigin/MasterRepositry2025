from django.test import TestCase
# GaiaProjectDjango
# systemcore/tests.py
# This file contains tests for the systemcore app in the GaiaProjectDjango project.
# Django imports
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import SystemCoreColourCode
from systemcore.models import (
    Country, Supplier, Product, Client, Cable, SystemCoreColourCode,
    RJ45Pinout, CatRJ45, Terminal, TerminalInput, SystemBuilder,
    SystemBuilderConnection, SystemPurchaseOrder, SystemPurchaseOrderItem,
    SystemClientInvoice, SystemClientInvoiceItem, SystemAccount, SystemAccountTransaction) 
from decimal import Decimal   

# Create your tests here.

class CountryModelTest(TestCase):
    def test_create_country(self):
        country = Country.objects.create(name="Testland", iso_code="TST")
        self.assertEqual(str(country), "Testland")

class SupplierModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Testland", iso_code="TST")

    def test_create_supplier(self):
        supplier = Supplier.objects.create(
            name="Test Supplier", country=self.country
        )
        self.assertTrue(supplier.supplier_code)
        self.assertEqual(str(supplier), "Test Supplier")
class ProductModelTest(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(name="Test Supplier")
    
    def test_create_product(self):
        product = Product.objects.create(
            name="Test Product", supplier=self.supplier, price=Decimal("10.00")
        )
        self.assertTrue(product.product_code)
        self.assertEqual(str(product), f"Test Product ({product.product_code})")

class ClientModelTest(TestCase):
    def test_create_client(self):
        client = Client.objects.create(name="Test Client")
        self.assertTrue(client.client_id)
        self.assertEqual(str(client), "Test Client")
class CableModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Cable Product", price=Decimal("5.00"))
    
    def test_gbps_to_mbps(self):
        cable = Cable.objects.create(name="Test Cable", type="CAT6", product=self.product, gbps=1)
        self.assertEqual(cable.mbps, 1000)

    def test_mbps_to_gbps(self):
        cable = Cable.objects.create(name="Test Cable2", type="CAT6", product=self.product, mbps=2000)
        self.assertEqual(cable.gbps, 2)

class SystemBuilderTest(TestCase):
    def setUp(self):
        self.client = Client.objects.create(name="Test Client")
        self.user = User.objects.create(username="designer")
        self.builder = SystemBuilder.objects.create(client=self.client, designer=self.user)
    
    def test_system_build_number_generated(self):
        self.assertTrue(self.builder.systemBuildNumber)
        self.assertIn("System Build", str(self.builder))

class SystemBuilderConnectionTest(TestCase):
    def setUp(self):
        self.client = Client.objects.create(name="Test Client")
        self.user = User.objects.create(username="designer")
        self.builder = SystemBuilder.objects.create(client=self.client, designer=self.user)
        self.supplier = Supplier.objects.create(name="Test Supplier")
        self.product = Product.objects.create(name="Cable Product", supplier=self.supplier, price=Decimal("5.00"))
        self.cable = Cable.objects.create(name="Test Cable", type="CAT6", product=self.product, gbps=1)
        self.terminal_product = Product.objects.create(name="Terminal Product", supplier=self.supplier, price=Decimal("2.00"))
        self.terminal_a = Terminal.objects.create(name="Terminal A", product=self.terminal_product)
        self.terminal_b = Terminal.objects.create(name="Terminal B", product=self.terminal_product)

    def test_connection_creation(self):
        connection = SystemBuilderConnection.objects.create(
            system_builder=self.builder,
            terminal_a=self.terminal_a,
            terminal_b=self.terminal_b,
            cable=self.cable,
            label="Port 1"
        )
        self.assertTrue(connection.code_sequence)
        self.assertEqual(connection.system_builder, self.builder)
        self.assertEqual(connection.terminal_a, self.terminal_a)
        self.assertEqual(connection.terminal_b, self.terminal_b)
        self.assertEqual(connection.cable, self.cable)
        self.assertEqual(connection.label, "Port 1")
        self.assertIn("Port 1", str(connection))

class PurchaseOrderGenerationTest(TestCase):
    def setUp(self):
        self.client = Client.objects.create(name="Test Client")
        self.user = User.objects.create(username="designer")
        self.supplier = Supplier.objects.create(name="Test Supplier")
        self.product = Product.objects.create(name="Cable Product", supplier=self.supplier, price=Decimal("5.00"))
        self.cable = Cable.objects.create(name="Test Cable", type="CAT6", product=self.product, gbps=1)
        self.terminal_product_a = Product.objects.create(name="Terminal Product A", supplier=self.supplier, price=Decimal("2.00"))
        self.terminal_product_b = Product.objects.create(name="Terminal Product B", supplier=self.supplier, price=Decimal("2.00"))
        self.terminal_a = Terminal.objects.create(name="Terminal A", product=self.terminal_product_a)
        self.terminal_b = Terminal.objects.create(name="Terminal B", product=self.terminal_product_b)
        self.builder = SystemBuilder.objects.create(client=self.client, designer=self.user, is_complete=True)
        self.connection = SystemBuilderConnection.objects.create(
            system_builder=self.builder,
            terminal_a=self.terminal_a,
            terminal_b=self.terminal_b,
            cable=self.cable,
            label="Port 1"
        )

    def test_generate_purchase_order(self):
        po = self.builder.generate_purchase_order(user=self.user)
        self.assertIsNotNone(po)
        self.assertEqual(po.system_builder, self.builder)
        self.assertEqual(po.items.count(), 3)  # 1 cable + 2 terminals
        self.assertAlmostEqual(po.total_price(), Decimal("9.00"))

class InvoiceGenerationTest(TestCase):
    def setUp(self):
        self.client = Client.objects.create(name="Test Client")
        self.user = User.objects.create(username="designer")
        self.supplier = Supplier.objects.create(name="Test Supplier")
        self.product = Product.objects.create(name="Cable Product", supplier=self.supplier, price=Decimal("5.00"))
        self.cable = Cable.objects.create(name="Test Cable", type="CAT6", product=self.product, gbps=1)
        self.terminal_product_a = Product.objects.create(name="Terminal Product A", supplier=self.supplier, price=Decimal("2.00"))
        self.terminal_product_b = Product.objects.create(name="Terminal Product B", supplier=self.supplier, price=Decimal("2.00"))
        self.terminal_a = Terminal.objects.create(name="Terminal A", product=self.terminal_product_a)
        self.terminal_b = Terminal.objects.create(name="Terminal B", product=self.terminal_product_b)
        self.builder = SystemBuilder.objects.create(client=self.client, designer=self.user, is_complete=True)
        self.connection = SystemBuilderConnection.objects.create(
        system_builder=self.builder,
        terminal_a=self.terminal_a,
        terminal_b=self.terminal_b,
        cable=self.cable,
        label="Port 1"
    )
        self.po = self.builder.generate_purchase_order(user=self.user)
    # If using signals, do NOT call generate_client_invoice manually:
        self.po.is_ordered = True
        self.po.save()
        invoice = SystemClientInvoice.objects.get(system_builder=self.builder)
        self.assertIsNotNone(invoice)

def test_generate_invoice(self):
        invoice = self.po.generate_client_invoice(user=self.user)
        self.assertIsNotNone(invoice)
        self.assertEqual(invoice.system_builder, self.builder)
        self.assertEqual(invoice.client, self.client)
        self.assertEqual(invoice.items.count(), 3)  # 1 cable + 2 terminals
        self.assertAlmostEqual(invoice.total_price(), Decimal("9.00"))

class SignalIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client.objects.create(name="Signal Client")
        self.user = User.objects.create(username="signaluser")
        self.supplier = Supplier.objects.create(name="Signal Supplier")
        self.product = Product.objects.create(name="Signal Cable Product", supplier=self.supplier, price=Decimal("5.00"))
        self.cable = Cable.objects.create(name="Signal Cable", type="CAT6", product=self.product, gbps=1)
        self.terminal_product_a = Product.objects.create(name="Signal Terminal Product A", supplier=self.supplier, price=Decimal("2.00"))
        self.terminal_product_b = Product.objects.create(name="Signal Terminal Product B", supplier=self.supplier, price=Decimal("2.00"))
        self.terminal_a = Terminal.objects.create(name="Signal Terminal A", product=self.terminal_product_a)
        self.terminal_b = Terminal.objects.create(name="Signal Terminal B", product=self.terminal_product_b)
        self.builder = SystemBuilder.objects.create(client=self.client, designer=self.user, is_complete=False)
        self.connection = SystemBuilderConnection.objects.create(
            system_builder=self.builder,
            terminal_a=self.terminal_a,
            terminal_b=self.terminal_b,
            cable=self.cable,
            label="Signal Port"
        )

    def test_purchase_order_created_by_signal(self):
        # Mark as complete and save to trigger signal
        self.builder.is_complete = True
        self.builder.save()
        from systemcore.models import SystemPurchaseOrder
        po = SystemPurchaseOrder.objects.get(system_builder=self.builder)
        self.assertIsNotNone(po)
        self.assertEqual(po.system_builder, self.builder)

    def test_invoice_created_by_signal(self):
        # Mark as complete and save to trigger PO creation
        self.builder.is_complete = True
        self.builder.save()
        from systemcore.models import SystemPurchaseOrder, SystemClientInvoice
        po = SystemPurchaseOrder.objects.get(system_builder=self.builder)
        # Mark PO as ordered and save to trigger invoice creation
        po.is_ordered = True
        po.save()
        invoice = SystemClientInvoice.objects.get(system_builder=self.builder)
        self.assertIsNotNone(invoice)
        self.assertEqual(invoice.system_builder, self.builder)



