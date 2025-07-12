default_app_config = 'crm.apps.CrmConfig'

from .celery import app as celery_app

__all__ = ('celery_app',)
