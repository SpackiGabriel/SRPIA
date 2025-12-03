from django.db import models

from .paper import Paper


class Note(models.Model):
    
    class Type(models.TextChoices):
        INSIGHT = 'INSIGHT', 'Insight'
        CRITICA = 'CRITICA', 'Crítica'
        DUVIDA = 'DUVIDA', 'Dúvida'
        CITACAO = 'CITACAO', 'Citação'
        OUTRO = 'OUTRO', 'Outro'

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
        choices=Type.choices,
        default=Type.OUTRO
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.paper.title})"
