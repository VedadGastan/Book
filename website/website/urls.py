from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from app.urls import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
