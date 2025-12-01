"""
Serviços de lógica de negócio para o sistema de papers
"""
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q, F, Max
from .models import Paper, RankingEntry


class RankingService:
    """Serviço responsável pelo cálculo e gestão do ranking de papers"""
    
    # Penalizações e bônus
    PENALTY_LIDO = -80
    PENALTY_REVISANDO = -50
    BONUS_NOVO_PAPER_DAYS = 7
    BONUS_NOVO_PAPER = 20
    PENALTY_RECENTE_DIAS = 3
    PENALTY_RECENTE = -30
    
    @classmethod
    def calculate_score(cls, paper):
        """
        Calcula o score de um paper para o ranking.
        
        Considera:
        - Prioridade base (URGENTE=100, ALTA=70, MÉDIA=40, BAIXA=10)
        - Penalização para papers lidos ou em revisão
        - Bônus para papers recém-criados
        - Penalização para papers recomendados recentemente
        """
        score = paper.priority_score
        
        # Penalizar papers já lidos ou em revisão
        if paper.status == Paper.STATUS_LIDO:
            score += cls.PENALTY_LIDO
        elif paper.status == Paper.STATUS_REVISANDO:
            score += cls.PENALTY_REVISANDO
        
        # Bônus para papers novos
        dias_desde_criacao = (timezone.now() - paper.created_at).days
        if dias_desde_criacao <= cls.BONUS_NOVO_PAPER_DAYS:
            score += cls.BONUS_NOVO_PAPER
        
        # Penalizar papers recomendados recentemente (rodízio)
        try:
            ranking_entry = paper.ranking_entry
            if ranking_entry.last_recommended_at:
                dias_desde_recomendacao = (timezone.now() - ranking_entry.last_recommended_at).days
                if dias_desde_recomendacao <= cls.PENALTY_RECENTE_DIAS:
                    score += cls.PENALTY_RECENTE
        except RankingEntry.DoesNotExist:
            pass
        
        # Penalizar papers com última sessão de leitura muito recente
        last_session = paper.reading_sessions.first()
        if last_session:
            dias_desde_leitura = (timezone.now().date() - last_session.date).days
            if dias_desde_leitura <= cls.PENALTY_RECENTE_DIAS:
                score += cls.PENALTY_RECENTE
        
        return max(score, 0)
    
    @classmethod
    def update_ranking(cls, user, limit=None):
        """
        Atualiza o ranking de todos os papers do usuário.
        Retorna queryset ordenado por score.
        """
        papers = Paper.objects.filter(owner=user)
        
        if limit:
            papers = papers[:limit]
        
        for paper in papers:
            score = cls.calculate_score(paper)
            RankingEntry.objects.update_or_create(
                paper=paper,
                defaults={'score': score}
            )
        
        return cls.get_ranked_papers(user, limit)
    
    @classmethod
    def get_ranked_papers(cls, user, limit=None):
        """
        Retorna papers ordenados por ranking sem atualizar scores.
        Calcula score dinamicamente.
        """
        papers = Paper.objects.filter(owner=user).prefetch_related(
            'authors', 'tags', 'reading_sessions', 'notes'
        )
        
        # Calcular scores dinamicamente e ordenar
        papers_with_scores = []
        for paper in papers:
            score = cls.calculate_score(paper)
            papers_with_scores.append((paper, score))
        
        # Ordenar por score (descendente) e depois por created_at (descendente)
        papers_with_scores.sort(key=lambda x: (-x[1], x[0].created_at), reverse=False)
        papers_with_scores.sort(key=lambda x: x[1], reverse=True)
        
        ranked_papers = [p[0] for p in papers_with_scores]
        
        if limit:
            return ranked_papers[:limit]
        
        return ranked_papers
    
    @classmethod
    def mark_as_recommended(cls, paper):
        """Marca um paper como recomendado (atualiza timestamp)"""
        entry, _ = RankingEntry.objects.get_or_create(
            paper=paper,
            defaults={'score': cls.calculate_score(paper)}
        )
        entry.last_recommended_at = timezone.now()
        entry.save()
    
    @classmethod
    def get_next_to_read(cls, user, count=5):
        """
        Retorna os próximos N papers recomendados para leitura.
        Marca os papers retornados como recomendados.
        """
        ranked = cls.get_ranked_papers(user, limit=count)
        
        # Marcar como recomendados
        for paper in ranked:
            cls.mark_as_recommended(paper)
        
        return ranked
