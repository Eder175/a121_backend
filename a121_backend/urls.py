from django.contrib import admin
from django.urls import path, include
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),  # Adicionando suporte para traduções JS
]
