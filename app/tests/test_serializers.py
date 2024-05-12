from django.test import TestCase
from app.models import Vendors, PurchaseOrder, HistoricalPerformance
from app.serializers import VendorSerializers, PurchaseOrderSerializers, HistoricalPerformanceSerializers

class SerializerTestCase(TestCase):
    def setUp(self):
        self.vendor_data = {
            'username': 'test_vendor',
            'contact_details': 'Test contact',
            'address': 'Test address',
            'vendor_code': 'V001',
            'password': 'test_password',
            'on_time_delivery_rate': 0.95,
            'quality_rating_avg': 4.5,
            'average_response_time': 24,
            'fulfillment_rate': 0.98
        }

        self.order_data = {
            'po_number': 'PO001',
            'vendor': None, 
            'order_date': '2024-05-12T12:00:00Z',
            'delivery_date': '2024-05-15T12:00:00Z',
            'items': ['Item 1', 'Item 2'],
            'quantity': 10,
            'status': 'pending',
            'quality_rating': 4.0,
            'issue_date': '2024-05-13T12:00:00Z',
            'acknowledgment_date': '2024-05-14T12:00:00Z',
        }

        self.performance_data = {
            'vendor': None, 
            'date': '2024-05-12T12:00:00Z',
            'on_time_delivery_rate': 0.95,
            'quality_rating_avg': 4.5,
            'average_response_time': 24,
            'fulfillment_rate': 0.98
        }

    def test_vendor_serializer(self):
        serializer = VendorSerializers(data=self.vendor_data)
        self.assertTrue(serializer.is_valid())
        vendor_instance = serializer.save()

        self.assertEqual(vendor_instance.username, 'test_vendor')
        self.assertEqual(vendor_instance.vendor_code, 'V001')

    def test_order_create_serializer(self):
        vendor = Vendors.objects.create_user(username='vendor1', vendor_code='V002', password='vendorpass')
        self.order_data['vendor'] = vendor.pk
        serializer = PurchaseOrderSerializers(data=self.order_data)
        self.assertTrue(serializer.is_valid())
        order_instance = serializer.save()

        self.assertEqual(order_instance.po_number, 'PO001')
        self.assertEqual(order_instance.vendor, vendor)
        self.assertEqual(order_instance.quantity, 10)


    def test_order_list_serializer(self):
        vendor = Vendors.objects.create_user(username='vendor1', vendor_code='V002', password='vendorpass')
        order = PurchaseOrder.objects.create(
            po_number='PO002',
            vendor=vendor, 
            status='pending'
        )
        serializer = PurchaseOrderSerializers(instance=order)
        self.assertEqual(serializer.data['po_number'], 'PO002')
        self.assertEqual(serializer.data['status'], 'pending')

    def test_performance_serializer(self):
        vendor = Vendors.objects.create_user(username='vendor2', vendor_code='V003', password='vendorpass')
        self.performance_data['vendor'] = vendor.pk
        serializer = HistoricalPerformanceSerializers(data=self.performance_data)
        self.assertTrue(serializer.is_valid())
        performance_instance = serializer.save()

        self.assertEqual(performance_instance.vendor, vendor)
        self.assertEqual(performance_instance.on_time_delivery_rate, 0.95)
        self.assertEqual(performance_instance.quality_rating_avg, 4.5)
