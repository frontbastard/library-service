from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingListSerializer,
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingReturnSerializer,
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()

    SERIALIZER_MAP = {
        "list": BorrowingListSerializer,
        "create": BorrowingSerializer,
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

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

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
        borrowing.actual_return_date = request.data.get(
            "actual_return_date", None
        )
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
