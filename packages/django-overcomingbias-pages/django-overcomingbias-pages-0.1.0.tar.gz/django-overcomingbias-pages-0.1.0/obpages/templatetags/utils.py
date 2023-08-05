from django import template
from obapi.models import Author, BaseSequence, ContentItem, Idea, Tag, Topic

register = template.Library()


@register.filter
def cat(value, extra):
    return f"{value}{extra}"


@register.filter
def is_content(value):
    return isinstance(value, ContentItem)


@register.filter
def is_classifier(value):
    return isinstance(value, (Author, Idea, Topic, Tag))


@register.filter
def is_sequence(value):
    return isinstance(value, BaseSequence)


@register.filter
def verbose_name_plural(item):
    return item._meta.verbose_name_plural


@register.simple_tag
def last_mention(item):
    most_recent_item = item.content.recent().first()
    if most_recent_item is None:
        return None

    return most_recent_item.publish_date


@register.simple_tag()
def query_transform(query, **kwargs):
    """Return URL-encoded querystring for current page, updated using kwarg params."""
    new_query = query.copy()
    for k, v in kwargs.items():
        new_query[k] = v
    return new_query.urlencode()
