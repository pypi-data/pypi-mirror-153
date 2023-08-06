#django-old-new-history
======================

|PyPI latest| |PyPI Version| |PyPI License|


**django-old-new-history** is customize history feature which is used to show the old and new value of model's change field in history action of admin panel.

=============
Requirements
=============

- Python 3.7 or later
- Django 2.0 or later

=============
Features
=============

-  Customize history.
-  Display old and new value of model's change field.
-  Simple admin integration.

=============


------------
Installation
------------

Just use:

::

    pip install django-old-new-history

------------
Setup
------------

Add **django_old_new_history** to **INSTALLED_APPS** in your settings.py, e.g.:

::

    INSTALLED_APPS = [
    ...
    'django_old_new_history',
    ...


------------
Usage
------------

Inherit from **DjangoOldNewHistory** to get the custom history feature.

admin.py e.g.:

::

    
    from django.contrib import admin
    from .models import ExampleModel
    from django_old_new_history.admin import DjangoOldNewHistory
    
    @admin.register(ExampleModel)
    class ExampleModelAdmin(DjangoOldNewHistory, admin.ModelAdmin):
        ...

------------
Screenshot
------------

Here is screenshot of django-old-new-history

|Screenshot|

.. |PyPI Version| image:: https://img.shields.io/pypi/pyversions/django-old-new-history.svg?maxAge=60
   :target: https://pypi.python.org/pypi/django-old-new-history
.. |PyPI License| image:: https://img.shields.io/pypi/l/django-old-new-history.svg?maxAge=120
   :target: https://github.com/Softices/django-old-new-history/blob/main/LICENSE
.. |PyPI latest| image:: https://img.shields.io/pypi/v/django-old-new-history.svg?maxAge=120
   :target: https://pypi.python.org/pypi/django-old-new-history
.. |Screenshot| image:: https://raw.githubusercontent.com/mayur-softices/djnago-customize-history/main/docs/_static/Change-history-CrudUser-object-5-Django-site-admin.png
