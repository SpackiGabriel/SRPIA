from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.urls import reverse_lazy
from django.db.models import Q, Count

from ..models import Paper, Note, ReadingSession, Experiment, Tag
from core.forms import (
    PaperForm, NoteForm, ReadingSessionForm, ExperimentForm,
    TagForm, PaperSearchForm
)
from ..services import RankingService


class OwnerRequiredMixin(LoginRequiredMixin):
    """Mixin para garantir que apenas o owner acessa o objeto"""
    
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)




class NoteCreateView(LoginRequiredMixin, CreateView):
    """Criação de nota para um paper"""
    model = Note
    form_class = NoteForm
    template_name = 'notes/form.html'
    
    def form_valid(self, form):
        paper = get_object_or_404(Paper, pk=self.kwargs['paper_pk'])
        form.instance.paper = paper
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('paper_detail', kwargs={'pk': self.object.paper.pk})

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    """Edição de nota"""
    model = Note
    form_class = NoteForm
    template_name = 'notes/form.html'
    
    def get_success_url(self):
        return reverse_lazy('paper_detail', kwargs={'pk': self.object.paper.pk})

class NoteDeleteView(LoginRequiredMixin, DeleteView):
    """Exclusão de nota"""
    model = Note
    template_name = 'notes/confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('paper_detail', kwargs={'pk': self.object.paper.pk})
