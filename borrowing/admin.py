from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

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
    actions = ["return_borrowing_action"]

    def get_books(self, obj):
        return ", ".join([book.title for book in obj.books.all()])

    def return_borrowing_action(self, request, queryset):
        for borrowing in queryset:
            borrowing.actual_return_date = None
            borrowing.save()

            for book in borrowing.books.all():
                book.update_inventory(1)

        self.message_user(
            request,
            _("Selected borrowings have been returned.")
        )

    get_books.short_description = _("Books")
    return_borrowing_action.short_description = _("Return selected borrowings")
