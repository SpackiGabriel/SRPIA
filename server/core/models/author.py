from django.db import models


class Author(models.Model):
    name = models.CharField('Nome', max_length=200)
    affiliation = models.CharField('Afiliação', max_length=300, blank=True)

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'
        ordering = ['name']

    def __str__(self):
        return self.name
