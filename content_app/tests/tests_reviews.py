from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from content_app.models import CustomerReview
from content_app.api.serializers import CustomerReviewSerializer
from content_app.tests.tests_orders import General as OrdersTests

class General(APITestCase):
    
    def setUp(self):
        OrdersTests.setUp(self)
        self.review = CustomerReview.objects.create(
            reviewer_profile=self.customer_profile,
            business_profile=self.business_profile,
            rating=4,
            description='testdescription'
        )
        # change login logic after activating authentication
        
class ReviewTests(APITestCase):
    
    def setUp(self):
        General.setUp(self)
        
    def test_get_review_list_ok(self):
        url = reverse('review-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_post_review_list_ok(self):
        data = {
            'business_user': self.business_profile.user.pk,
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