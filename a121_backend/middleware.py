import os
from django.http import HttpResponse, StreamingHttpResponse
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import re

class NgrokHostMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'HTTP_HOST' in request.META:
            host = request.META['HTTP_HOST']
            if 'ngrok' in host.lower():
                request.META['HTTP_HOST'] = '127.0.0.1:8000'
        return None

class RangeFileMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if not isinstance(response, StreamingHttpResponse) or not hasattr(response, 'file_to_stream'):
            return response
        
        file = response.file_to_stream
        if not os.path.exists(file.name):
            return HttpResponse(status=404, content="Arquivo não encontrado.")
        
        file_size = os.path.getsize(file.name)
        range_header = request.META.get('HTTP_RANGE', '').strip()
        range_match = re.match(r'bytes=(\d+)-(\d*)', range_header)
        
        if range_match:
            start = int(range_match.group(1))
            end = range_match.group(2)
            end = int(end) if end else file_size - 1
            
            if start >= file_size or end >= file_size or start > end:
                response = HttpResponse(status=416)
                response['Content-Range'] = f'bytes */{file_size}'
                return response
            
            chunk_size = end - start + 1
            response.status_code = 206
            response['Content-Length'] = str(chunk_size)
            response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
            response['Accept-Ranges'] = 'bytes'
            
            def stream_file():
                with open(file.name, 'rb') as f:
                    f.seek(start)
                    remaining = chunk_size
                    while remaining > 0:
                        chunk = f.read(min(8192, remaining))
                        if not chunk:
                            break
                        yield chunk
                        remaining -= len(chunk)
            
            response.streaming_content = stream_file()
        else:
            response['Accept-Ranges'] = 'bytes'
            response['Content-Length'] = str(file_size)
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file.name)}"'
        
        return response