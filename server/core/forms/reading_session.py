"""
Formulários para o sistema de papers
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import Paper, Note, ReadingSession, Experiment, Tag, Author




class ReadingSessionForm(forms.ModelForm):
    """Formulário para registro de sessões de leitura"""
    
    class Meta:
        model = ReadingSession
        fields = ['date', 'duration_minutes', 'quick_notes']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'quick_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
