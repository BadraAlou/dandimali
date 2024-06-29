from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

                  path('admin/', admin.site.urls),
                  path('', include('dandiApp.urls')),
                  path('gestionapp/', include('gestionapp.urls')),  # Inclure les URLs de votre deuxième application ici
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
