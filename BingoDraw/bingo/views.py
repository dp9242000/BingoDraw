from django.views import generic
from django.utils import timezone

from .models import Card


class IndexView(generic.ListView):
    template_name = 'bingo/index.html'
    context_object_name = 'bingo_index'
    paginate_by = 5

    def get_queryset(self):
        """Return the questions previously posted (no future dates) and order by date desc."""
        return Card.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Card
    template_name = 'bingo/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Card.objects.filter(pub_date__lte=timezone.now())
