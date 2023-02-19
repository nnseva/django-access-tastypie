[![Tests](https://github.com/nnseva/django-access-tastypie/actions/workflows/test.yml/badge.svg)](https://github.com/nnseva/django-access-tastypie/actions/workflows/test.yml)

# Django-Access-Tastypie

The Django-Access-Tastypie package provides an authorization backend for the [Django-Tastypie](https://django-tastypie.readthedocs.io/en/latest/) package to use access rules defined by the [Django-Access](https://github.com/nnseva/django-access) package.

## Installation

*Stable version* from the PyPi package repository
```bash
pip install django-access-tastypie
```

*Last development version* from the GitHub source version control system
```bash
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

## Using

### Define access rules

Define access rules as it is described in the [Django-Access](https://github.com/nnseva/django-access) package documentation.

### Modified model resource

You should use modified `ModelResource` successors in your project.

The `access_tastypie.resources.AccessModelResourceMixin` may be used to mix into any existent `tastypie.resources.ModelResource` successor.

The `access_tastypie.resources.AccessModelResource` may be used as a base class for your own model resource instead of `tastypie.resources.ModelResource` class. Really it is a pure combination of `access_tastypie.resources.AccessModelResourceMixin` and`tastypie.resources.ModelResource` base classes.

### Authorization backend

You should use `access_tastypie.authorization.AccessAuthorization` authorization backend **instead** of `tastypie.authorization.DjangoAuthorization`. It will totally replace authorization algorithm to take access rules defined for your project in account while requesting your api.

## Example

Having in mind the [example](https://github.com/nnseva/django-access#examples) defined for the [Django-Access](https://github.com/nnseva/django-access), let we describe the api resources as the following:

```python
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from tastypie.authentication import MultiAuthentication, SessionAuthentication

from access_tastypie.authorization import AccessAuthorization
from access_tastypie.resources import AccessModelResource

from django.contrib.auth import models as auth_models

class UserResource(AccessModelResource):
    class Meta:
        queryset = auth_models.User.objects.all()
        filtering = dict([(f.name, ALL_WITH_RELATIONS) for f in queryset.model._meta.get_fields()])
        authentication = MultiAuthentication(
            SessionAuthentication()
        )
        authorization = AccessAuthorization()
        resource_name = 'user'
        always_return_data = True
        excludes = ['password']

class GroupResource(AccessModelResource):
    class Meta:
        queryset = auth_models.Group.objects.all()
        filtering = dict([(f.name, ALL_WITH_RELATIONS) for f in queryset.model._meta.get_fields()])
        authentication = MultiAuthentication(
            SessionAuthentication()
        )
        authorization = AccessAuthorization()
        resource_name = 'group'
        always_return_data = True
```
