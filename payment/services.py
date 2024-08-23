import stripe
from django.db import transaction
from django.urls import reverse

from borrowing.models import Borrowing
from library_service import settings
from .models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentService:
    @staticmethod
    def create_checkout_session(
        request,
        borrowing,
        payment_type=Payment.TypeChoices.PAYMENT,
        money_to_pay=None
    ):
        if money_to_pay is None:
            money_to_pay = borrowing.regular_sum

        with transaction.atomic():
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(borrowing.regular_sum * 100),
                        "product_data": {
                            "name": f"Payment for Borrowing #{borrowing.id}",
                        },
                    },
                    "quantity": 1,
                }],
                mode="payment",
                success_url=(
                    request.build_absolute_uri(reverse("payment:success"))
                    + (
                        f"?session_id={{CHECKOUT_SESSION_ID}}"
                        f"&borrowing_id={borrowing.id}"
                    )
                ),
                cancel_url=request.build_absolute_uri(
                    reverse("payment:cancel")
                ) + f"?borrowing_id={borrowing.id}",
                client_reference_id=str(borrowing.id),
            )

            payment = Payment.objects.create(
                status=Payment.StatusChoices.PENDING,
                type=payment_type,
                borrowing=borrowing,
                session_url=checkout_session.url,
                session_id=checkout_session.id,
                money_to_pay=money_to_pay
            )

        return payment

    @staticmethod
    def process_successful_payment(session_id):
        with transaction.atomic():
            try:
                payment = Payment.objects.get(session_id=session_id)
                session = stripe.checkout.Session.retrieve(session_id)

                if session.payment_status == "paid":
                    payment.status = Payment.StatusChoices.PAID
                    payment.save()

                    return payment
            except Payment.DoesNotExist:
                pass

        return None
