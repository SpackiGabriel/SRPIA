from django.db import models
from django.contrib.auth.models import User

from .paper import Paper


class Experiment(models.Model):
    """Experimento relacionado a papers"""
    
    STATUS_PLANEJADO = 'PLANEJADO'
    STATUS_EM_EXECUCAO = 'EM_EXECUCAO'
    STATUS_CONCLUIDO = 'CONCLUIDO'
    STATUS_ABORTADO = 'ABORTADO'
    
    STATUS_CHOICES = [
        (STATUS_PLANEJADO, 'Planejado'),
        (STATUS_EM_EXECUCAO, 'Em execução'),
        (STATUS_CONCLUIDO, 'Concluído'),
        (STATUS_ABORTADO, 'Abortado'),
    ]

    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descrição')
    code_repository_url = models.URLField('URL do repositório', blank=True)
    dataset_description = models.TextField('Descrição do dataset', blank=True)
    status = models.CharField(
        'Status',
        max_length=15,
        choices=STATUS_CHOICES,
        default=STATUS_PLANEJADO
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
