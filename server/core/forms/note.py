"""
Formulários para o sistema de papers
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import Paper, Note, ReadingSession, Experiment, Tag, Author




class NoteForm(forms.ModelForm):
    """Formulário para criação e edição de notas"""
    
    class Meta:
        model = Note
        fields = ['title', 'content', 'note_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'note_type': forms.Select(attrs={'class': 'form-control'}),
        }
