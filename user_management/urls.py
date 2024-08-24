from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import *

urlpatterns = [
    path('home/register/', RegisterUser.as_view(), name='register'),
    path('home/login/', LoginUser.as_view(), name='login'),
    path('home/logout/', logout_user, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)