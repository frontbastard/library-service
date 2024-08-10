from django.urls import path

from borrowing.views import BorrowingListView, BorrowingDetailView

urlpatterns = [
    path("borrowings/", BorrowingListView.as_view(), name="borrowing_list"),
    path(
        "borrowings/<int:pk>/",
        BorrowingDetailView.as_view(),
        name="borrowing_detail",
    ),
]

app_name = "book"
