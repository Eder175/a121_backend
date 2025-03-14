from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns  # Importação correta

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),  # Para suportar 'javascript-catalog'
] + i18n_patterns(
    path('', include('core.urls', namespace='core')),
    prefix_default_language=False,
)
