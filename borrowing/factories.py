import factory

from borrowing.models import Borrowing


class BorrowingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Borrowing

    expected_return_date = factory.Faker(
        "date_between", start_date="today", end_date="+1d"
    )

    @factory.post_generation
    def books(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for actor in extracted:
                self.books.add(actor)
