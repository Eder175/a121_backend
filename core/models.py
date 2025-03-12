from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
