from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from coderr_backend.utils import reverse_with_queryparams
from users_app.models import BusinessProfile
from content_app.models import Offer, OfferDetails, Order, CustomerReview
from content_app.api.serializers.general import CustomerReviewSerializer
from content_app.tests.tests_offers import OfferDetailsTests
from content_app.tests.tests_orders import General as OrdersTests
from content_app.utils.general import get_order_create_dict

class General(APITestCase):
    """
    General setup class for creating reusable instances of users, profiles, orders, and reviews for testing.
    """
    def setUp(self):
        """
        Inherits orders tests general setup. Also creates a customer review.
        Also sets up a second business user, profile, offer, and order for test flexibility.
        """
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
            offer_details=self.scnd_details_standard,
        ))
        
class ReviewTests(APITestCase):
    """
    Tests for Review endpoints, covering review creation, retrieval, filtering, and deletion.
    """
    def setUp(self):
        """
        Inherits setup from the General class, including test users, profiles, and reviews.
        """
        General.setUp(self)
        
    def test_get_review_list_ok(self):
        """
        Tests successful retrieval of a list of reviews.

        Asserts:
            - 200 OK status.
        """
        url = reverse('review-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_review_list_filter_ok(self):
        """
        Tests retrieval of reviews filtered by business user ID and reviewer ID.

        Asserts:
            - 200 OK status.
            - Each review in the response data matches the requested filter criteria.
        """
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
        """
        Tests successful creation of a new review for a business.

        Asserts:
            - 201 Created status.
            - The response includes 'id' and 'reviewer' fields.
        """
        data = {
            'business_user': self.scnd_business_profile.user.pk,
            'rating': 4,
            'description': 'posttestdescription',
        }
        url = reverse('review-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key in ('id', 'reviewer'):
            self.assertIn(key, response.data)
        
    def test_post_review_list_missing_field_bad_request(self):
        """
        Tests review creation with a missing 'rating' field, expecting a bad request response.

        Asserts:
            - 400 Bad Request status.
        """
        data = {
            'business_user': self.scnd_business_profile.user.pk,
            'description': 'posttestdescription',
        }
        url = reverse('review-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_post_review_list_unique_constraint_bad_request(self):
        """
        Tests review creation with a duplicate review for the same business, expecting a unique constraint violation.

        Asserts:
            - 400 Bad Request status.
        """
        data = {
            'business_user': self.business_profile.user.pk,
            'description': 'posttestdescription',
        }
        url = reverse('review-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_get_review_detail_ok(self):
        """
        Tests retrieval of a specific review's details.

        Asserts:
            - 200 OK status.
            - Response data matches the serialized review data.
        """
        url = reverse('review-detail', kwargs={'pk': self.review.pk})
        response = self.client.get(url)
        expected_data = CustomerReviewSerializer(self.review).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        
    def test_delete_review_detail_no_content(self):
        """
        Tests successful deletion of a review.

        Asserts:
            - 204 No Content status.
        """
        url = reverse('review-detail', kwargs={'pk': self.review.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)