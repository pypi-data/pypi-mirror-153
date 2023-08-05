from django import template
from django.http import QueryDict
from django.urls import reverse
from django.utils.http import urlencode

from obpages.templatetags.constants import OBPAGES_COMPONENTS_PATH

register = template.Library()

OBPAGES_WIDGETS_PATH = f"{OBPAGES_COMPONENTS_PATH}/widgets"


@register.inclusion_tag(f"{OBPAGES_WIDGETS_PATH}/move_sequencemember.html")
def move_sequencemember_arrows(sequence, user, order):
    return {"sequence": sequence, "user": user, "order": order}


@register.inclusion_tag(f"{OBPAGES_WIDGETS_PATH}/delete_sequencemember.html")
def delete_sequencemember_widget(sequence, user, order):
    return {"sequence": sequence, "user": user, "order": order}


@register.inclusion_tag(f"{OBPAGES_WIDGETS_PATH}/pagination_bar.html")
def pagination_bar(paginator, page_obj, query=None):
    page_range = paginator.get_elided_page_range(page_obj.number)
    if query is None:
        query = QueryDict()
    return {
        "paginator": paginator,
        "page_obj": page_obj,
        "page_range": page_range,
        "query": query,
    }


@register.inclusion_tag(f"{OBPAGES_WIDGETS_PATH}/author_list.html")
def author_list(authors):
    return {"authors": authors}


@register.inclusion_tag(f"{OBPAGES_WIDGETS_PATH}/item_count.html")
def classifier_count(item):
    item_count = item.content.count()
    search_key = f"{item._meta.verbose_name}s"
    search_value = item.slug
    search_url = f"{reverse('search')}?{urlencode({search_key: search_value})}"
    return {"item_count": item_count, "search_url": search_url}
