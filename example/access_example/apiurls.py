from django.conf.urls import include, url
from django.conf import settings
from tastypie.api import Api

v1_api = Api(api_name='v1')

from accessprofile.api import *
v1_api.register(UserResource())
v1_api.register(GroupResource())

urlpatterns = [
    url(r'', include(v1_api.urls)),
]
