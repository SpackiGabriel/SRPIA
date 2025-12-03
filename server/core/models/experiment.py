from django.db import models
from django.contrib.auth.models import User

from .paper import Paper


class Experiment(models.Model):
    
    class Status(models.TextChoices):
        PLANEJADO = 'PLANEJADO', 'Planejado'
        EM_EXECUCAO = 'EM_EXECUCAO', 'Em execução'
        CONCLUIDO = 'CONCLUIDO', 'Concluído'
        ABORTADO = 'ABORTADO', 'Abortado'

    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descrição')
    code_repository_url = models.URLField('URL do repositório', blank=True)
    dataset_description = models.TextField('Descrição do dataset', blank=True)
    status = models.CharField(
        'Status',
        max_length=15,
        choices=Status.choices,
        default=Status.PLANEJADO
    )
    main_results = models.TextField('Principais resultados', blank=True)
    
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Proprietário',
        related_name='experiments'
    )
    papers = models.ManyToManyField(
        Paper,
        verbose_name='Papers relacionados',
        related_name='experiments',
        blank=True
    )
    
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Experimento'
        verbose_name_plural = 'Experimentos'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
