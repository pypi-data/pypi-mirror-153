# django-unumcharfield
Django Char Field using Unum

## Description
UnumCharField is a simple Django app to use Unum through a CharField.

## Install
Run the command in the terminal::

    pip install django-unumcharfield

## Quick start
1. Import in your models.py::

    from unumcharfield.models import UnumCharField

2. Use it as CharField.

## Test
1. If you would like to check if UnumCharField is working fine, add
UnumCharField demo application to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'unumcharfield.demo',
    ]

2. Include the UnumCharField URLconf in your project urls.py like this::

    from django.urls import include
    ...
    path('unumcharfield/', include('unumcharfield.demo.urls')),

3. Run `python manage.py makemigrations demo` to create the unumcharfield models.

4. Run `python manage.py migrate` to create the unumcharfield models.

5. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a unumcharfield (you'll need the Admin app enabled).

6. Visit http://127.0.0.1:8000/unumcharfield/ to check.