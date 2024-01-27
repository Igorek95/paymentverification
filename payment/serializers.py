from rest_framework import serializers

from payment.models import PaymentRequisite, PaymentRequest


class PaymentRequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRequisite
        fields = ['payment_type', 'owner_name', 'phone_number', 'limit', 'user']


class PaymentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRequest
        fields = ['amount', 'status', 'requisites', 'user']
