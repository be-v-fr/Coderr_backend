from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from users_app.models import CustomerProfile
from content_app.models import Order
from content_app.api.serializers.general import OfferDetailsSerializer, OrderSerializer
from content_app.tests.tests_offers import General as OffersTests
from content_app.utils.general import get_order_create_dict

class General(APITestCase):
    
    def setUp(self):
        OffersTests.setUp(self)
        self.customer_user = User.objects.create_user(username='customeruser', password='customerpassword')
        self.customer_profile = CustomerProfile.objects.create(user=self.customer_user)
        self.order = Order.objects.create(**get_order_create_dict(
            current_user=self.customer_user,
            offer_details=self.details_standard,
        ))
        self.customer_token = Token.objects.create(user=self.customer_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        
    
class OrderTests(APITestCase):
    
    def setUp(self):
        General.setUp(self)
        
    def test_get_order_list_ok(self):
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_post_order_list_ok(self):
        data = {'offer_detail_id': self.details_basic.pk}
        url = reverse('order-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], Order.IN_PROGRESS)
        self.assertIn('offer_type', response.data)
        self.assertNotIn('offer_detail_id', response.data)
        self.assertNotIn('offer_details', response.data)
        
    def test_post_order_list_bad_request(self):
        data = {'offer_details': OfferDetailsSerializer(self.details_basic).data}
        url = reverse('order-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_get_order_detail_ok(self):
        url = reverse('order-detail', kwargs={'pk': self.order.pk})
        response = self.client.get(url)
        expected_data = OrderSerializer(self.order).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        self.assertIn('offer_type', response.data)
        self.assertNotIn('offer_detail_id', response.data)
        self.assertNotIn('offer_details', response.data)
        
    def test_patch_order_detail_ok(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        data = {'status': Order.CANCELLED}
        url = reverse('order-detail', kwargs={'pk': self.order.pk})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], data['status'])
        self.assertIn('offer_type', response.data)
        self.assertNotIn('offer_detail_id', response.data)
        self.assertNotIn('offer_details', response.data)
        
    def test_patch_order_detail_bad_request(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        data = {'title': 'newtitle'}
        url = reverse('order-detail', kwargs={'pk': self.order.pk})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_delete_order_detail_as_customer_forbidden(self):
        url = reverse('order-detail', kwargs={'pk': self.order.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_delete_order_detail_as_creator_forbidden(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        url = reverse('order-detail', kwargs={'pk': self.order.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)