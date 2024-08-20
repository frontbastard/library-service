from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from book.serializers import BookSerializer
from borrowing.models import Borrowing
from user.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    regular_sum = serializers.SerializerMethodField()
    fine_sum = serializers.SerializerMethodField()

    def get_regular_sum(self, obj):
        return obj.regular_sum

    def get_fine_sum(self, obj):
        return obj.fine_sum

    def validate_books(self, books):
        if self.instance is None:
            for book in books:
                book.check_inventory()
        return books

    class Meta:
        model = Borrowing
        fields = "__all__"
        read_only_fields = (
            "borrow_date",
            "actual_return_date",
            "regular_sum",
            "fine_sum"
        )


class BorrowingCreateSerializer(BorrowingSerializer):
    def validate(self, attrs):
        Borrowing.validate_expected_return_date(
            expected_return_date=attrs.get("expected_return_date", None),
            error_to_raise=serializers.ValidationError
        )
        return attrs


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
    books = BookSerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True)


class BorrowingReturnSerializer(BorrowingDetailSerializer):
    user_email = serializers.CharField(read_only=True, source="user.email")
    books = serializers.SerializerMethodField()
    actual_return_date = serializers.DateField(required=True)

    def get_books(self, obj):
        return [book.title for book in obj.books.all()]

    def validate(self, attrs):
        Borrowing.validate_actual_return_date(
            actual_return_date=attrs.get("actual_return_date", None),
            borrow_date=self.instance.borrow_date,
            error_to_raise=serializers.ValidationError,
        )
        Borrowing.validate_books_returned(
            actual_return_date=self.instance.actual_return_date,
            error_to_raise=serializers.ValidationError,
        )
        return attrs

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "user_email",
            "books",
        )
        read_only_fields = ("books", "borrow_date", "expected_return_date")
