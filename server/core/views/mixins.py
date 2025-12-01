from django.contrib.auth.mixins import LoginRequiredMixin


class OwnerRequiredMixin(LoginRequiredMixin):
    """Mixin para garantir que apenas o owner acessa o objeto"""
    
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)
