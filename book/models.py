from django.db import models


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

    def __str__(self):
        return self.title
