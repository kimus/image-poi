# -*- coding: UTF-8 -*-
from django.conf.urls import patterns

urlpatterns = patterns('imagepoi.views',
    (r'^crosshair$', 'crosshair'),
    (r'^(?P<path>.*)$', 'image'),
)
