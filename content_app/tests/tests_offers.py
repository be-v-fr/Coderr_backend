from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users_app.models import BusinessProfile
from content_app.models import Offer, OfferDetails
from content_app.api.serializers import OfferSerializer, OfferDetailsSerializer

class OfferTests(APITestCase):
    
    def setUp(self):
        self.business_user = User.objects.create_user(username="businessuser", password="businesspassword")
        self.business_profile = BusinessProfile.objects.create(user=self.business_user, location="businesslocation", description="businessdescription")
        self.offer = Offer.objects.create(business_profile=self.business_profile, description="testdescription")
        self.client = APIClient()
        # add login logic after activating authentication
        
    def test_get_offer_list_ok(self):
        url = reverse('offer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_profile_detail_customer_ok(self):
        url = reverse('offer-detail', kwargs={"pk": self.offer.pk})
        response = self.client.get(url)
        expected_data = OfferSerializer(self.offer).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)