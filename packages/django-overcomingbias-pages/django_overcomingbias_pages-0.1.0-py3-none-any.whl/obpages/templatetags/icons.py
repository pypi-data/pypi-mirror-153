from django import template

register = template.Library()


@register.filter
def icon(item):
    """Get icon path corresponding to an item."""
    return f"obpages/icons/{type(item).__name__.lower()}.svg"
