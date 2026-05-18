from django.core.paginator import Paginator

from .constants import PAGE_SIZE

def paginate(request, queryset, per_page=PAGE_SIZE):
    return Paginator(queryset, per_page).get_page(request.GET.get('page'))
