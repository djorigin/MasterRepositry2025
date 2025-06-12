from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SystemBuilder, SystemPurchaseOrder, SystemAccount, SystemAccountTransaction, SystemClientInvoice

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
            
@receiver(post_save, sender=SystemPurchaseOrder)
def create_account_transaction_on_ordered(sender, instance, created, **kwargs):
    if not created and instance.is_ordered:
        # Only create if not already present
        account = SystemAccount.objects.first()  # Or select the appropriate account
        if account and not SystemAccountTransaction.objects.filter(
            related_purchase_order=instance, type='PURCHASE_ORDER_PAYMENT'
        ).exists():
            SystemAccountTransaction.objects.create(
                account=account,
                type='PURCHASE_ORDER_PAYMENT',
                amount=instance.total_price(),
                related_purchase_order=instance,
                description=f"Payment for PO {instance.purchase_order_number}"
            )
@receiver(post_save, sender=SystemClientInvoice)
def create_account_transaction_on_invoice_sent(sender, instance, created, **kwargs):
    if not created and instance.is_sent:
        account = SystemAccount.objects.first()  # Or select the appropriate account
        if account and not SystemAccountTransaction.objects.filter(
            related_invoice=instance, type='INVOICE_PAYMENT'
        ).exists():
            SystemAccountTransaction.objects.create(
                account=account,
                type='INVOICE_PAYMENT',
                amount=instance.total_price(),
                related_invoice=instance,
                description=f"Payment received for Invoice {instance.invoice_number}"
            )