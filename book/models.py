from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "hard", "Hard"
        SOFT = "soft", "Soft"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(
        max_length=10,
        choices=CoverChoices.choices
    )
    inventory = models.IntegerField()
    daily_fee = models.DecimalField(max_digits=6, decimal_places=2)

    def check_inventory(self):
        if self.inventory < 1:
            raise ValidationError(
                _(f"The book '{self.title}' is out of stock.")
            )

    def update_inventory(self, amount):
        self.inventory += amount
        self.save()

    def __str__(self):
        return self.title
