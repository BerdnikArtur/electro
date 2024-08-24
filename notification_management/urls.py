from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings

from .views import *

urlpatterns = [
    path('api/ajax-newsletter/', newsletter, name='newsletter'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)