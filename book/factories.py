import factory

from book.models import Book


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    inventory = 4
    daily_fee = 2
