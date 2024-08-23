from decimal import Decimal

import factory

from borrowing.factories import BorrowingFactory
from payment.models import Payment


class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    status = Payment.StatusChoices.PENDING
    type = Payment.TypeChoices.PAYMENT  # noqa: VNE003
    borrowing = factory.SubFactory(BorrowingFactory)
    session_url = factory.Faker("url")
    session_id = factory.Faker("uuid4")
    money_to_pay = factory.Faker(
        "pydecimal",
        left_digits=8,
        right_digits=2,
        positive=True,
        min_value=Decimal("0.01"),
    )
