from django.db import transaction
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingListSerializer,
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingReturnSerializer,
    BorrowingCreateSerializer,
)
from payment.models import Payment
from payment.services import PaymentService


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    permission_classes = [IsAuthenticated]

    SERIALIZER_MAP = {
        "list": BorrowingListSerializer,
        "create": BorrowingCreateSerializer,
        "retrieve": BorrowingDetailSerializer,
        "update": BorrowingSerializer,
        "partial_update": BorrowingSerializer,
        "return_borrowing": BorrowingReturnSerializer,
    }

    def get_serializer_class(self):
        return self.SERIALIZER_MAP.get(self.action, BorrowingSerializer)

    def get_queryset(self):
        queryset = self.queryset
        is_active = self.request.query_params.get("is_active", False)
        user_ids = self.request.query_params.get("user_ids", False)

        if self.request.user.is_authenticated:
            if not self.request.user.is_staff:
                queryset = queryset.filter(user=self.request.user)
        else:
            return Borrowing.objects.none()

        if user_ids:
            user_ids = [int(str_id) for str_id in user_ids.split(",")]
            queryset = queryset.filter(user__id__in=user_ids)

        if is_active:
            is_active = is_active.lower() == "true"
            queryset = queryset.filter(actual_return_date__isnull=is_active)

        if self.action in ("list", "retrieve"):
            queryset = (queryset
                        .select_related("user")
                        .prefetch_related("books"))

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        borrowing = serializer.save()

        payment = PaymentService.create_checkout_session(request, borrowing)

        return Response(
            {"checkout_url": payment.session_url},
            status=status.HTTP_303_SEE_OTHER
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "user_ids",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by user id (ex. ?user_ids=2,5)",
            ),
            OpenApiParameter(
                "is_active",
                type=OpenApiTypes.BOOL,
                description="Filter by active status (ex. ?is_active=fiction)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get list of all borrowings"""
        return super().list(request, *args, **kwargs)

    @action(
        detail=True,
        methods=["POST"],
        url_path="return",
        permission_classes=[permissions.IsAdminUser],
    )
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()
        serializer = self.get_serializer(
            borrowing,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            borrowing.actual_return_date = request.data.get(
                "actual_return_date"
            )

            if borrowing.actual_return_date:
                try:
                    payment = PaymentService.create_checkout_session(
                        request,
                        borrowing,
                        payment_type=Payment.TypeChoices.FINE,
                        money_to_pay=borrowing.fine_sum
                    )
                except Exception as e:
                    return Response(
                        {"message": f"Failed to create payment: {str(e)}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                return Response(
                    {
                        "checkout_url": payment.session_url
                    }, status=status.HTTP_200_OK
                )

            serializer.save()

            try:
                for book in borrowing.books.all():
                    book.update_inventory(1)
            except Exception as e:
                return Response(
                    {"message": f"Failed to update inventory: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            {
                "message": "Borrowing returned successfully.",
                "data": serializer.data,
            }, status=status.HTTP_200_OK
        )
