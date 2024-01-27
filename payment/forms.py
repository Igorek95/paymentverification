from django import forms

from .models import PaymentRequisite, PaymentRequest


class PaymentRequisiteForm(forms.ModelForm):
    class Meta:
        model = PaymentRequisite
        fields = ['payment_type', 'account_type', 'owner_name', 'phone_number', 'limit', 'user']


class PaymentRequestForm(forms.ModelForm):
    class Meta:
        model = PaymentRequest
        fields = ['amount', 'status', 'requisites', 'user']
