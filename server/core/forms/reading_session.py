from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import Paper, Note, ReadingSession, Experiment, Tag, Author




class ReadingSessionForm(forms.ModelForm):
    class Meta:
        model = ReadingSession
        fields = ['date', 'duration_minutes', 'pages_read', 'quick_notes']
        labels = {
            'date': 'Data',
            'duration_minutes': 'Duração (minutos)',
            'pages_read': 'Páginas lidas',
            'quick_notes': 'Notas rápidas',
        }
        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'duration_minutes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Ex: 30'
            }),
            'pages_read': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Número de páginas lidas nesta sessão'
            }),
            'quick_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Suas observações sobre esta sessão de leitura...'
            }),
        }
