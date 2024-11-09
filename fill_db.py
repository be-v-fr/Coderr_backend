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
        User.objects.create_user(username='Max_Mueller', password='passwort123', email='max.mueller@beispiel.de', first_name='Max', last_name='Mueller'),
        User.objects.create_user(username='Andreas_Bauer', password='passwort123', email='andreas.bauer@beispiel.de', first_name='Andreas', last_name='Bauer'),
        User.objects.create_user(username='Lucia_Schmidt', password='passwort456', email='lucia.schmidt@beispiel.de', first_name='Lucia', last_name='Schmidt'),
        User.objects.create_user(username='Anna_Krause', password='passwort456', email='anna.krause@beispiel.de', first_name='Anna', last_name='Krause'),
        User.objects.create_user(username='Tim_Jansen', password='passwort789', email='tim.jansen@beispiel.de', first_name='Tim', last_name='Jansen'),
        User.objects.create_user(username='Elisabeth_Neumann', password='passwort789', email='elisabeth.neumann@beispiel.de', first_name='Elisabeth', last_name='Neumann'),
        User.objects.create_user(username='Carlos_García', password='password123', email='carlos.garcia@example.com', first_name='Carlos', last_name='García'),
        User.objects.create_user(username='Sophia_Rossi', password='password123', email='sophia.rossi@example.com', first_name='Sophia', last_name='Rossi'),
        User.objects.create_user(username='John_Doe', password='password456', email='john.doe@example.com', first_name='John', last_name='Doe'),
        User.objects.create_user(username='Marie_Dubois', password='password456', email='marie.dubois@example.com', first_name='Marie', last_name='Dubois'),
        User.objects.create_user(username='Yuki_Sato', password='password789', email='yuki.sato@example.com', first_name='Yuki', last_name='Sato'),
        User.objects.create_user(username='Amina_Hassan', password='password789', email='amina.hassan@example.com', first_name='Amina', last_name='Hassan'),
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
        BusinessProfile.objects.create(user=users[6], location='Köln', description='Ein modernes Unternehmen', working_hours='8-17', tel='1122334455'),
        BusinessProfile.objects.create(user=users[7], location='Oldenburg (Oldb)', description='Ein großartiges Unternehmen', working_hours='8-17', tel='1122334455'),
        BusinessProfile.objects.create(user=users[8], location='Mainz', description='Ein modernes Unternehmen', working_hours='8-17', tel='1122334455'),
        BusinessProfile.objects.create(user=users[9], location='Chemnitz', description='Ein spezialisiertes Unternehmen', working_hours='8-17', tel='1122334455'),
        BusinessProfile.objects.create(user=users[10], location='Flensburg', description='Ein modernes Unternehmen', working_hours='8-17', tel='1122334455'),
        BusinessProfile.objects.create(user=users[11], location='Frankfurt a.M.', description='Ein modernes Unternehmen', working_hours='8-17', tel='1122334455'),
    ]

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
        Offer.objects.create(business_profile=b_profs[0], title='Website Redesign', description='Modernisieren Sie Ihre bestehende Website für eine bessere Benutzererfahrung.'),
        Offer.objects.create(business_profile=b_profs[3], title='Webdesign für lokale Unternehmen', description='Kreative Lösungen für kleine Unternehmen.'),
        Offer.objects.create(business_profile=b_profs[4], title='SEO-Paket für regionale Auffindbarkeit', description='Optimiert für lokale Suchmaschinenpräsenz.'),
        Offer.objects.create(business_profile=b_profs[5], title='Social Media Management', description='Effiziente Betreuung Ihrer Social Media Kanäle.'),
        Offer.objects.create(business_profile=b_profs[6], title='E-Commerce-Webdesign', description='E-Commerce-Lösungen für Online-Shops.'),
    ]
    
    OFFER_DETAILS_DATA = [
        {
            'features': 'Responsive Design,,SEO Optimiert',
            'title': 'Web Design - Basic',
            'delivery_time_in_days': 3,
            'revisions': 1,
        },
        {
            'features': 'Responsive Design,,SEO Optimiert,,Mehrsprachig',
            'title': 'Web Design - Standard',
            'delivery_time_in_days': 7,
            'revisions': 2,
        },
        {
            'features': 'Responsive Design,,SEO Optimiert,,Keyword Recherche,,Backlink Aufbau',
            'title': 'Web Design - Premium',
            'delivery_time_in_days': 21,
            'revisions': -1,
        },
        {
            'features': 'On-Page SEO,,Meta-Tag Optimierung',
            'title': 'SEO - Basic',
            'delivery_time_in_days': 3,
            'revisions': 2,
        },
        {
            'features': 'On-Page SEO,,Meta-Tag Optimierung,,Keyword Analyse',
            'title': 'SEO - Standard',
            'delivery_time_in_days': 7,
            'revisions': 3,
        },
        {
            'features': 'On-Page SEO,,Meta-Tag Optimierung,,Keyword Analyse,,Backlink Analyse',
            'title': 'SEO - Premium',
            'delivery_time_in_days': 21,
            'revisions': -1,
        },
        {
            'features': 'Facebook,,Instagram,,3 Beiträge/Woche',
            'title': 'Social Media - Basic',
            'delivery_time_in_days': 3,
            'revisions': 1,
        },
        {
            'features': 'Facebook,,Instagram,,LinkedIn,,5 Beiträge/Woche,,Community Management',
            'title': 'Social Media - Standard',
            'delivery_time_in_days': 7,
            'revisions': 2,
        },
        {
            'features': 'Facebook,,Instagram,,LinkedIn,,10 Beiträge/Woche,,Community Management,,Kampagnen Management',
            'title': 'Social Media - Premium',
            'delivery_time_in_days': 21,
            'revisions': 3,
        }
    ]

    offer_details = [
        OfferDetails.objects.create(offer=offers[0], offer_type='basic', price_cents=20000, **OFFER_DETAILS_DATA[0]),
        OfferDetails.objects.create(offer=offers[0], offer_type='standard', price_cents=30000, **OFFER_DETAILS_DATA[1]),
        OfferDetails.objects.create(offer=offers[0], offer_type='premium', price_cents=50000, **OFFER_DETAILS_DATA[2]),
        OfferDetails.objects.create(offer=offers[1], offer_type='basic', price_cents=15000, **OFFER_DETAILS_DATA[3]),
        OfferDetails.objects.create(offer=offers[1], offer_type='standard', price_cents=25000, **OFFER_DETAILS_DATA[4]),
        OfferDetails.objects.create(offer=offers[1], offer_type='premium', price_cents=40000, **OFFER_DETAILS_DATA[5]),
        OfferDetails.objects.create(offer=offers[2], offer_type='basic', price_cents=10000, **OFFER_DETAILS_DATA[6]),
        OfferDetails.objects.create(offer=offers[2], offer_type='standard', price_cents=20000, **OFFER_DETAILS_DATA[7]),
        OfferDetails.objects.create(offer=offers[2], offer_type='premium', price_cents=30000, **OFFER_DETAILS_DATA[8]),
        OfferDetails.objects.create(offer=offers[3], offer_type='basic', price_cents=22000, **OFFER_DETAILS_DATA[0]),
        OfferDetails.objects.create(offer=offers[3], offer_type='standard', price_cents=33000, **OFFER_DETAILS_DATA[1]),
        OfferDetails.objects.create(offer=offers[3], offer_type='premium', price_cents=53000, **OFFER_DETAILS_DATA[2]),
        OfferDetails.objects.create(offer=offers[4], offer_type='basic', price_cents=17000, **OFFER_DETAILS_DATA[3]),
        OfferDetails.objects.create(offer=offers[4], offer_type='standard', price_cents=28000, **OFFER_DETAILS_DATA[4]),
        OfferDetails.objects.create(offer=offers[4], offer_type='premium', price_cents=44000, **OFFER_DETAILS_DATA[5]),
        OfferDetails.objects.create(offer=offers[5], offer_type='basic', price_cents=12000, **OFFER_DETAILS_DATA[6]),
        OfferDetails.objects.create(offer=offers[5], offer_type='standard', price_cents=22000, **OFFER_DETAILS_DATA[7]),
        OfferDetails.objects.create(offer=offers[5], offer_type='premium', price_cents=35000, **OFFER_DETAILS_DATA[8]),
        OfferDetails.objects.create(offer=offers[6], offer_type='basic', price_cents=25000, **OFFER_DETAILS_DATA[0]),
        OfferDetails.objects.create(offer=offers[6], offer_type='standard', price_cents=38000, **OFFER_DETAILS_DATA[0]),
        OfferDetails.objects.create(offer=offers[6], offer_type='premium', price_cents=60000, **OFFER_DETAILS_DATA[0]),
        OfferDetails.objects.create(offer=offers[7], offer_type='basic', price_cents=13000, **OFFER_DETAILS_DATA[3]),
        OfferDetails.objects.create(offer=offers[7], offer_type='standard', price_cents=22000, **OFFER_DETAILS_DATA[4]),
        OfferDetails.objects.create(offer=offers[7], offer_type='premium', price_cents=36000, **OFFER_DETAILS_DATA[5]),
        OfferDetails.objects.create(offer=offers[8], offer_type='basic', price_cents=15000, **OFFER_DETAILS_DATA[6]),
        OfferDetails.objects.create(offer=offers[8], offer_type='standard', price_cents=26000, **OFFER_DETAILS_DATA[7]),
        OfferDetails.objects.create(offer=offers[8], offer_type='premium', price_cents=41000, **OFFER_DETAILS_DATA[8]),
        OfferDetails.objects.create(offer=offers[9], offer_type='basic', price_cents=30000, **OFFER_DETAILS_DATA[0]),
        OfferDetails.objects.create(offer=offers[9], offer_type='standard', price_cents=43000, **OFFER_DETAILS_DATA[0]),
        OfferDetails.objects.create(offer=offers[9], offer_type='premium', price_cents=65000, **OFFER_DETAILS_DATA[0]),
        OfferDetails.objects.create(offer=offers[10], offer_type='basic', price_cents=20000, **OFFER_DETAILS_DATA[3]),
        OfferDetails.objects.create(offer=offers[10], offer_type='standard', price_cents=30000, **OFFER_DETAILS_DATA[4]),
        OfferDetails.objects.create(offer=offers[10], offer_type='premium', price_cents=47000, **OFFER_DETAILS_DATA[5]),
        OfferDetails.objects.create(offer=offers[11], offer_type='basic', price_cents=14000, **OFFER_DETAILS_DATA[6]),
        OfferDetails.objects.create(offer=offers[11], offer_type='standard', price_cents=25000, **OFFER_DETAILS_DATA[7]),
        OfferDetails.objects.create(offer=offers[11], offer_type='premium', price_cents=40000, **OFFER_DETAILS_DATA[8]),
        OfferDetails.objects.create(offer=offers[12], offer_type='basic', price_cents=25000, **OFFER_DETAILS_DATA[0]),
        OfferDetails.objects.create(offer=offers[12], offer_type='standard', price_cents=38000, **OFFER_DETAILS_DATA[1]),
        OfferDetails.objects.create(offer=offers[12], offer_type='premium', price_cents=60000, **OFFER_DETAILS_DATA[2]),
        OfferDetails.objects.create(offer=offers[13], offer_type='basic', price_cents=250000, **OFFER_DETAILS_DATA[0]),
        OfferDetails.objects.create(offer=offers[13], offer_type='standard', price_cents=450000, **OFFER_DETAILS_DATA[1]),
        OfferDetails.objects.create(offer=offers[13], offer_type='premium', price_cents=750000, **OFFER_DETAILS_DATA[2]),
        OfferDetails.objects.create(offer=offers[14], offer_type='basic', price_cents=200000, **OFFER_DETAILS_DATA[3]),
        OfferDetails.objects.create(offer=offers[14], offer_type='standard', price_cents=400000, **OFFER_DETAILS_DATA[4]),
        OfferDetails.objects.create(offer=offers[14], offer_type='premium', price_cents=600000, **OFFER_DETAILS_DATA[5]),
        OfferDetails.objects.create(offer=offers[15], offer_type='basic', price_cents=150000, **OFFER_DETAILS_DATA[6]),
        OfferDetails.objects.create(offer=offers[15], offer_type='standard', price_cents=350000, **OFFER_DETAILS_DATA[7]),
        OfferDetails.objects.create(offer=offers[15], offer_type='premium', price_cents=550000, **OFFER_DETAILS_DATA[8]),
        OfferDetails.objects.create(offer=offers[16], offer_type='basic', price_cents=300000, **OFFER_DETAILS_DATA[0]),
        OfferDetails.objects.create(offer=offers[16], offer_type='standard', price_cents=500000, **OFFER_DETAILS_DATA[1]),
        OfferDetails.objects.create(offer=offers[16], offer_type='premium', price_cents=700000, **OFFER_DETAILS_DATA[2]),
    ]

    orders = [
        Order.objects.create(**get_order_create_dict(users[0], offer_details[0]), status='completed'),
        Order.objects.create(**get_order_create_dict(users[2], offer_details[3]), status='completed'),
        Order.objects.create(**get_order_create_dict(users[4], offer_details[6]), status='completed'),
        Order.objects.create(**get_order_create_dict(users[0], offer_details[1]), status='completed'),
        Order.objects.create(**get_order_create_dict(users[2], offer_details[7]), status='completed'),
        Order.objects.create(**get_order_create_dict(users[0], offer_details[8])),
        Order.objects.create(**get_order_create_dict(users[4], offer_details[2])),
        Order.objects.create(**get_order_create_dict(users[2], offer_details[4])),
        Order.objects.create(**get_order_create_dict(users[0], offer_details[5]), status='cancelled'),
        Order.objects.create(**get_order_create_dict(users[0], offer_details[0]), status='completed'),
        Order.objects.create(**get_order_create_dict(users[2], offer_details[13]), status='cancelled'),
        Order.objects.create(**get_order_create_dict(users[4], offer_details[26]), status='cancelled'),
        Order.objects.create(**get_order_create_dict(users[0], offer_details[35])),
        Order.objects.create(**get_order_create_dict(users[2], offer_details[42]), status='completed'),
        Order.objects.create(**get_order_create_dict(users[4], offer_details[47])),
        Order.objects.create(**get_order_create_dict(users[2], offer_details[40]), status='completed'),
        Order.objects.create(**get_order_create_dict(users[0], offer_details[46]), status='completed'),
        Order.objects.create(**get_order_create_dict(users[2], offer_details[37]), status='completed'),
        Order.objects.create(**get_order_create_dict(users[4], offer_details[41]), status='completed'),
    ]

    reviews = [
        CustomerReview.objects.create(reviewer_profile=c_profs[0], business_profile=b_profs[0], rating=5, description='Exzellenter Service! Sehr zufrieden mit dem Ergebnis.', created_at=date.today()),
        CustomerReview.objects.create(reviewer_profile=c_profs[1], business_profile=b_profs[1], rating=4, description='Gute Arbeit, aber die Lieferung war etwas verspätet.', created_at=date.today() - timedelta(days=2)),
        CustomerReview.objects.create(reviewer_profile=c_profs[2], business_profile=b_profs[2], rating=5, description='Toller Service! Sehr professionell und zuverlässig.', created_at=date.today() - timedelta(days=5)),
        CustomerReview.objects.create(reviewer_profile=c_profs[0], business_profile=b_profs[1], rating=5, description='Sehr zufrieden mit der SEO-Optimierung. Die Ergebnisse waren schnell sichtbar.', created_at=date.today() - timedelta(days=3)),
        CustomerReview.objects.create(reviewer_profile=c_profs[1], business_profile=b_profs[2], rating=4, description='Die Social Media-Kampagne war insgesamt gut, aber die Anzahl der Beiträge könnte höher sein.', created_at=date.today() - timedelta(days=10)),
        CustomerReview.objects.create(reviewer_profile=c_profs[0], business_profile=b_profs[2], rating=4, description='Professionelle Betreuung und schnelle Reaktionszeit.', created_at=date.today() - timedelta(days=15)),
        CustomerReview.objects.create(reviewer_profile=c_profs[1], business_profile=b_profs[0], rating=5, description='Sehr ansprechendes Webdesign und klare Kommunikation.', created_at=date.today() - timedelta(days=7)),
        CustomerReview.objects.create(reviewer_profile=c_profs[2], business_profile=b_profs[3], rating=5, description='Hervorragender SEO-Service, die Sichtbarkeit hat sich stark verbessert.', created_at=date.today() - timedelta(days=8)),
        CustomerReview.objects.create(reviewer_profile=c_profs[0], business_profile=b_profs[5], rating=4, description='Die Webdesign-Lösung war gut, aber es gab kleine Verzögerungen.', created_at=date.today() - timedelta(days=12)),
        CustomerReview.objects.create(reviewer_profile=c_profs[2], business_profile=b_profs[0], rating=5, description='Effektiver Service, hat meine Erwartungen übertroffen.', created_at=date.today() - timedelta(days=14))
    ]

    print('Data added successfully.')

if __name__ == '__main__':
    fill_database()