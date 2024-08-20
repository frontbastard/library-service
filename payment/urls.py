from django.urls import path
from .views import PaymentSuccessView, PaymentCancelView

app_name = "payment"

urlpatterns = [
    path("success/", PaymentSuccessView.as_view(), name="success"),
    path("cancel/", PaymentCancelView.as_view(), name="cancel"),
]
