from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.exceptions import DisallowedHost
import os
import logging

# Configurar logging para debug
logger = logging.getLogger(__name__)

class RangeFileMiddleware:
    """Middleware avançado para suportar streaming de vídeos com requisições Range."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar se é uma requisição de arquivo estático com Range
        if request.path.startswith('/static/') and 'Range' in request.headers:
            range_header = request.headers['Range']
            file_path = request.path[1:]  # Remove a barra inicial
            logger.debug(f"Requisição Range para: {file_path}")

            if default_storage.exists(file_path):
                file_size = default_storage.size(file_path)
                start, end = self.parse_range_header(range_header, file_size)

                if start is not None and end is not None:
                    try:
                        with default_storage.open(file_path, 'rb') as f:
                            f.seek(start)
                            data = f.read(end - start + 1)
                            response = HttpResponse(
                                data,
                                status=206,
                                content_type='video/mp4'
                            )
                            response['Content-Length'] = str(len(data))
                            response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
                            response['Accept-Ranges'] = 'bytes'
                            logger.info(f"Servindo {file_path} de {start} a {end}")
                            return response
                    except Exception as e:
                        logger.error(f"Erro ao servir arquivo: {e}")
                        return HttpResponse(status=500)
            else:
                logger.warning(f"Arquivo não encontrado: {file_path}")
                return HttpResponse(status=404)

        # Passar para o próximo middleware
        return self.get_response(request)

    def parse_range_header(self, range_header, file_size):
        """Analisar o cabeçalho Range de forma robusta."""
        try:
            if not range_header.startswith('bytes='):
                return None, None
            range_value = range_header.split('=')[1].split('-')
            start = int(range_value[0]) if range_value[0] else 0
            end = int(range_value[1]) if range_value[1] else file_size - 1
            if end >= file_size:
                end = file_size - 1
            if start > end or start < 0:
                return None, None
            return start, end
        except (IndexError, ValueError) as e:
            logger.error(f"Erro ao parsear Range header: {e}")
            return None, None

class NgrokHostMiddleware:
    """Middleware otimizado para suportar hosts dinâmicos como Ngrok."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            host = request.get_host()
            logger.debug(f"Host detectado: {host}")
            from django.conf import settings

            # Adicionar hosts Ngrok dinamicamente
            if host.endswith('.ngrok-free.app') and host not in settings.ALLOWED_HOSTS:
                settings.ALLOWED_HOSTS.append(host)
                logger.info(f"Host Ngrok adicionado: {host}")

            response = self.get_response(request)
            return response
        except DisallowedHost as e:
            logger.error(f"Host inválido: {e}")
            raise DisallowedHost(f"Host inválido detectado: {request.META.get('HTTP_HOST', '')}")
        except Exception as e:
            logger.error(f"Erro no NgrokHostMiddleware: {e}")
            return HttpResponse(status=500)