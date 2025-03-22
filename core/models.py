from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from core.blockchain import A121Blockchain
import json
import hashlib
from django.core.mail import send_mail
from django.conf import settings

# Inicializar a blockchain
blockchain = A121Blockchain()

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField(default=0)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class Venda(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    country = models.CharField(max_length=100)
    data = models.DateTimeField(default=timezone.now)
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=None)

    def __str__(self):
        return f"Venda de {self.quantidade} {self.produto.nome} por {self.vendedor.username if self.vendedor else 'Desconhecido'}"

class Nivel(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    pontos_necessarios = models.IntegerField(default=0)
    bonus_percentual = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return self.nome

class UsuarioMNM(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nivel = models.ForeignKey(Nivel, on_delete=models.SET_NULL, null=True, blank=True)
    pontos = models.IntegerField(default=0)
    upline = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='downlines')
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.usuario.username} - {self.nivel}"

class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    categoria = models.CharField(max_length=100, choices=[
        ('IA', 'Inteligência Artificial'),
        ('FIN', 'Finanças'),
        ('LEI', 'Leilões Mundiais'),
        ('STA', 'Startups')
    ])
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    duracao_horas = models.IntegerField()
    certificado = models.BooleanField(default=True)
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo

class InscricaoCurso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    data_inscricao = models.DateTimeField(default=timezone.now)
    concluido = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario.username} - {self.curso.titulo}"

class A121Coin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    transaction_type = models.CharField(
        max_length=20,
        choices=[
            ('REWARD', 'Reward'),
            ('TRANSFER', 'Transfer'),
            ('INITIAL', 'Initial Supply'),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)
    transaction_hash = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Registrar a transação na blockchain
        user_id = str(self.user.id) if self.user else "system"
        transaction = {
            'sender': "system",
            'receiver': user_id,
            'amount': float(self.amount),
            'description': self.description,
            'timestamp': self.created_at.timestamp()
        }
        blockchain.add_transaction(transaction)
        block = blockchain.mine_pending_transactions()
        if block:
            self.transaction_hash = block.hash
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username if self.user else 'System'} - {self.amount} A121Coin ({self.transaction_type})"

class A121CoinSupply(models.Model):
    total_supply = models.DecimalField(max_digits=20, decimal_places=2, default=21000000.00)  # 21 milhões
    circulating_supply = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk and A121CoinSupply.objects.exists():
            raise ValidationError("Apenas uma instância de A121CoinSupply pode existir.")
        super().save(*args, **kwargs)

    def can_distribute(self, amount):
        return (self.total_supply - self.circulating_supply) >= amount

    def distribute(self, amount, user=None, description=""):
        if not self.can_distribute(amount):
            raise ValidationError("Fornecimento insuficiente para distribuir essa quantidade de A121Coin.")
        
        self.circulating_supply += amount
        self.save()

        # Registrar a transação
        A121Coin.objects.create(
            user=user,
            amount=amount,
            transaction_type='REWARD',
            description=description
        )

    def __str__(self):
        return f"Total Supply: {self.total_supply}, Circulating: {self.circulating_supply}"

# Novo modelo para transações de A121Coin
class A121CoinTransaction(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions', null=True, blank=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transactions', null=True, blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transaction_hash = models.CharField(max_length=64, blank=True)
    notified = models.BooleanField(default=False)  # Para rastrear notificações

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Validar a transação
        if self.amount <= 0:
            raise ValidationError("O valor da transação deve ser maior que zero.")

        # Verificar saldo do remetente, se aplicável
        if self.sender:
            sender_balance = A121Coin.objects.filter(user=self.sender).aggregate(
                total=models.Sum('amount')
            )['total'] or 0
            if sender_balance < self.amount:
                raise ValidationError("Saldo insuficiente para realizar a transação.")

        # Registrar a transação na blockchain
        sender_id = str(self.sender.id) if self.sender else "system"
        receiver_id = str(self.receiver.id) if self.receiver else "system"
        transaction_data = {
            'sender': sender_id,
            'receiver': receiver_id,
            'amount': float(self.amount),
            'description': self.description,
            'timestamp': self.created_at.timestamp()
        }
        blockchain.add_transaction(transaction_data)
        block = blockchain.mine_pending_transactions()
        if block:
            self.transaction_hash = block.hash
            self.status = 'COMPLETED'
        else:
            self.status = 'FAILED'

        # Atualizar saldos
        if self.status == 'COMPLETED':
            if self.sender:
                A121Coin.objects.create(
                    user=self.sender,
                    amount=-self.amount,
                    transaction_type='TRANSFER',
                    description=f"Transferência para {receiver_id}",
                    transaction_hash=self.transaction_hash
                )
            if self.receiver:
                A121Coin.objects.create(
                    user=self.receiver,
                    amount=self.amount,
                    transaction_type='TRANSFER',
                    description=f"Recebido de {sender_id}",
                    transaction_hash=self.transaction_hash
                )

        super().save(*args, **kwargs)

        # Registrar no log de transações
        A121CoinTransactionLog.objects.create(
            transaction=self,
            status=self.status,
            details=json.dumps(transaction_data)
        )

        # Enviar notificação ao usuário (se configurado)
        if not self.notified and self.status == 'COMPLETED' and self.receiver:
            self.send_notification()

    def send_notification(self):
        if not self.receiver:
            return

        subject = "Nova Transação de A121Coin Recebida"
        message = (
            f"Olá {self.receiver.username},\n\n"
            f"Você recebeu {self.amount} A121Coin!\n"
            f"Detalhes:\n"
            f"- De: {self.sender.username if self.sender else 'Sistema'}\n"
            f"- Descrição: {self.description}\n"
            f"- Data: {self.created_at}\n"
            f"- Hash da Transação: {self.transaction_hash}\n\n"
            f"Obrigado por usar o A121Coin!"
        )
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [self.receiver.email],
                fail_silently=True,
            )
            self.notified = True
            self.save(update_fields=['notified'])
        except Exception as e:
            print(f"Falha ao enviar notificação: {e}")

    def __str__(self):
        return f"Transação de {self.amount} A121Coin: {self.sender.username if self.sender else 'System'} -> {self.receiver.username if self.receiver else 'System'} ({self.status})"

# Modelo para auditoria de transações
class A121CoinTransactionLog(models.Model):
    transaction = models.ForeignKey(A121CoinTransaction, on_delete=models.CASCADE, related_name='logs')
    status = models.CharField(max_length=20, choices=A121CoinTransaction.STATUS_CHOICES)
    details = models.TextField()  # Armazena os dados da transação em JSON
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log de Transação #{self.transaction.id} - {self.status}"