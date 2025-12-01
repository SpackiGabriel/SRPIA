from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from .author import Author
from .tag import Tag


class Paper(models.Model):
    """Paper acadêmico de IA"""
    
    PRIORITY_BAIXA = 'BAIXA'
    PRIORITY_MEDIA = 'MEDIA'
    PRIORITY_ALTA = 'ALTA'
    PRIORITY_URGENTE = 'URGENTE'
    
    PRIORITY_CHOICES = [
        (PRIORITY_BAIXA, 'Baixa'),
        (PRIORITY_MEDIA, 'Média'),
        (PRIORITY_ALTA, 'Alta'),
        (PRIORITY_URGENTE, 'Urgente'),
    ]
    
    STATUS_NAO_INICIADO = 'NAO_INICIADO'
    STATUS_EM_LEITURA = 'EM_LEITURA'
    STATUS_LIDO = 'LIDO'
    STATUS_REVISANDO = 'REVISANDO'
    
    STATUS_CHOICES = [
        (STATUS_NAO_INICIADO, 'Não iniciado'),
        (STATUS_EM_LEITURA, 'Em leitura'),
        (STATUS_LIDO, 'Lido'),
        (STATUS_REVISANDO, 'Revisando'),
    ]

    title = models.CharField('Título', max_length=500)
    abstract = models.TextField('Resumo', blank=True)
    year = models.PositiveIntegerField(
        'Ano',
        null=True,
        blank=True,
        validators=[MinValueValidator(1900), MaxValueValidator(2100)]
    )
    venue = models.CharField('Venue/Conferência', max_length=300, blank=True)
    doi = models.CharField('DOI', max_length=200, blank=True)
    url = models.URLField('URL', blank=True)
    pdf_file = models.FileField('Arquivo PDF', upload_to='papers/', blank=True, null=True)
    
    priority = models.CharField(
        'Prioridade',
        max_length=10,
        choices=PRIORITY_CHOICES,
        default=PRIORITY_MEDIA
    )
    status = models.CharField(
        'Status',
        max_length=15,
        choices=STATUS_CHOICES,
        default=STATUS_NAO_INICIADO
    )
    progress_percent = models.PositiveIntegerField(
        'Progresso (%)',
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Proprietário',
        related_name='papers'
    )
    
    authors = models.ManyToManyField(
        Author,
        verbose_name='Autores',
        related_name='papers',
        blank=True
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Tags',
        related_name='papers',
        blank=True
    )

    class Meta:
        verbose_name = 'Paper'
        verbose_name_plural = 'Papers'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def priority_score(self):
        """Retorna o score base da prioridade para cálculo de ranking"""
        scores = {
            self.PRIORITY_URGENTE: 100,
            self.PRIORITY_ALTA: 70,
            self.PRIORITY_MEDIA: 40,
            self.PRIORITY_BAIXA: 10,
        }
        return scores.get(self.priority, 0)

    @property
    def is_completed(self):
        """Verifica se o paper foi completamente lido"""
        return self.status == self.STATUS_LIDO

    @property
    def total_reading_time(self):
        """Retorna o tempo total de leitura em minutos"""
        return self.reading_sessions.aggregate(
            total=models.Sum('duration_minutes')
        )['total'] or 0
