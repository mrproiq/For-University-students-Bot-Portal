# config/celery.py
import os
from celery import Celery

# Django settings modulini default qilib belgilash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Celery app yaratish
app = Celery('config')

# Django settings ichidan CELERY_* sozlamalarni yuklash
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django app’lar ichidagi tasks.py fayllarni avtomatik topish
app.autodiscover_tasks()