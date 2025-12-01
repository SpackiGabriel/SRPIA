from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Papers
    path('papers/', views.PaperListView.as_view(), name='paper_list'),
    path('papers/novo/', views.PaperCreateView.as_view(), name='paper_create'),
    path('papers/<int:pk>/', views.PaperDetailView.as_view(), name='paper_detail'),
    path('papers/<int:pk>/editar/', views.PaperUpdateView.as_view(), name='paper_update'),
    path('papers/<int:pk>/excluir/', views.PaperDeleteView.as_view(), name='paper_delete'),
    
    # Notas
    path('papers/<int:paper_pk>/notas/nova/', views.NoteCreateView.as_view(), name='note_create'),
    path('notas/<int:pk>/editar/', views.NoteUpdateView.as_view(), name='note_update'),
    path('notas/<int:pk>/excluir/', views.NoteDeleteView.as_view(), name='note_delete'),
    
    # Sessões de leitura
    path('papers/<int:paper_pk>/sessoes/nova/', views.ReadingSessionCreateView.as_view(), name='session_create'),
    path('sessoes/<int:pk>/excluir/', views.ReadingSessionDeleteView.as_view(), name='session_delete'),
    
    # Experimentos
    path('experimentos/', views.ExperimentListView.as_view(), name='experiment_list'),
    path('experimentos/novo/', views.ExperimentCreateView.as_view(), name='experiment_create'),
    path('experimentos/<int:pk>/', views.ExperimentDetailView.as_view(), name='experiment_detail'),
    path('experimentos/<int:pk>/editar/', views.ExperimentUpdateView.as_view(), name='experiment_update'),
    path('experimentos/<int:pk>/excluir/', views.ExperimentDeleteView.as_view(), name='experiment_delete'),
    
    # Tags
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('tags/nova/', views.TagCreateView.as_view(), name='tag_create'),
    path('tags/<int:pk>/excluir/', views.TagDeleteView.as_view(), name='tag_delete'),
]
