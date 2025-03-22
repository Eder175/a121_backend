from django.http import HttpResponse
from django.core.files.storage import default_storage
import os

class RangeFileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith('/static/') and 'Range' in request.headers:
            range_header = request.headers['Range']
            file_path = request.path[1:]  # Remove a barra inicial
            if default_storage.exists(file_path):
                file_size = default_storage.size(file_path)
                start, end = self.parse_range_header(range_header, file_size)

                if start is not None and end is not None:
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
                        return response

        return response

    def parse_range_header(self, range_header, file_size):
        try:
            range_value = range_header.split('=')[1]
            start, end = range_value.split('-')
            start = int(start) if start else 0
            end = int(end) if end else file_size - 1
            if end >= file_size:
                end = file_size - 1
            return start, end
        except (IndexError, ValueError):
            return None, None

# Middleware existente
from django.core.exceptions import DisallowedHost

class NgrokHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            host = request.get_host()
        except DisallowedHost:
            host = request.META.get('HTTP_HOST', '')
            if host.endswith('.ngrok-free.app'):
                from django.conf import settings
                if host not in settings.ALLOWED_HOSTS:
                    settings.ALLOWED_HOSTS.append(host)
            else:
                raise DisallowedHost(f"Invalid host: {host}")
        response = self.get_response(request)
        return response