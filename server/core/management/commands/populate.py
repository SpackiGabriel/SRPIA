from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from core.models import Paper, Author, Tag, Note, ReadingSession, Experiment
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de demonstração para o SRPIA'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='demo',
            help='Nome de usuário para criar (padrão: demo)'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='demo123456',
            help='Senha para o usuário (padrão: demo123456)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Limpar dados existentes do usuário antes de popular'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        clear_data = options['clear']

        self.stdout.write(self.style.SUCCESS('='*70))
        self.stdout.write(self.style.SUCCESS(' SRPIA - Popular Banco de Dados'))
        self.stdout.write(self.style.SUCCESS('='*70))
        self.stdout.write('')

        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': f'{username}@example.com'}
        )
        
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Usuário "{username}" criado'))
        else:
            if clear_data:
                Paper.objects.filter(owner=user).delete()
                Tag.objects.filter(owner=user).delete()
                Experiment.objects.filter(owner=user).delete()
                self.stdout.write(self.style.WARNING(f'✓ Dados anteriores do usuário "{username}" removidos'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ Usuário "{username}" já existe (use --clear para limpar dados)'))

        self.stdout.write('')
        self.stdout.write('Criando autores...')
        authors_data = [
            {"name": "Yoshua Bengio", "affiliation": "Université de Montréal"},
            {"name": "Geoffrey Hinton", "affiliation": "University of Toronto"},
            {"name": "Yann LeCun", "affiliation": "New York University"},
            {"name": "Andrew Ng", "affiliation": "Stanford University"},
            {"name": "Ian Goodfellow", "affiliation": "Google Brain"},
            {"name": "Demis Hassabis", "affiliation": "DeepMind"},
            {"name": "Fei-Fei Li", "affiliation": "Stanford University"},
        ]

        authors = []
        for author_data in authors_data:
            author, created = Author.objects.get_or_create(**author_data)
            authors.append(author)
            if created:
                self.stdout.write(f'  ✓ {author.name}')

        self.stdout.write('')
        self.stdout.write('Criando tags...')
        tags_data = [
            "Deep Learning",
            "Visão Computacional",
            "Processamento de Linguagem Natural",
            "Aprendizado por Reforço",
            "GANs",
            "Transformers",
            "CNN",
            "Mecanismos de Atenção",
            "Transfer Learning",
        ]

        tags = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name, owner=user)
            tags.append(tag)
            if created:
                self.stdout.write(f'  ✓ {tag_name}')

        self.stdout.write('')
        self.stdout.write('Criando papers...')
        papers_data = [
            {
                "title": "Atenção é Tudo que Você Precisa",
                "abstract": "Os modelos dominantes de transdução de sequências são baseados em redes neurais recorrentes ou convolucionais complexas que incluem um codificador e um decodificador. Os modelos de melhor desempenho também conectam o codificador e o decodificador através de um mecanismo de atenção. Propomos uma nova arquitetura de rede simples, o Transformer, baseada apenas em mecanismos de atenção, dispensando completamente recorrência e convoluções.",
                "year": 2017,
                "venue": "NeurIPS 2017",
                "doi": "10.48550/arXiv.1706.03762",
                "total_pages": 15,
                "priority": Paper.Priority.URGENTE,
                "status": Paper.Status.NAO_INICIADO,
                "author_indices": [0, 1],
                "tag_indices": [5, 2, 7],
            },
            {
                "title": "Aprendizado Residual Profundo para Reconhecimento de Imagens",
                "abstract": "Redes neurais mais profundas são mais difíceis de treinar. Apresentamos um framework de aprendizado residual para facilitar o treinamento de redes substancialmente mais profundas do que as usadas anteriormente. Reformulamos explicitamente as camadas como funções residuais de aprendizado com referência às entradas da camada, em vez de aprender funções não referenciadas.",
                "year": 2016,
                "venue": "CVPR 2016",
                "doi": "10.1109/CVPR.2016.90",
                "total_pages": 12,
                "priority": Paper.Priority.ALTA,
                "status": Paper.Status.EM_LEITURA,
                "author_indices": [2, 6],
                "tag_indices": [0, 1, 6],
            },
            {
                "title": "Redes Adversariais Generativas",
                "abstract": "Propomos um novo framework para estimar modelos generativos através de um processo adversarial, no qual treinamos simultaneamente dois modelos: um modelo generativo G que captura a distribuição dos dados, e um modelo discriminativo D que estima a probabilidade de uma amostra ter vindo dos dados de treinamento em vez de G.",
                "year": 2014,
                "venue": "NeurIPS 2014",
                "doi": "10.48550/arXiv.1406.2661",
                "total_pages": 9,
                "priority": Paper.Priority.ALTA,
                "status": Paper.Status.LIDO,
                "author_indices": [4],
                "tag_indices": [0, 4],
            },
            {
                "title": "BERT: Pré-treinamento de Transformers Bidirecionais Profundos para Compreensão de Linguagem",
                "abstract": "Introduzimos um novo modelo de representação de linguagem chamado BERT, que significa Bidirectional Encoder Representations from Transformers. Diferente de modelos recentes de representação de linguagem, o BERT é projetado para pré-treinar representações bidirecionais profundas a partir de texto não rotulado, condicionando conjuntamente tanto o contexto à esquerda quanto à direita em todas as camadas.",
                "year": 2019,
                "venue": "NAACL 2019",
                "doi": "10.18653/v1/N19-1423",
                "total_pages": 16,
                "priority": Paper.PRIORITY_URGENTE,
                "status": Paper.STATUS_EM_LEITURA,
                "author_indices": [0, 1],
                "tag_indices": [2, 5, 8],
            },
            {
                "title": "Jogando Atari com Aprendizado por Reforço Profundo",
                "abstract": "Apresentamos o primeiro modelo de deep learning a aprender com sucesso políticas de controle diretamente de entrada sensorial de alta dimensão usando aprendizado por reforço. O modelo é uma rede neural convolucional, treinada com uma variante de Q-learning, cuja entrada são pixels brutos e cuja saída é uma função de valor que estima recompensas futuras.",
                "year": 2013,
                "venue": "NeurIPS 2013 Workshop",
                "doi": "10.48550/arXiv.1312.5602",
                "total_pages": 9,
                "priority": Paper.Priority.MEDIA,
                "status": Paper.Status.NAO_INICIADO,
                "author_indices": [3, 5],
                "tag_indices": [0, 3],
            },
            {
                "title": "Classificação ImageNet com Redes Neurais Convolucionais Profundas",
                "abstract": "Treinamos uma grande rede neural convolucional profunda para classificar 1,2 milhão de imagens de alta resolução do concurso ImageNet LSVRC-2010 em 1000 classes diferentes. Nos dados de teste, alcançamos taxas de erro top-1 e top-5 de 37,5% e 17,0%, consideravelmente melhor que o estado da arte anterior.",
                "year": 2012,
                "venue": "NeurIPS 2012",
                "doi": "10.1145/3065386",
                "total_pages": 9,
                "priority": Paper.Priority.MEDIA,
                "status": Paper.Status.LIDO,
                "author_indices": [1, 2],
                "tag_indices": [0, 1, 6],
            },
            {
                "title": "Dominando o Jogo de Go com Redes Neurais Profundas e Busca em Árvore",
                "abstract": "O jogo de Go há muito tempo é visto como o mais desafiador dos jogos clássicos para inteligência artificial devido ao seu enorme espaço de busca e à dificuldade de avaliar posições e movimentos no tabuleiro. Aqui apresentamos uma nova abordagem para Go computacional que usa 'redes de valor' para avaliar posições do tabuleiro e 'redes de política' para selecionar movimentos.",
                "year": 2016,
                "venue": "Nature",
                "doi": "10.1038/nature16961",
                "total_pages": 7,
                "priority": Paper.Priority.BAIXA,
                "status": Paper.Status.NAO_INICIADO,
                "author_indices": [5],
                "tag_indices": [3, 0],
            },
        ]

        papers = []
        for paper_data in papers_data:
            author_indices = paper_data.pop('author_indices')
            tag_indices = paper_data.pop('tag_indices')
            
            paper, created = Paper.objects.get_or_create(
                title=paper_data['title'],
                owner=user,
                defaults=paper_data
            )
            
            if created:
                for idx in author_indices:
                    paper.authors.add(authors[idx])
                
                for idx in tag_indices:
                    paper.tags.add(tags[idx])
                
                self.stdout.write(f'  ✓ {paper.title[:60]}...')
            
            papers.append(paper)

        self.stdout.write('')
        self.stdout.write('Criando notas...')
        notes_data = [
            {
                "paper": papers[1],
                "title": "Arquitetura ResNet - Conexões Residuais",
                "content": "A inovação principal é o uso de conexões residuais (skip connections) que permitem treinar redes muito mais profundas. Isso resolve o problema de degradação que ocorre em redes profundas convencionais. As conexões residuais facilitam o fluxo do gradiente durante o backpropagation.",
                "note_type": Note.TYPE_INSIGHT,
            },
            {
                "paper": papers[1],
                "title": "Aplicação em Transfer Learning",
                "content": "ResNet pré-treinada no ImageNet serve como excelente feature extractor para outras tarefas de visão computacional.",
                "note_type": Note.TYPE_INSIGHT,
            },
            {
                "paper": papers[2],
                "title": "Aplicações Práticas de GANs",
                "content": "GANs podem ser usadas para: geração de imagens realistas, super-resolução, transferência de estilo, data augmentation, geração de dados sintéticos para treinamento.",
                "note_type": Note.TYPE_INSIGHT,
            },
            {
                "paper": papers[2],
                "title": "Dificuldade de Treinamento",
                "content": "O treinamento de GANs é notoriamente instável. Mode collapse e vanishing gradients são problemas comuns. Requer muito tuning de hiperparâmetros.",
                "note_type": Note.TYPE_CRITICA,
            },
            {
                "paper": papers[3],
                "title": "Dúvida sobre Fine-tuning",
                "content": "Como determinar a melhor taxa de aprendizado para fine-tuning em tarefas específicas? Preciso investigar estratégias de learning rate scheduling.",
                "note_type": Note.TYPE_DUVIDA,
            },
            {
                "paper": papers[3],
                "title": "Citação Importante",
                "content": "\"BERT obtains new state-of-the-art results on eleven natural language processing tasks\" - isso demonstra a versatilidade do modelo.",
                "note_type": Note.TYPE_CITACAO,
            },
        ]

        for note_data in notes_data:
            note, created = Note.objects.get_or_create(**note_data)
            if created:
                self.stdout.write(f'  ✓ {note.title}')

        self.stdout.write('')
        self.stdout.write('Criando sessões de leitura...')
        sessions_data = [
            {
                "paper": papers[1],
                "date": date.today() - timedelta(days=5),
                "duration_minutes": 90,
                "pages_read": 4,
                "quick_notes": "Li a introdução e método. Arquitetura interessante com skip connections.",
            },
            {
                "paper": papers[1],
                "date": date.today() - timedelta(days=3),
                "duration_minutes": 60,
                "pages_read": 3,
                "quick_notes": "Resultados experimentais impressionantes no ImageNet. Rede de 152 camadas!",
            },
            {
                "paper": papers[1],
                "date": date.today() - timedelta(days=1),
                "duration_minutes": 75,
                "pages_read": 5,
                "quick_notes": "Análise dos experimentos de ablation. As conexões residuais são fundamentais.",
            },
            {
                "paper": papers[3],
                "date": date.today() - timedelta(days=2),
                "duration_minutes": 120,
                "pages_read": 8,
                "quick_notes": "Estudei o processo de pré-treinamento do BERT com MLM e NSP.",
            },
            {
                "paper": papers[3],
                "date": date.today(),
                "duration_minutes": 90,
                "pages_read": 6,
                "quick_notes": "Fine-tuning em tarefas downstream. Resultados impressionantes com minimal task-specific architecture.",
            },
            {
                "paper": papers[5],
                "date": date.today() - timedelta(days=7),
                "duration_minutes": 45,
                "pages_read": 9,
                "quick_notes": "AlexNet foi revolucionário. ReLU e dropout foram inovações importantes.",
            },
        ]

        for session_data in sessions_data:
            session, created = ReadingSession.objects.get_or_create(**session_data)
            if created:
                self.stdout.write(f'  ✓ Sessão para "{session.paper.title[:40]}..."')

        self.stdout.write('')
        self.stdout.write('Atualizando progresso dos papers...')
        for paper in papers:
            if paper.reading_sessions.exists():
                paper.update_progress()
                self.stdout.write(f'  ✓ {paper.title[:50]}... - {paper.progress_percent}%')

        self.stdout.write('')
        self.stdout.write('Criando experimentos...')
        experiments_data = [
            {
                "title": "Classificação de Imagens CIFAR-10 com ResNet",
                "description": "Experimento para classificar imagens do dataset CIFAR-10 usando ResNet-50 pré-treinada no ImageNet. Objetivo: alcançar acurácia superior a 90%.",
                "status": Experiment.STATUS_CONCLUIDO,
                "dataset_description": "CIFAR-10: 60.000 imagens coloridas 32x32 em 10 classes (50.000 para treino, 10.000 para teste)",
                "main_results": "Acurácia final de 92,3% após 100 épocas. Taxa de aprendizado: 0,001 com decaimento. Aumento de dados aplicado (inversão horizontal, recorte aleatório).",
                "code_repository_url": "https://github.com/demo/resnet-cifar10",
                "paper_indices": [1],
            },
            {
                "title": "Geração de Faces com GAN",
                "description": "Implementação de DCGAN para geração de faces humanas realistas usando o dataset CelebA.",
                "status": Experiment.STATUS_EM_EXECUCAO,
                "dataset_description": "CelebA: mais de 200 mil imagens de celebridades, redimensionadas para 64x64 pixels",
                "main_results": "Após 50 épocas, as faces geradas começam a ter características realistas, mas ainda há problemas com colapso de modo (mode collapse) em alguns casos.",
                "code_repository_url": "https://github.com/demo/dcgan-faces",
                "paper_indices": [2],
            },
            {
                "title": "Análise de Sentimento com BERT Fine-tuning",
                "description": "Ajuste fino (fine-tuning) do BERT para análise de sentimento em avaliações de filmes do dataset IMDb.",
                "status": Experiment.STATUS_PLANEJADO,
                "dataset_description": "IMDb: 50 mil avaliações de filmes (25 mil positivas, 25 mil negativas)",
                "main_results": "Esperamos alcançar F1-score superior a 0,90",
                "code_repository_url": "https://github.com/demo/bert-sentiment",
                "paper_indices": [3],
            },
        ]

        for exp_data in experiments_data:
            paper_indices = exp_data.pop('paper_indices')
            
            experiment, created = Experiment.objects.get_or_create(
                title=exp_data['title'],
                owner=user,
                defaults=exp_data
            )
            
            if created:
                for idx in paper_indices:
                    experiment.papers.add(papers[idx])
                
                self.stdout.write(f'  ✓ {experiment.title}')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('='*70))
        self.stdout.write(self.style.SUCCESS(' Dados criados com sucesso!'))
        self.stdout.write(self.style.SUCCESS('='*70))
        self.stdout.write('')
        
        self.stdout.write(self.style.WARNING('Credenciais de acesso:'))
        self.stdout.write(f'  Usuário: {username}')
        self.stdout.write(f'  Senha: {password}')
        self.stdout.write('')
        
        self.stdout.write(self.style.WARNING('Estatísticas:'))
        self.stdout.write(f'  Papers: {Paper.objects.filter(owner=user).count()}')
        self.stdout.write(f'  Autores: {len(authors)}')
        self.stdout.write(f'  Tags: {Tag.objects.filter(owner=user).count()}')
        self.stdout.write(f'  Notas: {Note.objects.filter(paper__owner=user).count()}')
        self.stdout.write(f'  Sessões de Leitura: {ReadingSession.objects.filter(paper__owner=user).count()}')
        self.stdout.write(f'  Experimentos: {Experiment.objects.filter(owner=user).count()}')
        self.stdout.write('')
