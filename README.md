[![Build Status](https://travis-ci.org/nnseva/django-access-tastypie.svg?branch=master)](https://travis-ci.org/nnseva/django-access-tastypie)

# Django-Access-Tastypie

## Installation

*Stable version* from the PyPi package repository
```bash
pip install django-access-tastypie
```

*Last development version* from the GitHub source version control system
```
pip install git+git://github.com/nnseva/django-access-tastypie.git
```

## Configuration

Include the `tastypie`, `access`, and `access_tastypie` applications into the `INSTALLED_APPS` list, like:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    ...
    'tastypie',
    'access',
    'access_tastypie',
    ...
]
```

