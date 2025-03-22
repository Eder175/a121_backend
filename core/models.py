from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from core.blockchain import A121Blockchain
import json

# Inicializar a blockchain
blockchain = A121Blockchain()

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField(default=0)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    criado_em = models.DateTimeField(default=timezone.now)  # Default fixo para dados existentes
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class Venda(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    country = models.CharField(max_length=100)
    data = models.DateTimeField(default=timezone.now)  # Default fixo
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=None)  # Permite null para dados existentes

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
        # Garantir que apenas uma instância exista
        if not self.pk and A121CoinSupply.objects.exists():
            raise ValidationError("Apenas uma instância de A121CoinSupply pode existir.")
        super().save(*args, **kwargs)

    def can_distribute(self, amount):
        """Verifica se há moedas suficientes para distribuir."""
        return (self.total_supply - self.circulating_supply) >= amount

    def distribute(self, amount, user=None, description=""):
        """Distribui moedas, se possível."""
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