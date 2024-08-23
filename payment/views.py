from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from borrowing.models import Borrowing
from .models import Payment
from .services import PaymentService


class PaymentSuccessView(APIView):
    def get(self, request, *args, **kwargs):
        session_id = request.query_params.get("session_id")

        if session_id:
            with transaction.atomic():
                payment = PaymentService.process_successful_payment(session_id)
                if payment:
                    borrowing = payment.borrowing
                    borrowing.is_paid = True
                    borrowing.save()

                    return Response(
                        {
                            "message": "Payment successful",
                            "borrowing_id": borrowing.id
                        }
                    )

        return Response(
            {"message": "Payment verification failed"},
            status=status.HTTP_400_BAD_REQUEST
        )


class PaymentCancelView(APIView):
    def get(self, request, *args, **kwargs):
        borrowing_id = request.query_params.get("borrowing_id")

        if borrowing_id:
            with transaction.atomic():
                try:
                    borrowing = Borrowing.objects.get(id=borrowing_id)
                    payment = Payment.objects.filter(
                        borrowing=borrowing,
                        status=Payment.StatusChoices.PENDING
                    ).first()
                    if payment:
                        payment.status = Payment.StatusChoices.PAID
                    return Response(
                        {"message": "Payment cancelled"},
                        status=status.HTTP_200_OK
                    )
                except Borrowing.DoesNotExist:
                    pass

        return Response(
            {"message": "Payment cancellation failed"},
            status=status.HTTP_400_BAD_REQUEST
        )
