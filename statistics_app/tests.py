from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from content_app.tests.tests_reviews import General as ReviewsTests
from content_app.models import CustomerReview

class General(APITestCase):
    """
    General setup class to prepare necessary data across different test classes.
    """
    def setUp(self):
        """
        Inherits offers tests general setup.        
        """
        ReviewsTests.setUp(self)
        
class BaseInfoTests(APITestCase):
    """
    Tests for retrieving basic information about reviews, including the average rating.
    """
    def setUp(self):
        """
        Extends the setup from `General`, creating an additional customer review instance.
        """
        General.setUp(self)
        self.scnd_review = CustomerReview.objects.create(
            reviewer_profile=self.customer_profile,
            business_profile=self.scnd_business_profile,
            rating=3,
            description='testdescription'
        )
        
    def test_get_review_list_ok(self):
        """
        Tests successful retrieval of review list with calculated average rating.

        Asserts:
            - 200 OK status.
            - The calculated average rating matches the expected value, formatted to 1 decimal place.
        """
        url = reverse('base-info-list')
        response = self.client.get(url)
        average_rating = (self.review.rating + self.scnd_review.rating) / 2
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['average_rating'], f"{average_rating:.1f}")
        
class OrderCountTests(APITestCase):
    """
    Tests for retrieving the total count of active orders associated with a business user.
    """
    def setUp(self):
        """
        Sets up the test environment by extending setup from the `General` class.
        """
        General.setUp(self)
        
    def test_get_order_count_detail_ok(self):
        """
        Tests successful retrieval of the order count for a specific business user.

        Asserts:
            - 200 OK status.
        """
        url = reverse('order-count-detail', kwargs={'pk': self.business_user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_order_count_detail_user_not_found(self):
        """
        Tests response when requesting order count for a non-existent user.

        Asserts:
            - 404 Not Found status.
        """
        url = reverse('order-count-detail', kwargs={'pk': User.objects.count() + 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
class CompletedOrderCountTests(APITestCase):
    """
    Tests for retrieving the count of completed orders for a specific business user.
    """
    def setUp(self):
        """
        Extends the setup from `General` to prepare completed order count testing.
        """
        General.setUp(self)
        
    def test_get_order_count_detail_ok(self):
        """
        Tests successful retrieval of the completed order count for a business user.

        Asserts:
            - 200 OK status.
        """
        url = reverse('completed-order-count-detail', kwargs={'pk': self.business_user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_order_count_detail_user_not_found(self):
        """
        Tests response when requesting completed order count for a non-existent user.

        Asserts:
            - 404 Not Found status.
        """
        url = reverse('completed-order-count-detail', kwargs={'pk': User.objects.count() + 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)