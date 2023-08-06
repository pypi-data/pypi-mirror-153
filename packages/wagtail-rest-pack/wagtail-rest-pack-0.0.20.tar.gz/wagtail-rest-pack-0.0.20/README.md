# wagtail-rest-pack

# wagtail-rest-pack

=====
Rest Page Children
=====

Wagtail app creating an views that expose children of pages

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

   INSTALLED_APPS = [
   ...
   'wagtail_rest_pack',
   ]

2. Include the polls URLconf in your project urls.py like this::

   url(r'^polls/', include('polls.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/polls/ to participate in the poll.