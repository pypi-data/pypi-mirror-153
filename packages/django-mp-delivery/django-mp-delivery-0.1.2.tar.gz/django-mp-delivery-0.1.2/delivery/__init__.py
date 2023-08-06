
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


def setup_settings(settings, is_prod, **kwargs):

    settings['DATABASES']['delivery'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mp',
        'USER': 'dev'
    }

    settings['DATABASE_ROUTERS'] = settings.get('DATABASE_ROUTERS', []) + [
        'delivery.routers.DeliveryRouter'
    ]


class DeliveryAppConfig(AppConfig):
    name = 'delivery'
    verbose_name = _('Delivery')


default_app_config = 'delivery.DeliveryAppConfig'
