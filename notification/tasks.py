from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from borrowing.models import Borrowing
from .bot import send_telegram_message_sync


@shared_task
def send_borrowing_creation_notification(borrowing_data):
    books = ", ".join(book["title"] for book in borrowing_data["books"])
    message = f"""
Borrowing Creation with user {borrowing_data["user"]["email"]}
ID: {borrowing_data["id"]}
Borrowing Date: {borrowing_data["borrow_date"]}
Expected Return Date: {borrowing_data["expected_return_date"]}
Books: {books}
"""
    send_telegram_message_sync(message)


@shared_task
def check_overdue_borrowings():
    today = timezone.now().date()

    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lt=today,
        actual_return_date__isnull=True,
    )

    if not overdue_borrowings:
        return send_telegram_message_sync("No borrowings overdue today!")

    message = "Overdue borrowings:\n\n"
    for borrowing in overdue_borrowings:
        message += (
            f"User: {borrowing.user.get_full_name() or borrowing.user.email}\n"
            f"Books: {', '.join(book.title for book in borrowing.books.all())}\n"
            f"Borrow date: {borrowing.borrow_date}\n"
            f"Expected return date: {borrowing.expected_return_date}\n"
            f"Days overdue: {(today - borrowing.expected_return_date).days}\n"
            f"{'-' * 10}\n"
        )

    send_telegram_message_sync(message)
