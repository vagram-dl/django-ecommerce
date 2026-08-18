import uuid

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APITestCase,APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from store.models import Wallet, Payment
from store.services import PaymentService

class PaymentServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',password='testpass123')
        self.wallet = Wallet.objects.create(user=self.user, balance=1000)
        self.idempotency_key = uuid.uuid4()

    def test_deposit_increases_balance(self):
        payment = PaymentService.process_transaction(
            user=self.user, amount=500, payment_type=Payment.Type.DEPOSIT,
            idempotency_key=self.idempotency_key
        )

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 1500)
        self.assertEqual(payment.status, Payment.Status.SUCCESS)
        self.assertEqual(payment.type, Payment.Type.DEPOSIT)

    def test_withdrawal_decreases_balance(self):
        payment = PaymentService.process_transaction(
            user=self.user, amount=300, payment_type=Payment.Type.WITHDRAWAL,
            idempotency_key=self.idempotency_key
        )

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 700)
        self.assertEqual(payment.status, Payment.Status.SUCCESS)

    def test_withdrawal_insufficient_funds(self):
        with self.assertRaises(ValidationError) as context:
            PaymentService.process_transaction(
                user=self.user, amount=2000.00, payment_type=Payment.Type.WITHDRAWAL,
                idempotency_key=self.idempotency_key
            )

        self.assertIn("Недостаточно средств", str(context.exception))

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 1000)

        failed_payment = Payment.objects.filter(idempotency_key=self.idempotency_key).first()
        self.assertIsNotNone(failed_payment)
        self.assertEqual(failed_payment.status, Payment.Status.FAILED)

    def test_idempotency_prevents_double_charge(self):
        key = uuid.uuid4()

        payment1 = PaymentService.process_transaction(
            user=self.user, amount=500, payment_type=Payment.Type.DEPOSIT,
            idempotency_key=key
        )

        payment2 = PaymentService.process_transaction(
            user=self.user, amount=500, payment_type=Payment.Type.DEPOSIT,
            idempotency_key=key
        )

        self.assertEqual(payment1.id, payment2.id)

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 1500)

class PaymentAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='apiuser',password='apipass123')
        self.wallet = Wallet.objects.create(user=self.user,balance=5000)

        self.refresh = RefreshToken.for_user(self.user)
        self.client=APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')

        self.payment_url = reverse('payment-api')
        self.balance_url = reverse('wallet-balance')
        self.history_url = reverse('payment-history')

    def test_api_deposit_success(self):
        data = {
            "amount" : "1000",
            "type" : "deposit"
        }
        response = self.client.post(self.payment_url, data,format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Операция выполнена")
        self.assertEqual(response.data['payment_status'], "success")
        self.assertEqual(float(response.data['current_balance']), 6000)

