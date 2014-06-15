Description
===========

This project makes it possible to choose how an image will be cropped by [sorl-thumbnail](https://github.com/mariocesar/sorl-thumbnail). Choosing Noop, Top, Center, etc and also a widget to choose the Point Of Interest of an image.

Thanks to [francescortiz/image](https://github.com/francescortiz/image) where this is based from.


![image example](https://www.dropbox.com/s/0mf047cgguns5h2/Screenshot%202014-06-15%2012.58.34.png?dl=1)


## Examples

Sample model:

```python
from imagepoi.fields import ImageCenterField

class Test(models.Model):
    image = ImageField(upload_to="test")
    image_center = ImageCenterField(image_field=image)
```

Sample urls.py:

```python
from django.conf.urls import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/imagepoi/', include('imagepoi.urls')),
)
```

Sample template:

```html
{% thumbnail item.image "100x86" crop=item.image_center.value as im %}
    <img src="{{ im.url }}" alt="{{ item.description }}" />
{% endthumbnail %}
```