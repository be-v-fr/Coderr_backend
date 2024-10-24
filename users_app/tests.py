from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import CustomerProfile, BusinessProfile
from .api.serializers import CustomerProfileSerializer, BusinessProfileSerializer

class ProfileTests(APITestCase):
    
    def setUp(self):
        self.customer_user = User.objects.create_user(username="customeruser", password="customerpassword")
        self.customer_profile = CustomerProfile.objects.create(user=self.customer_user)
        self.business_user = User.objects.create_user(username="businessuser", password="businesspassword")
        self.business_profile = BusinessProfile.objects.create(user=self.business_user, location="businesslocation", description="businessdescription")
        self.client = APIClient()
        
    def test_get_profile_detail_customer(self):
        url = reverse('profile-detail', kwargs={"pk": self.customer_user.id})
        response = self.client.get(url)
        expected_data = CustomerProfileSerializer(self.customer_profile).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        
    def test_get_profile_detail_business(self):
        url = reverse('profile-detail', kwargs={"pk": self.business_user.id})
        response = self.client.get(url)
        expected_data =BusinessProfileSerializer(self.business_profile).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        