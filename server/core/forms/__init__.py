"""
Forms do SRPIA

Estrutura modularizada por domínio:
- paper.py: PaperForm
- note.py: NoteForm
- reading_session.py: ReadingSessionForm
- experiment.py: ExperimentForm
- tag.py: TagForm
- paper_search.py: PaperSearchForm
"""

from .paper import PaperForm
from .note import NoteForm
from .reading_session import ReadingSessionForm
from .experiment import ExperimentForm
from .tag import TagForm
from .paper_search import PaperSearchForm

__all__ = [
    'PaperForm',
    'NoteForm',
    'ReadingSessionForm',
    'ExperimentForm',
    'TagForm',
    'PaperSearchForm',
]
