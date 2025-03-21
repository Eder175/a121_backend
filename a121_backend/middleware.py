from django.core.exceptions import DisallowedHost

class NgrokHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Tenta obter o host da requisição
            host = request.get_host()
        except DisallowedHost:
            # Captura o erro se o host não estiver em ALLOWED_HOSTS
            host = request.META.get('HTTP_HOST', '')
            
            # Verifica se o host é um domínio do Ngrok
            if host.endswith('.ngrok-free.app'):
                # Adiciona o host dinamicamente ao ALLOWED_HOSTS
                from django.conf import settings
                if host not in settings.ALLOWED_HOSTS:
                    settings.ALLOWED_HOSTS.append(host)
            else:
                # Se não for um domínio do Ngrok, levanta o erro novamente
                raise DisallowedHost(f"Invalid host: {host}")

        # Continua o processamento da requisição
        response = self.get_response(request)
        return response