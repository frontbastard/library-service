from rest_framework import generics

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingListSerializer,
    BorrowingSerializer,
    BorrowingDetailSerializer,
)


class BorrowingListView(generics.ListCreateAPIView):
    model = Borrowing
    serializer_class = BorrowingSerializer
    queryset = Borrowing.objects.all()

    SERIALIZER_MAP = {
        "GET": BorrowingListSerializer,
        "POST": BorrowingSerializer,
    }

    @staticmethod
    def _params_to_ints(query_string):
        """
        Converts a string of format '1,3,4' to a list of integers [1,2,3].
        """
        return [int(str_id) for str_id in query_string.split(",")]

    def get_serializer_class(self):
        return self.SERIALIZER_MAP.get(
            self.request.method,
            self.serializer_class
        )

    def get_queryset(self):
        queryset = (self
                    .queryset.select_related("user")
                    .prefetch_related("books"))
        is_active = self.request.query_params.get("is_active", False)
        user_ids = self.request.query_params.get("user_ids", False)

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        if user_ids:
            user_ids = self._params_to_ints(user_ids)
            queryset = queryset.filter(user__id__in=user_ids)

        if is_active:
            is_active = is_active.lower() == "true"
            queryset = queryset.filter(actual_return_date__isnull=is_active)

        return queryset


class BorrowingDetailView(generics.RetrieveUpdateAPIView):
    model = Borrowing
    serializer_class = BorrowingDetailSerializer
    queryset = Borrowing.objects.all()

    SERIALIZER_MAP = {
        "GET": BorrowingListSerializer,
        "PUT": BorrowingSerializer,
        "PATCH": BorrowingSerializer,
    }

    def get_serializer_class(self):
        return self.SERIALIZER_MAP.get(
            self.request.method,
            self.serializer_class
        )

    def get_queryset(self):
        queryset = self.queryset

        if self.request.method == "GET":
            queryset = (queryset
                        .select_related("user")
                        .prefetch_related("books"))

        return queryset
