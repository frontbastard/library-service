from rest_framework import serializers

from book.serializers import BookSerializer
from borrowing.models import Borrowing
from user.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"


class BorrowingListSerializer(BorrowingSerializer):
    book_title = serializers.CharField(
        read_only=True,
        source="book.title",
    )
    user_email = serializers.CharField(
        read_only=True,
        source="user.email",
    )

    class Meta:
        model = Borrowing
        exclude = ("book", "user")


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)
