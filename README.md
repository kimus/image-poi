image-poi
=========

Add Point Of Interest Field for supporting sorl-thumbnail.

Thanks to [francescortiz/image](https://github.com/francescortiz/image) where this is based from.


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