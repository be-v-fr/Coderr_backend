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
    """
    General setup class for creating reusable test instances of customer users, profiles, tokens, and orders.
    """    
    def setUp(self):
        """
        Inherits offers tests general setup. Also creates a customer user, customer profile, and an order.
        Also configures the client with an authorization token for the customer user.
        """
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
    """
    Tests for Order endpoints, focusing on order creation, retrieval, updating, and deletion with permissions.
    """
    def setUp(self):
        """
        Inherits the general setup for creating test data for orders.
        """
        General.setUp(self)
        
    def test_get_order_list_ok(self):
        """
        Tests retrieval of the list of orders.

        Asserts:
            - 200 OK status.
        """
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_post_order_list_ok(self):
        """
        Tests successful creation of an order with basic offer details.

        Asserts:
            - 201 Created status.
            - Order status is set to IN_PROGRESS.
            - 'offer_type' field is present in response.
            - 'offer_detail_id' and 'offer_details' fields are absent in response.
        """
        data = {'offer_detail_id': self.details_basic.pk}
        url = reverse('order-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], Order.IN_PROGRESS)
        self.assertIn('offer_type', response.data)
        self.assertNotIn('offer_detail_id', response.data)
        self.assertNotIn('offer_details', response.data)
        
    def test_post_order_list_bad_request(self):
        """
        Tests order creation with invalid data, expecting a bad request response.

        Asserts:
            - 400 Bad Request status.
        """
        data = {'offer_details': OfferDetailsSerializer(self.details_basic).data}
        url = reverse('order-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_get_order_detail_ok(self):
        """
        Tests retrieval of specific order details.

        Asserts:
            - 200 OK status.
            - Response data matches serialized order data.
            - 'offer_type' field is present in response.
            - 'offer_detail_id' and 'offer_details' fields are absent in response.
            - 'price' is in float format
        """
        url = reverse('order-detail', kwargs={'pk': self.order.pk})
        response = self.client.get(url)
        expected_data = OrderSerializer(self.order).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        self.assertIn('offer_type', response.data)
        self.assertNotIn('offer_detail_id', response.data)
        self.assertNotIn('offer_details', response.data)
        self.assertIsInstance(response.data['price'], float)
        
    def test_patch_order_detail_ok(self):
        """
        Tests updating an order status to 'cancelled' by an authorized business user.

        Asserts:
            - 200 OK status.
            - Order status is updated to 'cancelled' in response.
            - 'offer_type' field is present in response.
            - 'offer_detail_id' and 'offer_details' fields are absent in response.
        """
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
        """
        Tests updating an order with invalid field data, expecting a bad request response.

        Asserts:
            - 400 Bad Request status.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        data = {'title': 'newtitle'}
        url = reverse('order-detail', kwargs={'pk': self.order.pk})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_delete_order_detail_as_customer_forbidden(self):
        """
        Tests deletion of an order by the customer, expecting forbidden response.

        Asserts:
            - 403 Forbidden status.
        """
        url = reverse('order-detail', kwargs={'pk': self.order.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_delete_order_detail_as_creator_forbidden(self):
        """
        Tests deletion of an order by the creator (business user), expecting forbidden response.

        Asserts:
            - 403 Forbidden status.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        url = reverse('order-detail', kwargs={'pk': self.order.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)