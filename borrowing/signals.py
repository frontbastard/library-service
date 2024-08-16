from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingDetailSerializer,
)
from notification.tasks import send_borrowing_creation_notification


@receiver(m2m_changed, sender=Borrowing.books.through)
def check_and_decrement_inventory(sender, instance, action, **kwargs):
    if action == "post_add":
        for book in instance.books.all():
            book.check_inventory()
            book.update_inventory(-1)


@receiver(m2m_changed, sender=Borrowing.books.through)
def notify_books_changed(sender, instance, action, **kwargs):
    if action == "post_add":
        serialized_data = BorrowingDetailSerializer(instance).data
        send_borrowing_creation_notification.delay(serialized_data)
