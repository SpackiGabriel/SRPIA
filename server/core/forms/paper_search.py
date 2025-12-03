from django import forms
from core.models import Paper, Tag


class PaperSearchForm(forms.Form):
    q = forms.CharField(
        label='Buscar',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por título, resumo, autores...'
        })
    )
    
    priority = forms.ChoiceField(
        label='Prioridade',
        required=False,
        choices=[('', 'Todas')] + Paper.PRIORITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    status = forms.ChoiceField(
        label='Status',
        required=False,
        choices=[('', 'Todos')] + Paper.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    tag = forms.ModelChoiceField(
        label='Tag',
        required=False,
        queryset=Tag.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Todas'
    )
    
    year = forms.IntegerField(
        label='Ano',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 2023'})
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['tag'].queryset = Tag.objects.filter(owner=user)
