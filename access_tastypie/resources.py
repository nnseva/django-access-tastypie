from tastypie.resources import ModelResource
from tastypie.exceptions import Unauthorized

from django.db.models.fields.related import ForeignObjectRel

from django.utils.six import string_types

import collections

from access.managers import AccessManager


class AccessModelResource(ModelResource):
    def obj_create(self, bundle, **kwargs):
        manager = AccessManager(bundle.obj.__class__)
        data = manager.check_appendable(bundle.obj.__class__, bundle.request)
        if data is False:
            raise Unauthorized("Is not appendable")
        new_bundle = super(AccessModelResource, self).obj_create(bundle, **kwargs)
        if data:
            for k in data:
                v = data[k]
                fieldname = k
                if fieldname.endswith("_set"):
                    fieldname = fieldname[:-4]
                field = bundle.obj._meta.get_field(fieldname)
                if isinstance(field, ForeignObjectRel):
                    if isinstance(v, collections.Iterable) and not isinstance(v, string_types):
                        fld = getattr(bundle.obj, k)
                        for i in v:
                            fld.add(i)
                elif getattr(bundle.obj, k) is None:
                    setattr(bundle.obj, k, v)
            new_bundle.obj.save()
        return new_bundle
