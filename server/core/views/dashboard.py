from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from core.models import Paper
from core.services import RankingService



class DashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal com progresso e próximos papers recomendados"""
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Estatísticas gerais
        total_papers = Paper.objects.filter(owner=user).count()
        papers_nao_iniciados = Paper.objects.filter(
            owner=user, status=Paper.STATUS_NAO_INICIADO
        ).count()
        papers_em_leitura = Paper.objects.filter(
            owner=user, status=Paper.STATUS_EM_LEITURA
        ).count()
        papers_lidos = Paper.objects.filter(
            owner=user, status=Paper.STATUS_LIDO
        ).count()
        papers_revisando = Paper.objects.filter(
            owner=user, status=Paper.STATUS_REVISANDO
        ).count()
        
        # Próximos papers recomendados
        next_papers = RankingService.get_next_to_read(user, count=5)
        
        context.update({
            'total_papers': total_papers,
            'papers_nao_iniciados': papers_nao_iniciados,
            'papers_em_leitura': papers_em_leitura,
            'papers_lidos': papers_lidos,
            'papers_revisando': papers_revisando,
            'next_papers': next_papers,
        })
        
        return context
