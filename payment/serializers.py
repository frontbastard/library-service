from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "amount",
            "status",
            "stripe_payment_intent_id",
            "created_at",
            "updated_at"
        ]
        read_only_fields = [
            "id",
            "user",
            "status",
            "stripe_payment_intent_id",
            "created_at",
            "updated_at"
        ]


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["amount"]


class PaymentStatusSerializer(serializers.Serializer):
    message = serializers.CharField()
