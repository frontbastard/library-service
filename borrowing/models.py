import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from book.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    books = models.ManyToManyField(Book, related_name="borrowings")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrowings",
    )

    def __str__(self):
        return (f"Borrowing by "
                f"{self.user.email} on {self.borrow_date}")


    def clean(self):
        if self.borrow_date is None:
            self.borrow_date = self.borrow_date or datetime.date.today()

        if self.expected_return_date <= self.borrow_date:
            raise ValidationError(
                _("Expected return date must be tomorrow or later.")
            )

        if (self.actual_return_date and
                self.actual_return_date < self.borrow_date):
            raise ValidationError(
                _("Actual return date cannot be before borrow date.")
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-borrow_date",)
