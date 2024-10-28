from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users_app.models import BusinessProfile
from content_app.models import Offer, OfferDetails
from content_app.api.serializers import OfferSerializer, OfferDetailsSerializer
from content_app.utils import features_list_to_str

class General(APITestCase):
    
    def setUp(self):
        self.business_user = User.objects.create_user(username="businessuser", password="businesspassword")
        self.business_profile = BusinessProfile.objects.create(user=self.business_user, location="businesslocation", description="businessdescription")
        self.offer = Offer.objects.create(business_profile=self.business_profile, title="testtitle", description="testdescription")
        self.details_basic = OfferDetails.objects.create(offer_type=OfferDetails.BASIC, offer=self.offer, **OfferDetailsTests.EXAMPLE_DATA)
        self.details_standard = OfferDetails.objects.create(offer_type=OfferDetails.STANDARD, offer=self.offer, **OfferDetailsTests.EXAMPLE_DATA)
        self.details_premium = OfferDetails.objects.create(offer_type=OfferDetails.PREMIUM, offer=self.offer, **OfferDetailsTests.EXAMPLE_DATA)
        self.details_basic.features = features_list_to_str(self.details_basic.features)
        self.details_standard.features = features_list_to_str(self.details_standard.features)
        self.details_premium.features = features_list_to_str(self.details_premium.features)
        self.client = APIClient()
        self.client.login(username="businessuser", password='businesspassword')
        # change login logic after activating authentication
    
class OfferDetailsTests(APITestCase):
    EXAMPLE_DATA = {
        'title': 'detailstest',
        'price': 100,
        'features': ['feature1', 'feature2'],
        'revisions': 4,
        'delivery_time_in_days': 6,                
    }
    
    def setUp(self):
        General.setUp(self)

    def test_get_offerdetails_list_ok(self):
        url = reverse('offerdetails-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_offerdetails_detail_ok(self):
        url = reverse('offerdetails-detail', kwargs={"pk": self.details_standard.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data = OfferDetailsSerializer(self.details_standard).data
        expected_data = {
            'id': serializer_data.get('id'),
            'url': serializer_data.get('url'),
        }
        self.assertEqual(response.data, expected_data)   
        
class OfferTests(APITestCase):
    EXAMPLE_DATA = {
        'title': 'Grafikdesign-Paket',
        'image': 'urlplaceholder',
        'description': 'Ein umfassendes Grafikdesign-Paket für Unternehmen.',
        'details': [
            {
                'offer_type': OfferDetails.BASIC,
                **OfferDetailsTests.EXAMPLE_DATA.copy(),                
            },
            {
                'offer_type': OfferDetails.STANDARD,
                **OfferDetailsTests.EXAMPLE_DATA.copy(),                
            },
                                    {
                'offer_type': OfferDetails.PREMIUM,
                **OfferDetailsTests.EXAMPLE_DATA.copy(),                
            },
        ]
    }
    
    def setUp(self):
        General.setUp(self=self)
        
    def test_get_offer_list_ok(self):
        url = reverse('offer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_post_offer_list_ok(self):
        url = reverse('offer-list')
        response = self.client.post(url, self.EXAMPLE_DATA, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['details']), 3)
        
    def test_post_offer_list_unique_constraint_bad_request(self):
        url = reverse('offer-list')
        data = self.EXAMPLE_DATA.copy()
        data['details'][0]['offer_type'] = OfferDetails.STANDARD
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_get_offer_detail_ok(self):
        url = reverse('offer-detail', kwargs={"pk": self.offer.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)