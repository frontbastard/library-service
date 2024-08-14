import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from book.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField(blank=False)
    actual_return_date = models.DateField(null=True, blank=True)
    books = models.ManyToManyField(Book, related_name="borrowings")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrowings",
    )

    @staticmethod
    def validate_books_returned(actual_return_date, error_to_raise):
        if actual_return_date is not None:
            raise error_to_raise(
                _("The books have already been returned.")
            )

    @staticmethod
    def validate_actual_return_date(
        actual_return_date,
        borrow_date,
        error_to_raise,
    ):
        if actual_return_date == "":
            actual_return_date = None

        if (
            actual_return_date is not None
            and (actual_return_date < borrow_date
                 or actual_return_date > datetime.date.today())
        ):
            raise error_to_raise(
                _("The actual return date should be "
                  "between the borrow date and today.")
            )

    @staticmethod
    def validate_expected_return_date(
        expected_return_date,
        error_to_raise,
    ):
        if (
            expected_return_date is not None
            and expected_return_date <= datetime.date.today()
        ):
            raise error_to_raise(
                _("The expected return date should "
                  "be longer than the borrow date.")
            )

    def __str__(self):
        return (f"Borrowing by "
                f"{self.user.email} on {self.borrow_date}")

    def clean(self):
        Borrowing.validate_expected_return_date(
            expected_return_date=self.expected_return_date,
            error_to_raise=ValidationError,
        )
        Borrowing.validate_actual_return_date(
            actual_return_date=self.actual_return_date,
            borrow_date=self.borrow_date,
            error_to_raise=ValidationError,
        )

    def save(self, *args, **kwargs):
        self.full_clean()

        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("-borrow_date",)
