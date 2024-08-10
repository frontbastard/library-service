from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from borrowing.models import Borrowing


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

