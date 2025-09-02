from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('desire_moda_feminina.urls')),
    path('vestidos/', include('vestidos.urls')),
    path('blusas/', include('blusas.urls')),
    path('calcas/', include('calcas.urls')),
    path('roupa_intima/', include('roupa_intima.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
