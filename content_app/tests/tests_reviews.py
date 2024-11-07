from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from coderr_backend.utils import reverse_with_queryparams
from users_app.models import BusinessProfile
from content_app.models import Offer, OfferDetails, Order, CustomerReview
from content_app.api.serializers import CustomerReviewSerializer
from content_app.tests.tests_offers import OfferDetailsTests
from content_app.tests.tests_orders import General as OrdersTests
from content_app.utils import get_order_create_dict

class General(APITestCase):
    
    def setUp(self):
        OrdersTests.setUp(self)
        self.review = CustomerReview.objects.create(
            reviewer_profile=self.customer_profile,
            business_profile=self.business_profile,
            rating=4,
            description='testdescription'
        )
        self.scnd_business_user = User.objects.create_user(username='secondbusinessuser', password='businesspassword')
        self.scnd_business_profile = BusinessProfile.objects.create(user=self.scnd_business_user, location='businesslocation', description='businessdescription')
        self.scnd_offer = Offer.objects.create(business_profile=self.scnd_business_profile, title='testtitle', description='testdescription')
        self.scnd_details_standard = OfferDetails.objects.create(offer_type=OfferDetails.STANDARD, offer=self.scnd_offer, **OfferDetailsTests.CREATE_DATA)
        self.scnd_order = Order.objects.create(**get_order_create_dict(
            current_user=self.customer_user,
            offer=self.scnd_offer,
            offer_details=self.scnd_details_standard,
        ))
        
class ReviewTests(APITestCase):
    
    def setUp(self):
        General.setUp(self)
        
    def test_get_review_list_ok(self):
        url = reverse('review-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_review_list_filter_ok(self):
        params = {
            'business_user_id': self.business_user.id,
            'reviewer_id': self.customer_user.id,
        }
        url = reverse_with_queryparams('review-list', **params)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for review_data in response.data:
            self.assertEqual(review_data['business_user'], params['business_user_id'])
            self.assertEqual(review_data['reviewer'], params['reviewer_id'])
        
    def test_post_review_list_ok(self):
        data = {
            'business_user': self.scnd_business_profile.user.pk,
            'rating': 4,
            'description': 'posttestdescription',
        }
        url = reverse('review-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertIn('reviewer', response.data)
        
    def test_post_review_list_missing_field_bad_request(self):
        data = {
            'business_user': self.scnd_business_profile.user.pk,
            'description': 'posttestdescription',
        }
        url = reverse('review-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_post_review_list_unique_constraint_bad_request(self):
        data = {
            'business_user': self.business_profile.user.pk,
            'description': 'posttestdescription',
        }
        url = reverse('review-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_get_review_detail_ok(self):
        url = reverse('review-detail', kwargs={'pk': self.review.pk})
        response = self.client.get(url)
        expected_data = CustomerReviewSerializer(self.review).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)