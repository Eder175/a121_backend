# a121_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from core.views import A121CoinTransactionViewSet, ChatInteractionAPIView

# Configuração de API RESTful para transações e interações
router = DefaultRouter()
router.register(r'transactions', A121CoinTransactionViewSet, basename='transaction')

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # URLs do aplicativo core com namespace
    path('', include('core.urls', namespace='core')),
    
    # API RESTful para transações e interações
    path('api/', include(router.urls)),
    path('api/chat-interaction/', ChatInteractionAPIView.as_view(), name='chat_interaction'),
    
    # WebSocket para interações em tempo real (chat, notificações, etc.)
    path('ws/', include('core.routing', namespace='ws')),
    
    # Service Worker para Progressive Web App (PWA)
    path('service-worker.js', TemplateView.as_view(
        template_name='service-worker.js',
        content_type='application/javascript',
    ), name='service_worker'),
    
    # Manifest para PWA
    path('manifest.json', TemplateView.as_view(
        template_name='manifest.json',
        content_type='application/json',
    ), name='manifest'),
]

# Servir arquivos estáticos e de mídia em modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Configuração para WebXR e AR (opcional, para futuras melhorias)
if hasattr(settings, 'WEBXR_ENABLED') and settings.WEBXR_ENABLED:
    urlpatterns += [
        path('webxr/', include('core.webxr_urls', namespace='webxr')),
    ]