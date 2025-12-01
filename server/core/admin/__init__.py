"""
Admin configuration do SRPIA

Estrutura modularizada por domínio:
- author.py: Admin de Author
- tag.py: Admin de Tag
- paper.py: Admin de Paper
- experiment.py: Admin de Experiment
- note.py: Admin de Note
- reading_session.py: Admin de ReadingSession
- ranking.py: Admin de RankingEntry
"""

# Importar todos os admins para registrá-los
from .author import AuthorAdmin
from .tag import TagAdmin
from .paper import PaperAdmin
from .experiment import ExperimentAdmin
from .note import NoteAdmin
from .reading_session import ReadingSessionAdmin
from .ranking import RankingEntryAdmin

__all__ = [
    'AuthorAdmin',
    'TagAdmin',
    'PaperAdmin',
    'ExperimentAdmin',
    'NoteAdmin',
    'ReadingSessionAdmin',
    'RankingEntryAdmin',
]
