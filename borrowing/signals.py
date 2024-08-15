from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from borrowing.models import Borrowing


@receiver(m2m_changed, sender=Borrowing.books.through)
def check_and_decrement_inventory(sender, instance, action, **kwargs):
    if action == "post_add":
        for book in instance.books.all():
            book.check_inventory()
            book.update_inventory(-1)
