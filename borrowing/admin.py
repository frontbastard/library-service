from django.contrib import admin

from borrowing.models import Borrowing


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "borrow_date",
        "expected_return_date",
        "actual_return_date",
        "get_books",
    )

    def get_books(self, obj):
        return ", ".join([book.title for book in obj.books.all()])

    get_books.short_description = "Books"
