Coderr backend is a Django backend providing a marketplace for coding services and related services.

(c) 2025 Bengt Früchtenicht

General functionality:
======================

Users can register as business users or customers.
Business users can create offers and update the offer state.
Customers can create offer orders and customer reviews for the related business.

Local setup:
============

- Install the Python dependencies listed in `requirements.txt`.
- Run `python manage.py makemigrations` in the shell
- Run `python manage.py migrate`

Filling the database:
=====================

After the initial migration, the database will be empty. You can either fill it manually
or execute the `fill_db.py` script, which contains example data in the German language:
- Run `python fill_db.py`

Local hosting:
==============

To use your own device as server:
- Run `python manage.py runserver`

You can use both `http://localhost:8000/` and `http://127.0.0.1:8000/` as base URLs.

The `admin/` sub-URL features the default Django database interface. To login, you need
to create an admin account:
- Run `python manage.py createsuperuser`

The `api/` sub-URL features the API URLs as listed in the `urls.py` files prevalent in the
`api` folder of the sub-app packages (`users_app/api`, `content_app/api`, `statistics_app/api`).
When accessing the URLs via browser, the default Django REST Framework interface will show.

Documentation:
==============

To access the documentation, load the `docs` route in your browser.
You can also use your IDE to host `docs_app/docs/_build/index.html` via a non-Django live server.
The documentation has been auto-generated from comments inside the Python files.

Data structure:
===============

The data structure for each API endpoint can vary depending on the request method.

To get a first impression regarding GET requests, you can use the Django REST Framework interface
mentioned above.

To gain an insight into the data structure required for writing, study
- The tests for the respective POST and PATCH requests towards the endpoint in interest.
- The serializers in the respective `serializers.py` file or `serializers` folder.
- The documentation.

Frontend information:
=====================

The Coderr backend at hand was developed for a given frontend. The backend is fully matched to
the 1.0 version of the frontend, i.e., no configuration changes were made.