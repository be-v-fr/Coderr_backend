from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from .models import CustomerProfile, BusinessProfile
from .api.serializers import CustomerProfileDetailSerializer, BusinessProfileDetailSerializer
import copy

CUSTOMER_USER_DATA = {
    'username': 'customer_user',
    'first_name': 'customer',
    'last_name': 'user',
    'password': 'customerpassword',        
}
    
BUSINESS_USER_DATA = {
    'username': 'business_user',
    'first_name': 'business',
    'last_name': 'user',
    'password': 'businesspassword',        
}

class General(APITestCase):
    """
    Base test setup class for creating test users, profiles, and tokens.
    """    
    def setUp(self):
        """
        Creates a customer and business user, with associated profiles and authentication tokens.
        """
        self.customer_user = User.objects.create_user(**CUSTOMER_USER_DATA)
        self.customer_profile = CustomerProfile.objects.create(user=self.customer_user)
        self.customer_token = Token.objects.create(user=self.customer_user)
        self.business_user = User.objects.create_user(**BUSINESS_USER_DATA)
        self.business_profile = BusinessProfile.objects.create(user=self.business_user, location="businesslocation", description="businessdescription")
        self.business_token = Token.objects.create(user=self.business_user)
        self.client = APIClient()
        
class AuthTests(APITestCase):
    """
    Tests for user authentication endpoints, including login and registration.

    Attributes:
        AUTH_DATA (dict): Test data for registration including username, password, and email.
    """
    AUTH_DATA = {
        'username': 'newuser',
        'password': 'newPassw0rd',
        'repeated_password': 'newPassw0rd',
        'email': 'new@email.com',
        'type': CustomerProfile.TYPE,
    }
    
    def setUp(self):
        """
        Calls the general setup for shared test data.
        """
        General.setUp(self)
        
    def test_login_ok(self):
        """
        Tests successful login with correct credentials.
        
        Asserts:
            200 OK status.
            Presence of required fields in response data.
        """
        data = {
            'username': self.customer_user.username,
            'password': 'customerpassword',
        }
        url = reverse('login')
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in ('token', 'username', 'email', 'user_id'):
            self.assertIn(key, response.data)
        
    def test_login_false_password_bad_request(self):
        """
        Tests login with incorrect password.
        
        Asserts:
            400 Bad Request status.
        """
        data = {
            'username': self.customer_user.username,
            'password': 'password',
        }
        url = reverse('login')
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_registration_ok(self):
        """
        Tests successful user registration.
        
        Asserts:
            201 Created status.
            Valid customer profile association.
            Presence of required fields in response data.
        """
        url = reverse('registration')
        response = self.client.post(url, self.AUTH_DATA, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user_id'], CustomerProfile.objects.get(user=response.data['user_id']).user.pk)
        for key in ('token', 'username', 'email'):
            self.assertIn(key, response.data)
        
    def test_registration_weak_password_bad_request(self):
        """
        Tests registration with a weak password.

        Asserts:
            400 Bad Request status.
        """
        data = copy.deepcopy(self.AUTH_DATA)
        password = 'newpassword'
        data['password'] = password
        data['repeated_password'] = password
        url = reverse('registration')
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_registration_passwords_not_matching_bad_request(self):
        """
        Tests registration when passwords do not match.
        
        Asserts:
            400 Bad Request status.
        """
        data = copy.deepcopy(self.AUTH_DATA)
        data['repeated_password'] += 'a'
        url = reverse('registration')
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_registration_email_missing_bad_request(self):
        """
        Tests registration with missing email field.
        
        Asserts:
            400 Bad Request status.
        """
        data = copy.deepcopy(self.AUTH_DATA)
        data['email'] = ''
        url = reverse('registration')
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_registration_username_taken_bad_request(self):
        """
        Tests registration when username is already taken.
        
        Asserts:
            400 Bad Request status.
        """
        data = copy.deepcopy(self.AUTH_DATA)
        data['username'] = self.customer_user.username
        url = reverse('registration')
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_registration_email_taken_bad_request(self):
        """
        Tests registration when email is already taken.
        
        Asserts:
            400 Bad Request status.
        """
        data = copy.deepcopy(self.AUTH_DATA)
        data['email'] = self.customer_user.email
        url = reverse('registration')
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ProfileTests(APITestCase):
    """
    Tests for profile-related endpoints, including retrieval and updates.
    """
    def setUp(self):
        """
        Calls the general setup for shared test data.
        """
        General.setUp(self)
        
    def test_get_profile_detail_customer_ok(self):
        """
        Tests retrieval of customer profile details.

        Asserts:
            200 OK status.
            Expected profile data matches response.
        """
        url = reverse('profile-detail', kwargs={"pk": self.customer_user.id})
        response = self.client.get(url)
        expected_data = CustomerProfileDetailSerializer(self.customer_profile).data
        expected_data.update(file=None, uploaded_at=None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        
    def test_get_profile_detail_business_ok(self):
        """
        Tests retrieval of business profile details.
        
        Asserts:
            200 OK status.
            Expected profile data matches response.
        """
        url = reverse('profile-detail', kwargs={"pk": self.business_user.id})
        response = self.client.get(url)
        expected_data = BusinessProfileDetailSerializer(self.business_profile).data
        expected_data.update(file=None, uploaded_at=None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        
    def test_get_profile_detail_user_not_found(self):
        """
        Tests profile retrieval for non-existent user.

        Asserts:
            404 Not Found status.
        """
        pk = User.objects.count() + 1
        url = reverse('profile-detail', kwargs={"pk": pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_get_profile_detail_user_profile_not_found(self):
        """
        Tests profile retrieval for user without a profile.

        Asserts:
            404 Not Found status.
        """
        no_profile_user = User.objects.create_user(username="noprofileuser", password="noprofilepassword")
        url = reverse('profile-detail', kwargs={"pk": no_profile_user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_patch_customer_profile_detail_ok(self):
        """
        Tests updating a customer profile.

        Asserts:
            200 OK status.
            Expected updated profile data matches response.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        new_username = 'customerpatch'
        data = { 'username': new_username }
        url = reverse('profile-detail', kwargs={"pk": self.customer_user.id})
        response = self.client.patch(url, data, format="json")
        expected_data = CustomerProfileDetailSerializer(self.customer_profile).data
        expected_data['username'] = new_username
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        
    def test_patch_foreign_profile_detail_forbidden(self):
        """
        Tests updating a foreign user profile.

        Asserts:
            403 Forbidden status.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        data = { 'username': 'patch' }
        url = reverse('profile-detail', kwargs={"pk": self.business_user.id})
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_patch_business_profile_detail_ok(self):
        """
        Tests updating a business profile.

        Asserts:
            200 OK status.
            Expected updated profile data matches response.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        new_username = 'businesspatch'
        new_location = 'patchcity'
        data = {
            'username': new_username,
            'location' : new_location,
        }
        url = reverse('profile-detail', kwargs={"pk": self.business_user.id})
        response = self.client.patch(url, data, format="json")
        expected_data = BusinessProfileDetailSerializer(self.business_profile).data
        expected_data.update({'username': new_username, 'location': new_location})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        
    def test_get_customer_profile_list_ok(self):
        """
        Tests retrieval of customer profile list.

        Asserts:
            200 OK status.
            'file' key is in each list item.
            'uploaded_at' key is in no list item.
        """
        url = reverse('customer-list')
        response = self.client.get(url)    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for profile in response.data:
            self.assertIn('file', profile)
            self.assertNotIn('uploaded_at', profile)
        
    def test_get_business_profile_list_ok(self):
        """
        Tests retrieval of business profile list.

        Asserts:
            200 OK status.
            'file' key is in each list item.
            'uploaded_at' key is in no list item.
        """
        url = reverse('business-list')
        response = self.client.get(url)    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for profile in response.data:
            self.assertIn('file', profile)
            self.assertNotIn('uploaded_at', profile)