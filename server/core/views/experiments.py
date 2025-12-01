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




class ExperimentListView(LoginRequiredMixin, ListView):
    model = Experiment
    template_name = 'experiments/list.html'
    context_object_name = 'experiments'
    paginate_by = 20
    
    def get_queryset(self):
        return Experiment.objects.filter(owner=self.request.user)

class ExperimentDetailView(OwnerRequiredMixin, DetailView):
    model = Experiment
    template_name = 'experiments/detail.html'
    context_object_name = 'experiment'

class ExperimentCreateView(LoginRequiredMixin, CreateView):
    model = Experiment
    form_class = ExperimentForm
    template_name = 'experiments/form.html'
    success_url = reverse_lazy('experiment_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ExperimentUpdateView(OwnerRequiredMixin, UpdateView):
    model = Experiment
    form_class = ExperimentForm
    template_name = 'experiments/form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class ExperimentDeleteView(OwnerRequiredMixin, DeleteView):
    model = Experiment
    template_name = 'experiments/confirm_delete.html'
    success_url = reverse_lazy('experiment_list')
