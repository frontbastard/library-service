from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from borrowing.factories import BorrowingFactory
from borrowing.models import Borrowing
from borrowing.serializers import BorrowingListSerializer
from user.factories import UserFactory

BORROWING_URL = reverse("borrowing:borrowing-list")


class UnauthorizedBorrowingTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_authentication_is_required(self):
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthorizedBorrowingTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(self.user)

    def test_borrowings_list(self):
        BorrowingFactory(user=self.user)

        res = self.client.get(BORROWING_URL)
        borrowings = Borrowing.objects.all()
        serializer = BorrowingListSerializer(borrowings, many=True)

        self.assertEqual(res.data["results"], serializer.data)
