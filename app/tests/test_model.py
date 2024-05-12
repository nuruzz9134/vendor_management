from django.test import TestCase
from django.contrib.auth import get_user_model
from app.models import *
User = get_user_model()

class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='vendor1',
            vendor_code='v12345',
            password='vendor12345'
        )
        self.order = PurchaseOrder.objects.create(
            po_number='PO001',
            vendor=self.user,
            status='pending'
        )
        self.performance = HistoricalPerformance.objects.create(
            vendor=self.user,
            on_time_delivery_rate=0.9,
            quality_rating_avg=4.5,
            average_response_time=24,
            fulfillment_rate=0.95
        )

    def test_vendor_creation(self):
        self.assertEqual(self.user.username, 'vendor1')
        self.assertEqual(self.user.vendor_code, 'v12345')
        self.assertTrue(self.user.check_password('vendor12345'))

    def test_order_creation(self):
        self.assertEqual(self.order.po_number, 'PO001')
        self.assertEqual(self.order.vendor, self.user)
        self.assertEqual(self.order.status, 'pending')

    def test_performance_creation(self):
        self.assertEqual(self.performance.vendor, self.user)
        self.assertEqual(self.performance.on_time_delivery_rate, 0.9)
        self.assertEqual(self.performance.quality_rating_avg, 4.5)
        self.assertEqual(self.performance.average_response_time, 24)
        self.assertEqual(self.performance.fulfillment_rate, 0.95)
