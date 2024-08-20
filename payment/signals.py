from django.db.models.signals import post_save
from django.dispatch import receiver

from borrowing.serializers import BorrowingDetailSerializer
from notification.tasks import send_borrowing_creation_notification
from payment.models import Payment


@receiver(post_save, sender=Payment)
def notify_about_new_borrowing(sender, instance, created, **kwargs):
    if instance.status == Payment.StatusChoices.PAID:
        serialized_data = BorrowingDetailSerializer(instance.borrowing).data
        send_borrowing_creation_notification.delay(serialized_data)
