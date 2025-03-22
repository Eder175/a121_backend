from django.shortcuts import render
from django.http import JsonResponse
from core.models import A121CoinSupply, A121Coin
from django.core.exceptions import ValidationError
import json

def index(request):
    return render(request, 'core/index.html')

def chat_interaction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '')

            # Lógica de resposta do A121Bot (simplificada por agora)
            response_message = "Olá! Bem-vindo à A121 Evolution! Como posso te ajudar hoje?"
            if 'curso' in message.lower():
                response_message = "Recomendo o curso de Introdução à IA! Quer saber mais?"
            elif 'olá' in message.lower() or 'oi' in message.lower():
                response_message = "Oi! Como posso te ajudar hoje?"

            # Distribuir 1 A121Coin por interação (sem usuário por agora)
            supply = A121CoinSupply.objects.first()
            if supply:
                supply.distribute(
                    amount=1.00,
                    user=None,  # Não associar a um usuário por agora
                    description="Interação com A121Bot"
                )

            return JsonResponse({
                'response': response_message,
                'a121coin_balance': float(sum(t.amount for t in A121Coin.objects.all()))
            })
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Erro ao processar a interação.'}, status=500)
    return JsonResponse({'error': 'Método não permitido.'}, status=405)