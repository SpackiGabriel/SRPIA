from django.db import models

from .paper import Paper


class RankingEntry(models.Model):
    paper = models.OneToOneField(
        Paper,
        on_delete=models.CASCADE,
        verbose_name='Paper',
        related_name='ranking_entry'
    )
    score = models.FloatField('Score', default=0.0)
    last_recommended_at = models.DateTimeField(
        'Última recomendação',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Entrada de ranking'
        verbose_name_plural = 'Entradas de ranking'
        ordering = ['-score']

    def __str__(self):
        return f"{self.paper.title} - Score: {self.score}"
