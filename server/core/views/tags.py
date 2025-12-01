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




class TagListView(LoginRequiredMixin, ListView):
    """Lista de tags"""
    model = Tag
    template_name = 'tags/list.html'
    context_object_name = 'tags'
    
    def get_queryset(self):
        return Tag.objects.filter(owner=self.request.user)

class TagCreateView(LoginRequiredMixin, CreateView):
    """Criação de tag"""
    model = Tag
    form_class = TagForm
    template_name = 'tags/form.html'
    success_url = reverse_lazy('tag_list')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class TagDeleteView(OwnerRequiredMixin, DeleteView):
    """Exclusão de tag"""
    model = Tag
    template_name = 'tags/confirm_delete.html'
    success_url = reverse_lazy('tag_list')
