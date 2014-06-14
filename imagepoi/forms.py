# -*- coding: UTF-8 -*-
from django import forms
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django.utils.encoding import force_unicode
from django.core.urlresolvers import reverse
import threading


COUNTER = 0


class ImageCenterFormWidget(forms.Widget):

    def _format_value(self, value):
        return unicode(value)

    def render(self, name, value, attrs=None):

        global COUNTER

        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(self._format_value(value))

        resp = ''
        if getattr(value, 'image_path', None):
            try:
                resp =  '<div id="imagepoi-widget-' + str(COUNTER) + '">\n'
                resp += '    <select class="imagepoi-select" style="display: block; width: 150px;">\n'
                resp += '        <option value="noop">None</option>\n'
                resp += '        <option value="top">Top</option>\n'
                resp += '        <option value="center">Center</option>\n'
                resp += '        <option value="point">Point</option>\n'
                resp += '    </select>\n'
                resp += '    <div class="imagepoi-point" style="clear: left; display: none; position:relative;">\n'
                resp += '        <img class="imagepoi-image" src="' + reverse('imagepoi.views.image', args=(value.image_path,)) + '" onclick=""/>\n'
                resp += '        <img class="imagepoi-crosshair" src="' + reverse('imagepoi.views.crosshair') + '" style="position:absolute; left:0; top:0;" />\n'
                resp += '    </div>\n'
                resp += '   <input%s />\n' % flatatt(final_attrs)
                resp += '</div>\n'
                resp += '<script>\n'
                resp += '(function($) {\n'
                resp += '    $(window).load(function(){\n'
                resp += '        var imwidget = $("#imagepoi-widget-' + str(COUNTER) + '");\n'
                resp += '        var select = imwidget.find(".imagepoi-select");\n'
                resp += '        var image = imwidget.find(".imagepoi-image");\n'
                resp += '        var crosshair = imwidget.find(".imagepoi-crosshair");\n'
                resp += '        var input = imwidget.find("input");\n'
                
                resp += '        var iw = image.get(0).width;\n'
                resp += '        var ih = image.get(0).height;\n'
                
                resp += '        crosshair.css( { left: (iw * ' + (str(float(value.x) / 100)) + ' - 7)+"px", top: (ih*' + (str(float(value.y) / 100)) + ' - 7)+"px" } );\n'
                
                resp += '        input.hide();\n'

                resp += '        if (input.val() == "noop" || input.val() == "top" || input.val() == "center") {\n'
                resp += '            select.val(input.val());\n'
                resp += '            image.parent().css({display: "none"});\n'
                resp += '        } else {\n'
                resp += '            select.val("point");\n'
                resp += '            image.parent().css({display: "inline-block"});\n'
                resp += '        }\n'

                resp += '        select.change(function(e){\n'
                resp += '            if (select.val() == "noop" || select.val() == "top" || select.val() == "center") {\n'
                resp += '                input.val(select.val());\n'
                resp += '                image.parent().css({display: "none"});\n'
                resp += '            } else {\n'
                resp += '                input.val("0, 0");\n'
                resp += '                image.parent().css({display: "inline-block"});\n'
                resp += '            }\n'
                resp += '        });\n'

                resp += '        image.parent().click(function(e){\n debugger;'
                resp += '            var nx = Math.ceil(e.pageX - image.offset().left);\n'
                resp += '            var ny = Math.ceil(e.pageY - image.offset().top);\n'
                resp += '            crosshair.css({left: (nx - 7) + "px", top: (ny - 7) + "px"});\n'
                resp += '            var x = Math.min(100, Math.floor((nx/iw) * 100));\n'
                resp += '            var y = Math.min(100, Math.floor((ny/ih) * 100));\n'
                resp += '            var val = (x < 0 ? 0 : x) + "% " + (y < 0 ? 0 : y) + "%";\n'
                resp += '            input.val(val);\n'
                resp += '        });\n'
                resp += '});\n'
                resp += '})(django.jQuery);\n'
                resp += u'</script>\n'

                lock = threading.Lock()
                with lock:
                    COUNTER += 1
                    if COUNTER > 4000000000:
                        COUNTER = 0
            except AttributeError:
                resp = 'Please save your image first'

        return mark_safe(resp)


class ImageCenterFormField(forms.Field):

    widget = ImageCenterFormWidget

    def __init__(self, **kwargs):
        kwargs['required'] = False
        super(ImageCenterFormField, self).__init__(kwargs)

    def clean(self, value):
        value = self.to_python(value)
        return value
