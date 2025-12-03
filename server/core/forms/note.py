from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import Paper, Note, ReadingSession, Experiment, Tag, Author




class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'note_type']
        labels = {
            'title': 'Título',
            'content': 'Conteúdo',
            'note_type': 'Tipo de Nota',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Principais contribuições, Pontos de melhoria...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Descreva suas observações, insights, dúvidas ou comentários...'
            }),
            'note_type': forms.Select(attrs={'class': 'form-control'}),
        }
