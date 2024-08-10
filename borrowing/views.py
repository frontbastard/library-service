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

    def get_serializer_class(self):
        return self.SERIALIZER_MAP.get(
            self.request.method,
            self.serializer_class
        )

    def get_queryset(self):
        if self.request.method == "GET":
            return self.queryset.select_related("book", "user")

        return self.queryset


class BorrowingDetailView(generics.RetrieveAPIView):
    model = Borrowing
    serializer_class = BorrowingDetailSerializer
    queryset = Borrowing.objects.all()
