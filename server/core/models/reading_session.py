from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

from .paper import Paper


class ReadingSession(models.Model):
    """Sessão de leitura de um paper"""
    paper = models.ForeignKey(
        Paper,
        on_delete=models.CASCADE,
        verbose_name='Paper',
        related_name='reading_sessions'
    )
    date = models.DateField('Data', default=timezone.now)
    duration_minutes = models.PositiveIntegerField(
        'Duração (minutos)',
        validators=[MinValueValidator(1)]
    )
    quick_notes = models.TextField('Notas rápidas', blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Sessão de leitura'
        verbose_name_plural = 'Sessões de leitura'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.paper.title} - {self.date}"
