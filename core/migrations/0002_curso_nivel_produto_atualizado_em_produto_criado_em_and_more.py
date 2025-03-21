# Generated by Django 5.1.6 on 2025-03-12 13:44

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descricao', models.TextField()),
                ('categoria', models.CharField(choices=[('IA', 'Inteligência Artificial'), ('FIN', 'Finanças'), ('LEI', 'Leilões Mundiais'), ('STA', 'Startups')], max_length=100)),
                ('preco', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('duracao_horas', models.IntegerField()),
                ('certificado', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Nivel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, unique=True)),
                ('pontos_necessarios', models.IntegerField(default=0)),
                ('bonus_percentual', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
            ],
        ),
        migrations.AddField(
            model_name='produto',
            name='atualizado_em',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='criado_em',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='venda',
            name='vendedor',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='produto',
            name='estoque',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='venda',
            name='data',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name='InscricaoCurso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_inscricao', models.DateTimeField(default=django.utils.timezone.now)),
                ('concluido', models.BooleanField(default=False)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.curso')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioMNM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pontos', models.IntegerField(default=0)),
                ('criado_em', models.DateTimeField(default=django.utils.timezone.now)),
                ('nivel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.nivel')),
                ('upline', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='downlines', to='core.usuariomnm')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
