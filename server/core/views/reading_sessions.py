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
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)




class ReadingSessionCreateView(LoginRequiredMixin, CreateView):
    model = ReadingSession
    form_class = ReadingSessionForm
    template_name = 'sessions/form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paper'] = get_object_or_404(Paper, pk=self.kwargs['paper_pk'], owner=self.request.user)
        return context
    
    def form_valid(self, form):
        paper = get_object_or_404(Paper, pk=self.kwargs['paper_pk'], owner=self.request.user)
        form.instance.paper = paper
        response = super().form_valid(form)
        
        # Atualiza o progresso do paper
        paper.update_progress()
        
        messages.success(self.request, 'Sessão de leitura registrada com sucesso!')
        return response
    
    def get_success_url(self):
        return reverse_lazy('paper_detail', kwargs={'pk': self.object.paper.pk})

class ReadingSessionDeleteView(LoginRequiredMixin, DeleteView):
    model = ReadingSession
    template_name = 'sessions/confirm_delete.html'
    
    def get_queryset(self):
        return ReadingSession.objects.filter(paper__owner=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paper'] = self.object.paper
        return context
    
    def form_valid(self, form):
        paper = self.object.paper
        response = super().form_valid(form)
        
        # Atualiza o progresso do paper
        paper.update_progress()
        
        messages.success(self.request, 'Sessão de leitura excluída com sucesso!')
        return response
    
    def get_success_url(self):
        return reverse_lazy('paper_detail', kwargs={'pk': self.object.paper.pk})
