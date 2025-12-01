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




class PaperListView(LoginRequiredMixin, ListView):
    model = Paper
    template_name = 'papers/list.html'
    context_object_name = 'papers'
    paginate_by = 20
    
    def get_queryset(self):
        return Paper.objects.filter(owner=self.request.user)

class PaperDetailView(OwnerRequiredMixin, DetailView):
    model = Paper
    template_name = 'papers/detail.html'
    context_object_name = 'paper'

class PaperCreateView(LoginRequiredMixin, CreateView):
    model = Paper
    form_class = PaperForm
    template_name = 'papers/form.html'
    success_url = reverse_lazy('paper_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class PaperUpdateView(OwnerRequiredMixin, UpdateView):
    model = Paper
    form_class = PaperForm
    template_name = 'papers/form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_url(self):
        return reverse_lazy('paper_detail', kwargs={'pk': self.object.pk})

class PaperDeleteView(OwnerRequiredMixin, DeleteView):
    model = Paper
    template_name = 'papers/confirm_delete.html'
    success_url = reverse_lazy('paper_list')
