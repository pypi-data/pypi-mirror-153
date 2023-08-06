# MP-delivery

Django delivery app.

### Installation

1) Install with pip:

```
pip install django-mp-delivery
```

2) Add app to urls.py:

```
path('delivery/', include('delivery.urls')),
```

3) Add delivery settings
```
from delivery.settings import DeliverySettings

class CommonSettings(
        ...
        DeliverySettings,
        BaseSettings):
    pass
```

4) Run `python manage.py migrate`


### Model
```
from delivery.models import DeliveryMethodField
 
delivery_method = DeliveryMethodField()
```

### View
```
order.delivery_method = form.fields['delivery'].get_delivery_method()
order.address = form.fields['delivery'].get_address()
```

### Form
```
from delivery.fields import DeliveryFormField
 
class CheckoutForm(forms.ModelForm):
 
    delivery = DeliveryFormField()
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
        self.fields['delivery'].init_form(*args, **kwargs)
```

### Template
```
{{ form.delivery }}
 
 
{% block js %}
    {{ block.super }}
 
    {{ form.fields.delivery.media }}
{% endblock %}
```
