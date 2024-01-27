
from django.test import TestCase
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from .models import PaymentRequisite, PaymentRequest


class PaymentAPITests(TestCase):
    def setUp(self):
        call_command('csu')

        self.client = APIClient()
        self.superuser = User.objects.get(email='admin@mail.ru')
        self.client.force_authenticate(user=self.superuser)

        is_superuser = self.superuser.is_superuser

    def test_create_invoice(self):
        url = reverse('payment:create-invoice')
        data = {'payment_type': 'Card', 'amount': 500.00, 'account_type': 'Debit'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(
            PaymentRequest.objects.filter(amount=500.00, requisites__user=self.superuser).exists()
        )

    def test_get_invoice_status(self):
        payment_requisite = PaymentRequisite.objects.create(
            user=self.superuser,
            payment_type='Card',
            account_type='Debit',
            owner_name='John Doe',
            phone_number='1234567890',
            limit=1000.00
        )
        payment_request = PaymentRequest.objects.create(
            amount=500.00,
            status='Pending',
            requisites=payment_requisite,
            user=self.superuser
        )
        url = reverse('payment:get-invoice-status', kwargs={'invoice_id': payment_request.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data.get('amount'), '500.00')
        self.assertEqual(response.data.get('status'), 'Pending')
        self.assertEqual(response.data.get('requisites'), 2)
        self.assertEqual(response.data.get('user'), 2)
