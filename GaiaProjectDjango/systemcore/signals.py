from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SystemBuilder, SystemPurchaseOrder

@receiver(post_save, sender=SystemBuilder)
def create_purchase_order_on_complete(sender, instance, created, **kwargs):
    # Only act if not just created, but updated
    if not created and instance.is_complete:
        # Only create if not already present
        if not hasattr(instance, 'systempurchaseorder'):
            try:
                instance.generate_purchase_order()
            except Exception as e:
                # Optionally log or handle errors
                pass
@receiver(post_save, sender=SystemPurchaseOrder)
def create_client_invoice_on_ordered(sender, instance, created, **kwargs):
    if not created and instance.is_ordered:
        # Only create if not already present
        if not hasattr(instance, 'systemclientinvoice'):
            try:
                instance.generate_client_invoice()
            except Exception:
                pass  # Optionally log or handle errors