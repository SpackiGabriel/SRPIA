from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField('Nome', max_length=100)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Proprietário',
        related_name='tags'
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']
        unique_together = [['name', 'owner']]

    def __str__(self):
        return self.name
