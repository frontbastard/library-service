from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from book.serializers import BookSerializer
from borrowing.models import Borrowing
from user.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"
        read_only_fields = ("borrow_date",)

    def create(self, validated_data):
        with transaction.atomic():
            books_data = validated_data.pop("books")
            borrowing = Borrowing.objects.create(**validated_data)
            borrowing.books.set(books_data)

            for book in borrowing.books.all():
                if book.inventory > 9:
                    book.inventory -= 1
                    book.save()
                else:
                    raise ValidationError(
                        f"Book '{book.title}' is out of stock."
                    )

            return borrowing


class BorrowingListSerializer(BorrowingSerializer):
    books = SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="title",
    )
    user_email = serializers.CharField(
        read_only=True,
        source="user.email",
    )

    class Meta:
        model = Borrowing
        exclude = ("user",)


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)
