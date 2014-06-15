# -*- coding: UTF-8 -*-
from django.db import models
from django.db.models.signals import post_init
from django.db.models.fields import FieldDoesNotExist

from .forms import ImageCenterFormField


class ImageCenter(object):
    def __init__(self, image_field, value=None):
        self.image_field = image_field
        if value is not None:
            value = value.strip()
        self._value = value
        self.type = 'top'
        self.x = 0
        self.y = 0

        if value is not None:
            if value == 'noop' or value == 'top' or value == 'center':
                self.type = value
            else:
                self.type = 'point'
                try:
                    p = value.replace('%', '').split(' ')
                    self.x = int(p[0])
                    self.y = int(p[1])
                except ValueError:
                    self.type = 'noop'
        else:
            self._value = 'noop'

    @property
    def value(self):
        return self.__unicode__()

    def __unicode__(self):
        if self._value == 'noop' or self._value == 'top' or self._value == 'center':
            return self._value
        else:
            return str(self.x) + "% " + str(self.y) + "%"


class ImageCenterField(models.Field):

    attr_class = ImageCenter

    description = "A field that stores the center of attention for an image."

    __metaclass__ = models.SubfieldBase

    def __init__(self, image_field=None, *args, **kwargs):
        #if image_field is not None:
        #    if not isinstance(image_field, models.ImageField):
        #        raise ValueError("image_field value must be an ImageField instance")
        kwargs["default"] = "noop"
        self.image_field = image_field
        super(ImageCenterField, self).__init__(*args, **kwargs)

    def set_instance(self, instance):
        self.instance = instance

    def formfield(self, **kwargs):
        defaults = {'form_class': ImageCenterFormField}
        defaults.update(kwargs)
        return super(ImageCenterField, self).formfield(**defaults)

    def db_type(self, connection):
        return "char(100)"

    # this method is called when the value comes from the database
    def to_python(self, value):
        if isinstance(value, ImageCenter):
            return value
        return ImageCenter(self.image_field, value=value)

    # this method is called when the value is about to be written to the database
    def get_db_prep_value(self, value, connection=None, prepared=False):
        try:
            return value.__unicode__()
        except AttributeError:
            return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

    def query_string(self):
        return u"crop=%s" % self.value.__unicode__()



def post_init_capture(sender, instance, *args, **kwargs):
    fields = instance.__class__._meta.get_all_field_names()
    for field_name in fields:
        try:
            field = instance.__class__._meta.get_field(field_name)
            if isinstance(field, ImageCenterField):
                image_field = instance.__class__._meta.get_field(field.image_field.name)
                image_instance = instance.__getattribute__(image_field.name)
                image_center_instance = instance.__getattribute__(field.name)
                image_instance.__image_center_instance__ = image_center_instance
                image_center_instance.image_path = unicode(image_instance)
        except FieldDoesNotExist:
            pass

post_init.connect(post_init_capture)


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^imagepoi\.fields\.ImageCenterField$"])
except ImportError:
    pass
