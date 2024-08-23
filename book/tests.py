from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from book.factories import BookFactory
from book.models import Book
from book.serializers import BookSerializer
from user.factories import UserFactory

BOOK_URL = reverse("book:book-list")


class UnauthorizedBookTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_authentication_is_required(self):
        res = self.client.get(BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class AuthorizedBookTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(self.user)

    def test_books_list(self):
        BookFactory()

        res = self.client.get(BOOK_URL)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        self.assertEqual(res.data["results"], serializer.data)
