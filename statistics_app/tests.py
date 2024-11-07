from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from content_app.tests.tests_reviews import General as ReviewsTests
from content_app.models import CustomerReview

class General(APITestCase):
    
    def setUp(self):
        ReviewsTests.setUp(self)
        
class BaseInfoTests(APITestCase):
    
    def setUp(self):
        General.setUp(self)
        self.scnd_review = CustomerReview.objects.create(
            reviewer_profile=self.customer_profile,
            business_profile=self.scnd_business_profile,
            rating=3,
            description='testdescription'
        )
        
    def test_get_review_list_ok(self):
        url = reverse('base-info-list')
        response = self.client.get(url)
        average_rating = (self.review.rating + self.scnd_review.rating) / 2
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['average_rating'], f"{average_rating:.1f}")
        
class OrderCountTests(APITestCase):
    
    def setUp(self):
        General.setUp(self)
        
    def test_get_order_count_detail_ok(self):
        url = reverse('order-count-detail', kwargs={'pk': self.business_user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_order_count_detail_user_not_found(self):
        url = reverse('order-count-detail', kwargs={'pk': User.objects.count() + 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
class CompletedOrderCountTests(APITestCase):
    
    def setUp(self):
        General.setUp(self)
        
    def test_get_order_count_detail_ok(self):
        url = reverse('completed-order-count-detail', kwargs={'pk': self.business_user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_order_count_detail_user_not_found(self):
        url = reverse('completed-order-count-detail', kwargs={'pk': User.objects.count() + 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)