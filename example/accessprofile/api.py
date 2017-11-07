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
