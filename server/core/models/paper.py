from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from .author import Author
from .tag import Tag


class Paper(models.Model):
    
    class Priority(models.TextChoices):
        BAIXA = 'BAIXA', 'Baixa'
        MEDIA = 'MEDIA', 'Média'
        ALTA = 'ALTA', 'Alta'
        URGENTE = 'URGENTE', 'Urgente'
    
    class Status(models.TextChoices):
        NAO_INICIADO = 'NAO_INICIADO', 'Não iniciado'
        EM_LEITURA = 'EM_LEITURA', 'Em leitura'
        LIDO = 'LIDO', 'Lido'
        REVISANDO = 'REVISANDO', 'Revisando'

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
    total_pages = models.PositiveIntegerField(
        'Total de Páginas',
        null=True,
        blank=True,
        validators=[MinValueValidator(1)]
    )
    
    priority = models.CharField(
        'Prioridade',
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIA
    )
    status = models.CharField(
        'Status',
        max_length=15,
        choices=Status.choices,
        default=Status.NAO_INICIADO
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
            self.Priority.URGENTE: 100,
            self.Priority.ALTA: 70,
            self.Priority.MEDIA: 40,
            self.Priority.BAIXA: 10,
        }
        return scores.get(self.priority, 0)

    @property
    def is_completed(self):
        """Verifica se o paper foi completamente lido"""
        return self.status == self.Status.LIDO

    @property
    def total_reading_time(self):
        """Retorna o tempo total de leitura em minutos"""
        return self.reading_sessions.aggregate(
            total=models.Sum('duration_minutes')
        )['total'] or 0
    
    @property
    def total_pages_read(self):
        """Retorna o total de páginas lidas em todas as sessões"""
        return self.reading_sessions.aggregate(
            total=models.Sum('pages_read')
        )['total'] or 0
    
    def update_progress(self):
        """Atualiza o progresso de leitura baseado nas páginas lidas"""
        if self.total_pages and self.total_pages > 0:
            pages_read = self.total_pages_read
            self.progress_percent = min(100, int((pages_read / self.total_pages) * 100))
        else:
            self.progress_percent = 0
        self.save(update_fields=['progress_percent'])
