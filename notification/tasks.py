from celery import shared_task

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
