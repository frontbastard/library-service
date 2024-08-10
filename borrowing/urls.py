from django.urls import path

from borrowing.views import BorrowingListView

urlpatterns = [
    path("borrowings/", BorrowingListView.as_view(), name="borrowing")
]

app_name = "book"

