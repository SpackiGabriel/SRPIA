"""
Template tags para geração automática de breadcrumbs no SRPIA.
"""
from django import template
from django.urls import reverse, resolve, Resolver404
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


# Mapeamento de nomes de views para títulos legíveis
BREADCRUMB_TITLES = {
    'dashboard': 'Dashboard',
    
    # Papers
    'paper_list': 'Papers',
    'paper_create': 'Novo Paper',
    'paper_detail': 'Detalhes',
    'paper_update': 'Editar',
    'paper_delete': 'Excluir',
    
    # Experiments
    'experiment_list': 'Experimentos',
    'experiment_create': 'Novo Experimento',
    'experiment_detail': 'Detalhes',
    'experiment_update': 'Editar',
    'experiment_delete': 'Excluir',
    
    # Tags
    'tag_list': 'Tags',
    'tag_create': 'Nova Tag',
    'tag_update': 'Editar',
    'tag_delete': 'Excluir',
    
    # Notes
    'note_create': 'Nova Nota',
    'note_update': 'Editar Nota',
    'note_delete': 'Excluir Nota',
    
    # Sessions
    'session_create': 'Nova Sessão',
    'session_delete': 'Excluir Sessão',
    
    # Auth
    'login': 'Login',
    'logout': 'Logout',
    'register': 'Registrar',
}


# Mapeamento de hierarquia de breadcrumbs
BREADCRUMB_HIERARCHY = {
    # Papers
    'paper_create': ['dashboard', 'paper_list'],
    'paper_detail': ['dashboard', 'paper_list'],
    'paper_update': ['dashboard', 'paper_list', 'paper_detail'],
    'paper_delete': ['dashboard', 'paper_list', 'paper_detail'],
    
    # Experiments
    'experiment_create': ['dashboard', 'experiment_list'],
    'experiment_detail': ['dashboard', 'experiment_list'],
    'experiment_update': ['dashboard', 'experiment_list', 'experiment_detail'],
    'experiment_delete': ['dashboard', 'experiment_list', 'experiment_detail'],
    
    # Tags
    'tag_create': ['dashboard', 'tag_list'],
    'tag_update': ['dashboard', 'tag_list'],
    'tag_delete': ['dashboard', 'tag_list'],
    
    # Notes
    'note_create': ['dashboard', 'paper_list', 'paper_detail'],
    'note_update': ['dashboard', 'paper_list', 'paper_detail'],
    'note_delete': ['dashboard', 'paper_list', 'paper_detail'],
    
    # Sessions
    'session_create': ['dashboard', 'paper_list', 'paper_detail'],
    'session_delete': ['dashboard', 'paper_list', 'paper_detail'],
    
    # Lists
    'paper_list': ['dashboard'],
    'experiment_list': ['dashboard'],
    'tag_list': ['dashboard'],
}


@register.inclusion_tag('shared/includes/breadcrumb.html', takes_context=True)
def render_breadcrumbs(context, custom_items=None):
    """
    Renderiza breadcrumbs automaticamente baseado na view atual.
    
    Uso:
        {% load breadcrumbs %}
        {% render_breadcrumbs %}
    
    Uso com itens customizados:
        {% render_breadcrumbs custom_items=custom_breadcrumbs %}
    """
    request = context.get('request')
    if not request:
        return {'items': []}
    
    # Se itens customizados foram fornecidos, use-os
    if custom_items:
        return {'items': custom_items}
    
    # Resolver a view atual
    try:
        resolved = resolve(request.path)
        view_name = resolved.url_name
    except (Resolver404, AttributeError):
        return {'items': []}
    
    # Construir lista de breadcrumbs
    items = []
    
    # Adicionar Home (Dashboard) com ícone
    items.append({
        'url': reverse('dashboard'),
        'title': 'Dashboard',
        'icon': 'bi-house',
        'active': view_name == 'dashboard'
    })
    
    # Se não for dashboard, adicionar hierarquia
    if view_name != 'dashboard':
        hierarchy = BREADCRUMB_HIERARCHY.get(view_name, [])
        
        # Adicionar itens da hierarquia
        for parent_view in hierarchy:
            if parent_view == 'dashboard':
                continue  # Já adicionado
            
            # Tentar construir URL
            url = None
            try:
                # Para views de detail/update/delete, precisamos do ID
                if parent_view in ['paper_detail', 'experiment_detail']:
                    obj_id = context.get('object') or context.get('paper') or context.get('experiment')
                    if obj_id and hasattr(obj_id, 'pk'):
                        url = reverse(parent_view, kwargs={'pk': obj_id.pk})
                else:
                    url = reverse(parent_view)
            except Exception:
                url = None
            
            items.append({
                'url': url,
                'title': BREADCRUMB_TITLES.get(parent_view, parent_view.replace('_', ' ').title()),
                'icon': None,
                'active': False
            })
        
        # Adicionar item atual (ativo)
        current_title = BREADCRUMB_TITLES.get(view_name, view_name.replace('_', ' ').title())
        
        # Para views de detail, tentar usar o título do objeto
        if view_name in ['paper_detail', 'experiment_detail']:
            obj = context.get('object') or context.get('paper') or context.get('experiment')
            if obj and hasattr(obj, 'title'):
                from django.template.defaultfilters import truncatewords
                current_title = truncatewords(obj.title, 5)
        
        items.append({
            'url': None,
            'title': current_title,
            'icon': None,
            'active': True
        })
    
    return {'items': items}


@register.simple_tag(takes_context=True)
def breadcrumb_title(context, view_name):
    """
    Retorna o título de um breadcrumb baseado no nome da view.
    
    Uso:
        {% breadcrumb_title 'paper_list' %}
    """
    return BREADCRUMB_TITLES.get(view_name, view_name.replace('_', ' ').title())
