"""
Formulários para o sistema de papers
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import Paper, Note, ReadingSession, Experiment, Tag, Author




class PaperForm(forms.ModelForm):
    """Formulário para criação e edição de papers"""
    
    authors_text = forms.CharField(
        label='Autores (separe por vírgula)',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Ex: João Silva, Maria Santos, Pedro Costa'
        }),
        help_text='Digite os nomes dos autores separados por vírgula'
    )
    
    class Meta:
        model = Paper
        fields = ['title', 'abstract', 'year', 'venue', 'doi', 'url', 'pdf_file', 'tags', 'priority', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'venue': forms.TextInput(attrs={'class': 'form-control'}),
            'doi': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-control'}),
            'tags': forms.CheckboxSelectMultiple(),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filtrar tags por owner
        if user:
            self.fields['tags'].queryset = Tag.objects.filter(owner=user)
        
        # Popular campo authors_text se estiver editando
        if self.instance.pk:
            authors = self.instance.authors.all()
            if authors:
                self.initial['authors_text'] = ', '.join([author.name for author in authors])
    
    def save(self, commit=True):
        paper = super().save(commit=commit)
        
        if commit:
            # Processar autores
            authors_text = self.cleaned_data.get('authors_text', '')
            if authors_text:
                # Limpar autores existentes
                paper.authors.clear()
                
                # Criar/obter autores
                author_names = [name.strip() for name in authors_text.split(',') if name.strip()]
                for author_name in author_names:
                    author, created = Author.objects.get_or_create(name=author_name)
                    paper.authors.add(author)
        
        return paper
