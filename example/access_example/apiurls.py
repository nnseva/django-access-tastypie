try:
    from django.urls import re_path, include
except ImportError:
    from django.conf.urls import url as re_path, include

from django.conf import settings
from tastypie.api import Api

v1_api = Api(api_name='v1')

from accessprofile.api import *
v1_api.register(UserResource())
v1_api.register(GroupResource())

urlpatterns = [
    re_path(r'', include(v1_api.urls)),
]
