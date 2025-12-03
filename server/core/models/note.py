from django.db import models

from .paper import Paper


class Note(models.Model):
    TYPE_INSIGHT = 'INSIGHT'
    TYPE_CRITICA = 'CRITICA'
    TYPE_DUVIDA = 'DUVIDA'
    TYPE_CITACAO = 'CITACAO'
    TYPE_OUTRO = 'OUTRO'
    
    TYPE_CHOICES = [
        (TYPE_INSIGHT, 'Insight'),
        (TYPE_CRITICA, 'Crítica'),
        (TYPE_DUVIDA, 'Dúvida'),
        (TYPE_CITACAO, 'Citação'),
        (TYPE_OUTRO, 'Outro'),
    ]

    paper = models.ForeignKey(
        Paper,
        on_delete=models.CASCADE,
        verbose_name='Paper',
        related_name='notes'
    )
    title = models.CharField('Título', max_length=200)
    content = models.TextField('Conteúdo')
    note_type = models.CharField(
        'Tipo',
        max_length=10,
        choices=TYPE_CHOICES,
        default=TYPE_OUTRO
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.paper.title})"
