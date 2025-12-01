"""
Formulários para o sistema de papers
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import Paper, Note, ReadingSession, Experiment, Tag, Author




class ExperimentForm(forms.ModelForm):
    """Formulário para criação e edição de experimentos"""
    
    class Meta:
        model = Experiment
        fields = ['title', 'description', 'dataset_description', 'main_results', 'status', 'code_repository_url', 'papers']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'dataset_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'main_results': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'code_repository_url': forms.URLInput(attrs={'class': 'form-control'}),
            'papers': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['papers'].queryset = Paper.objects.filter(owner=user)
