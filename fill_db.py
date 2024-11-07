import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coderr_backend.settings')
django.setup()

from users_app.models import CustomerProfile, BusinessProfile
from django.contrib.auth.models import User
from content_app.models import Offer, OfferDetails, Order, CustomerReview
from content_app.utils import get_order_create_dict

def fill_database():
    users = [
        User.objects.create_user(username='Max Mueller', password='passwort123', email='max.mueller@beispiel.de'),
        User.objects.create_user(username='Andreas Bauer', password='passwort123', email='andreas.bauer@beispiel.de'),
        User.objects.create_user(username='Lucia Schmidt', password='passwort456', email='lucia.schmidt@beispiel.de'),
        User.objects.create_user(username='Anna Krause', password='passwort456', email='anna.krause@beispiel.de'),
        User.objects.create_user(username='Tim Jansen', password='passwort789', email='tim.jansen@beispiel.de'),
        User.objects.create_user(username='Elisabeth Neumann', password='passwort789', email='elisabeth.neumann@beispiel.de'),
    ]

    c_profs = [
        CustomerProfile.objects.create(user=users[0]),
        CustomerProfile.objects.create(user=users[2]),
        CustomerProfile.objects.create(user=users[4]),
    ]
    
    b_profs = [
        BusinessProfile.objects.create(user=users[1], location='Berlin', description='Ein großartiges Unternehmen', working_hours='9-18', tel='0123456789'),
        BusinessProfile.objects.create(user=users[3], location='Hamburg', description='Ein spezialisiertes Unternehmen', working_hours='10-20', tel='0987654321'),
        BusinessProfile.objects.create(user=users[5], location='München', description='Ein modernes Unternehmen', working_hours='8-17', tel='1122334455'),
    ]

    comm_feat = {
        'web_design': 'Responsive Design,,SEO Optimiert',
        'web_design_standard': 'Responsive Design,,SEO Optimiert,,Mehrsprachig',
        'web_design_premium': 'Responsive Design,,SEO Optimiert,,Keyword Recherche,,Backlink Aufbau',
        'seo_basic': 'On-Page SEO,,Meta-Tag Optimierung',
        'seo_standard': 'On-Page SEO,,Meta-Tag Optimierung,,Keyword Analyse',
        'seo_premium': 'On-Page SEO,,Meta-Tag Optimierung,,Keyword Analyse,,Backlink Analyse',
        'social_media_basic': 'Facebook,,Instagram,,3 Beiträge/Woche',
        'social_media_standard': 'Facebook,,Instagram,,LinkedIn,,5 Beiträge/Woche,,Community Management',
        'social_media_premium': 'Facebook,,Instagram,,LinkedIn,,10 Beiträge/Woche,,Community Management,,Kampagnen Management'
    }

    offers = [
        Offer.objects.create(business_profile=b_profs[0], title='Webdesign-Paket A', description='Ein umfassendes Webdesign-Paket für kleine Unternehmen.'),
        Offer.objects.create(business_profile=b_profs[1], title='SEO-Optimierung', description='Optimieren Sie Ihre Website für bessere Google-Rankings.'),
        Offer.objects.create(business_profile=b_profs[2], title='Social Media Management', description='Verwalten Sie Ihre Social-Media-Kanäle effizient und effektiv.'),
        Offer.objects.create(business_profile=b_profs[0], title='Webdesign-Paket B', description='Erstellen Sie eine moderne und ansprechende Website für Ihr Unternehmen.'),
        Offer.objects.create(business_profile=b_profs[1], title='SEO Complete', description='Ein vollständiges SEO-Paket für Ihre Website.'),
        Offer.objects.create(business_profile=b_profs[2], title='Social Media Boost', description='Steigern Sie Ihre Social-Media-Präsenz mit gezielten Kampagnen.'),
        Offer.objects.create(business_profile=b_profs[0], title='Landing Page Design', description='Erstellen Sie eine hochwertige Landing Page für Ihre Marketing-Kampagnen.'),
        Offer.objects.create(business_profile=b_profs[1], title='SEO Audit', description='Überprüfen Sie Ihre Website auf SEO-Fehler und Verbesserungspotenziale.'),
        Offer.objects.create(business_profile=b_profs[2], title='Social Media Strategie', description='Entwickeln Sie eine maßgeschneiderte Strategie für Ihre Social-Media-Kanäle.'),
        Offer.objects.create(business_profile=b_profs[0], title='Online Shop Design', description='Erstellen Sie einen funktionalen und ansprechenden Online-Shop.'),
        Offer.objects.create(business_profile=b_profs[1], title='SEO-Content-Erstellung', description='Erstellen Sie SEO-optimierten Content für Ihre Website.'),
        Offer.objects.create(business_profile=b_profs[2], title='Social Media Ads', description='Schalten Sie gezielte Social Media-Anzeigen zur Kundenakquise.'),
        Offer.objects.create(business_profile=b_profs[0], title='Website Redesign', description='Modernisieren Sie Ihre bestehende Website für eine bessere Benutzererfahrung.')
    ]

    offer_details = [
        OfferDetails.objects.create(offer=offers[0], offer_type='basic', price_cents=1999, features=comm_feat['web_design']),
        OfferDetails.objects.create(offer=offers[0], offer_type='standard', price_cents=2999, features=comm_feat['web_design_standard']),
        OfferDetails.objects.create(offer=offers[0], offer_type='premium', price_cents=4999, features=comm_feat['web_design_premium']),
        OfferDetails.objects.create(offer=offers[1], offer_type='basic', price_cents=1499, features=comm_feat['seo_basic']),
        OfferDetails.objects.create(offer=offers[1], offer_type='standard', price_cents=2499, features=comm_feat['seo_standard']),
        OfferDetails.objects.create(offer=offers[1], offer_type='premium', price_cents=3999, features=comm_feat['seo_premium']),
        OfferDetails.objects.create(offer=offers[2], offer_type='basic', price_cents=999, features=comm_feat['social_media_basic']),
        OfferDetails.objects.create(offer=offers[2], offer_type='standard', price_cents=1999, features=comm_feat['social_media_standard']),
        OfferDetails.objects.create(offer=offers[2], offer_type='premium', price_cents=2999, features=comm_feat['social_media_premium']),
        OfferDetails.objects.create(offer=offers[3], offer_type='basic', price_cents=2199, features=comm_feat['web_design']),
        OfferDetails.objects.create(offer=offers[3], offer_type='standard', price_cents=3299, features=comm_feat['web_design_standard']),
        OfferDetails.objects.create(offer=offers[3], offer_type='premium', price_cents=5299, features=comm_feat['web_design_premium']),
        OfferDetails.objects.create(offer=offers[4], offer_type='basic', price_cents=1699, features=comm_feat['seo_basic']),
        OfferDetails.objects.create(offer=offers[4], offer_type='standard', price_cents=2799, features=comm_feat['seo_standard']),
        OfferDetails.objects.create(offer=offers[4], offer_type='premium', price_cents=4399, features=comm_feat['seo_premium']),
        OfferDetails.objects.create(offer=offers[5], offer_type='basic', price_cents=1199, features=comm_feat['social_media_basic']),
        OfferDetails.objects.create(offer=offers[5], offer_type='standard', price_cents=2199, features=comm_feat['social_media_standard']),
        OfferDetails.objects.create(offer=offers[5], offer_type='premium', price_cents=3499, features=comm_feat['social_media_premium']),
        OfferDetails.objects.create(offer=offers[6], offer_type='basic', price_cents=2499, features=comm_feat['web_design']),
        OfferDetails.objects.create(offer=offers[6], offer_type='standard', price_cents=3799, features=comm_feat['web_design_standard']),
        OfferDetails.objects.create(offer=offers[6], offer_type='premium', price_cents=5999, features=comm_feat['web_design_premium']),
        OfferDetails.objects.create(offer=offers[7], offer_type='basic', price_cents=1299, features=comm_feat['seo_basic']),
        OfferDetails.objects.create(offer=offers[7], offer_type='standard', price_cents=2199, features=comm_feat['seo_standard']),
        OfferDetails.objects.create(offer=offers[7], offer_type='premium', price_cents=3599, features=comm_feat['seo_premium']),
        OfferDetails.objects.create(offer=offers[8], offer_type='basic', price_cents=1499, features=comm_feat['social_media_basic']),
        OfferDetails.objects.create(offer=offers[8], offer_type='standard', price_cents=2599, features=comm_feat['social_media_standard']),
        OfferDetails.objects.create(offer=offers[8], offer_type='premium', price_cents=4099, features=comm_feat['social_media_premium']),
        OfferDetails.objects.create(offer=offers[9], offer_type='basic', price_cents=2999, features=comm_feat['web_design']),
        OfferDetails.objects.create(offer=offers[9], offer_type='standard', price_cents=4299, features=comm_feat['web_design_standard']),
        OfferDetails.objects.create(offer=offers[9], offer_type='premium', price_cents=6499, features=comm_feat['web_design_premium']),
        OfferDetails.objects.create(offer=offers[10], offer_type='basic', price_cents=1999, features=comm_feat['seo_basic']),
        OfferDetails.objects.create(offer=offers[10], offer_type='standard', price_cents=2999, features=comm_feat['seo_standard']),
        OfferDetails.objects.create(offer=offers[10], offer_type='premium', price_cents=4699, features=comm_feat['seo_premium']),
        OfferDetails.objects.create(offer=offers[11], offer_type='basic', price_cents=1399, features=comm_feat['social_media_basic']),
        OfferDetails.objects.create(offer=offers[11], offer_type='standard', price_cents=2499, features=comm_feat['social_media_standard']),
        OfferDetails.objects.create(offer=offers[11], offer_type='premium', price_cents=3999, features=comm_feat['social_media_premium']),
        OfferDetails.objects.create(offer=offers[12], offer_type='basic', price_cents=2499, features=comm_feat['web_design']),
        OfferDetails.objects.create(offer=offers[12], offer_type='standard', price_cents=3799, features=comm_feat['web_design_standard']),
        OfferDetails.objects.create(offer=offers[12], offer_type='premium', price_cents=5999, features=comm_feat['web_design_premium']),
    ]

    orders = [
        Order.objects.create(status='completed', **get_order_create_dict(users[0], offer_details[0])),
        Order.objects.create(status='completed', **get_order_create_dict(users[2], offer_details[3])),
        Order.objects.create(status='completed', **get_order_create_dict(users[4], offer_details[6])),
        Order.objects.create(status='completed', **get_order_create_dict(users[0], offer_details[1])),
        Order.objects.create(status='completed', **get_order_create_dict(users[2], offer_details[7])),
        Order.objects.create(**get_order_create_dict(users[0], offer_details[8])),
        Order.objects.create(**get_order_create_dict(users[4], offer_details[2])),
        Order.objects.create(**get_order_create_dict(users[2], offer_details[4])),
        Order.objects.create(status='cancelled', **get_order_create_dict(users[0], offer_details[5])),
    ]

    reviews = [
        CustomerReview.objects.create(reviewer_profile=c_profs[0], business_profile=b_profs[0], rating=5, description='Exzellenter Service! Sehr zufrieden mit dem Ergebnis.', created_at=date.today()),
        CustomerReview.objects.create(reviewer_profile=c_profs[1], business_profile=b_profs[1], rating=4, description='Gute Arbeit, aber die Lieferung war etwas verspätet.', created_at=date.today() - timedelta(days=2)),
        CustomerReview.objects.create(reviewer_profile=c_profs[2], business_profile=b_profs[2], rating=5, description='Toller Service! Sehr professionell und zuverlässig.', created_at=date.today() - timedelta(days=5)),
        CustomerReview.objects.create(reviewer_profile=c_profs[0], business_profile=b_profs[1], rating=5, description='Sehr zufrieden mit der SEO-Optimierung. Die Ergebnisse waren schnell sichtbar.', created_at=date.today() - timedelta(days=3)),
        CustomerReview.objects.create(reviewer_profile=c_profs[1], business_profile=b_profs[2], rating=4, description='Die Social Media-Kampagne war insgesamt gut, aber die Anzahl der Beiträge könnte höher sein.', created_at=date.today() - timedelta(days=10)),
    ]

    print('Data added successfully.')

if __name__ == '__main__':
    fill_database()