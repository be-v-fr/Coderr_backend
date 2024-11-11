from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from coderr_backend.utils import reverse_with_queryparams
from users_app.models import BusinessProfile
from content_app.models import Offer, OfferDetails
from content_app.api.serializers import OfferDetailsSerializer
from content_app.utils import features_list_to_str
import copy

class General(APITestCase):
    
    def setUp(self):
        self.business_user = User.objects.create_user(username='businessuser', password='businesspassword')
        self.business_profile = BusinessProfile.objects.create(user=self.business_user, location='businesslocation', description='businessdescription')
        self.offer = Offer.objects.create(business_profile=self.business_profile, title='testtitle', description='testdescription')
        self.details_basic = OfferDetails.objects.create(offer_type=OfferDetails.BASIC, offer=self.offer, **OfferDetailsTests.CREATE_DATA)
        self.details_standard = OfferDetails.objects.create(offer_type=OfferDetails.STANDARD, offer=self.offer, **OfferDetailsTests.CREATE_DATA)
        self.details_premium = OfferDetails.objects.create(offer_type=OfferDetails.PREMIUM, offer=self.offer, **OfferDetailsTests.CREATE_DATA)
        self.details_basic.features = features_list_to_str(self.details_basic.features)
        self.details_standard.features = features_list_to_str(self.details_standard.features)
        self.details_premium.features = features_list_to_str(self.details_premium.features)
        self.business_token = Token.objects.create(user=self.business_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
    
class OfferDetailsTests(APITestCase):
    CREATE_DATA = {
        'title': 'detailstest',
        'price': '100.00',
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
        url = reverse('offerdetails-detail', kwargs={'pk': self.details_standard.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('url', response.data)
        
class OfferTests(APITestCase):
    QUERY_PARAMS = {
        'min_price': 200
    }    

    CREATE_DATA = {
        'title': 'Grafikdesign-Paket',
        'description': 'Ein umfassendes Grafikdesign-Paket für Unternehmen.',
        'details': [
            {
                'offer_type': OfferDetails.BASIC,
                **OfferDetailsTests.CREATE_DATA.copy(),                
            },
            {
                'offer_type': OfferDetails.STANDARD,
                **OfferDetailsTests.CREATE_DATA.copy(),                
            },
                                    {
                'offer_type': OfferDetails.PREMIUM,
                **OfferDetailsTests.CREATE_DATA.copy(),                
            },
        ]
    }
    
    PATCH_DATA = {
        'title': 'titlepatch',
        'details': [
            {
                'offer_type': OfferDetails.BASIC,
                'price': '768.00',
                'features': ['patchfeature1', 'patchfeature2'],
            },
        ],
    }
    
    def setUp(self):
        General.setUp(self=self)
        
    def test_get_offer_list_ok(self):
        url = reverse('offer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        
    def test_get_offer_list_filter_ok(self):
        url = reverse_with_queryparams('offer-list', **self.QUERY_PARAMS)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for offer_data in response.data['results']:
            min_price_int = int(float(offer_data['min_price']))
            self.assertLessEqual(min_price_int, self.QUERY_PARAMS['min_price'])
        
    def test_post_offer_list_ok(self):
        url = reverse('offer-list')
        response = self.client.post(url, self.CREATE_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['details']), 3)
        
    def test_post_offer_list_double_title_unique_constraint(self):
        url = reverse('offer-list')
        response_first = self.client.post(url, self.CREATE_DATA, format='json')
        response_second = self.client.post(url, self.CREATE_DATA, format='json')
        self.assertEqual(response_first.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_second.status_code, status.HTTP_409_CONFLICT)
        
    def test_post_offer_list_double_offer_type_validation_err(self):
        url = reverse('offer-list')
        data = copy.deepcopy(self.CREATE_DATA)
        data['details'][0]['offer_type'] = OfferDetails.STANDARD
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_get_offer_detail_ok(self):
        url = reverse('offer-detail', kwargs={'pk': self.offer.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_patch_offer_detail_ok(self):
        url = reverse('offer-detail', kwargs={'pk': self.offer.pk})
        response = self.client.patch(url, self.PATCH_DATA, format='json')
        self.offer.refresh_from_db()
        updated_features = self.offer.details.get(offer_type=OfferDetails.BASIC).features
        expected_features = features_list_to_str(self.PATCH_DATA['details'][0]['features'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.offer.title, self.PATCH_DATA['title'])
        self.assertEqual(updated_features, expected_features)
        
    def test_patch_offer_detail_double_title_unique_constraint(self):
        data = {'title': self.CREATE_DATA['title']}
        url_post = reverse('offer-list')
        url_patch = reverse('offer-detail', kwargs={'pk': self.offer.pk})
        response_post = self.client.post(url_post, self.CREATE_DATA, format='json')
        response_patch = self.client.patch(url_patch, data, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_patch.status_code, status.HTTP_409_CONFLICT)
        
    def test_patch_offer_detail_missing_offer_type_validation_err(self):
        data = copy.deepcopy(self.PATCH_DATA)
        data['details'][0].pop('offer_type')
        url = reverse('offer-detail', kwargs={'pk': self.offer.pk})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_patch_offer_detail_double_offer_type_validation_err(self):
        data = copy.deepcopy(self.PATCH_DATA)
        data['details'].append(data['details'][0])
        url = reverse('offer-detail', kwargs={'pk': self.offer.pk})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_delete_offer_detail_no_content(self):
        url = reverse('offer-detail', kwargs={'pk': self.offer.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)