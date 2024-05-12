from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from app.models import Vendors, PurchaseOrder, HistoricalPerformance

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendors.objects.create_user(
            username='vendor54',
            vendor_code='vendor54',
            password='test_password'
        )
        if not Token.objects.filter(user=self.vendor).exists():
            self.vendor_token = Token.objects.create(user=self.vendor)
        else:
            self.vendor_token = Token.objects.get(user=self.vendor)

        self.order_data = {
            'po_number': 'PO001',
            'vendor': self.vendor.id,
            'order_date': '2024-05-12T12:00:00Z',
            'delivery_date': '2024-05-15T12:00:00Z',
            'items': ['Item 1', 'Item 2'],
            'quantity': 10,
            'status': 'pending',
            'quality_rating': 4.0,
            'issue_date': '2024-05-13T12:00:00Z',
            'acknowledgment_date': '2024-05-14T12:00:00Z',
        }

    def test_create_new_vendor(self):
        url = reverse('create_new_vendor')
        response = self.client.post(url, {'username': 'new_vendor', 'password': 'new_password'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('message' in response.data)

    def test_vendors_list(self):
        url = reverse('vendors_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('message' in response.data)

    def test_single_vendor(self):
        url = reverse('single_vendor', args=[self.vendor.vendor_code])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('massage' in response.data)

    def test_new_order(self):
        url = reverse('new_order')
        headers = {'Authorization': f'Token {self.vendor_token}'}
        if 'vendor' not in self.order_data or self.order_data['vendor'] is None:
            self.order_data['vendor'] = self.vendor.id
        self.order_data['vendor']=self.vendor.id
        response = self.client.post(url, self.order_data, format='json',headers=headers)
        print('Response data:', response.data) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('message' in response.data)

    def test_order_list(self):
        url = reverse('order_list')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.vendor_token))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('orders' in response.data)

    def test_single_order(self):
        order = PurchaseOrder.objects.create(**self.order_data)
        url = reverse('single_order', args=[order.po_number])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.vendor_token))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('message' in response.data)

    def test_update_order(self):
        order = PurchaseOrder.objects.create(**self.order_data)
        url = reverse('update_order', args=[order.po_number])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.vendor_token)
        response = self.client.put(url, {'status': 'completed'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('message' in response.data)

    def test_vendor_performance(self):
        url = reverse('vendor_performance', args=[self.vendor.vendor_code])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('massage' in response.data)

    def test_update_acknowledgment_date(self):
        order = PurchaseOrder.objects.create(**self.order_data)
        url = reverse('update_acknowledgment_date', args=[order.po_number])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.vendor_token)
        response = self.client.post(url, {'acknowledgment_date': '2024-05-14T12:00:00Z'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('message' in response.data)
