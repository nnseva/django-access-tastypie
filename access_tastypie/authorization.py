from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized, ImmediateHttpResponse, ApiFieldError

from django.utils.six import text_type, string_types

from django.conf import settings

import collections
from django.db.models.fields.related import ForeignObjectRel

from access.managers import AccessManager


class AccessAuthorization(Authorization):
    '''
    This class authorizes access to models accordingly to access control rules defined
    in the project.
    '''

    def apply_able(self, ability, queryset, request):
        return AccessManager(queryset.model).apply_able(ability, queryset, request)

    def check_able(self, ability, model, request):
        return AccessManager(model).check_able(ability, model, request)

    def read_list(self, object_list, bundle):
        if self.check_able('visible', object_list.model, bundle.request) is False:
            return False
        return self.apply_able('visible', object_list, bundle.request)

    def read_detail(self, object_list, bundle):
        if self.check_able('visible', object_list.model, bundle.request) is False:
            return False
        if bundle.obj:
            return self.apply_able('visible', object_list.filter(pk=bundle.obj.pk), bundle.request)
        return True

    def update_list(self,object_list,bundle):
        if not getattr(settings,'ACCESS_ALLOW_BULK_UPDATE', False):
            raise Unauthorized()  # too dangerous
        if self.check_able('changeable', object_list.model, bundle.request) is False:
            return False
        return self.apply_able('changeable', object_list, bundle.request)

    def update_detail(self,object_list,bundle):
        if self.check_able('changeable', object_list.model, bundle.request) is False:
            return False
        if bundle.obj:
            return self.apply_able('changeable', object_list.filter(pk=bundle.obj.pk), bundle.request)
        return True

    def delete_list(self,object_list,bundle):
        if not getattr(settings,'ACCESS_ALLOW_BULK_DELETE', False):
            raise Unauthorized()  # too dangerous
        if self.check_able('deleteable', object_list.model, bundle.request) is False:
            return False
        return self.apply_able('deleteable', object_list, bundle.request)

    def delete_detail(self,object_list,bundle):
        if self.check_able('deleteable', object_list.model, bundle.request) is False:
            return False
        if bundle.obj:
            return self.apply_able('deleteable', object_list.filter(pk=bundle.obj.pk), bundle.request)
        return True

    def create_list(self,object_list,bundle):
        raise Unauthorized() # is never used by the Tastypie

    def create_detail(self,object_list,bundle):
        data = self.check_able('appendable', object_list.model, bundle.request)
        if data is False:
            return False
        '''
        for k in data:
            v = data[k]
            fieldname = k
            if fieldname.endswith("_set"):
                fieldname = fieldname[:-4]
            field = bundle.obj._meta.get_field(fieldname)
            if isinstance(v, collections.Iterable) and not isinstance(v, string_types) and isinstance(field, ForeignObjectRel):
                continue
            if getattr(bundle.obj, k) is None:
                setattr(bundle.obj, k, v)
        '''
        return True
