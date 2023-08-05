from django import template

from obpages.templatetags.constants import OBPAGES_COMPONENTS_PATH

OBPAGES_TILES_PATH = f"{OBPAGES_COMPONENTS_PATH}/tiles"

register = template.Library()


@register.inclusion_tag(f"{OBPAGES_TILES_PATH}/tile_content.html")
def content_tile(item):
    return {"item": item}


@register.inclusion_tag(f"{OBPAGES_TILES_PATH}/tile_classifier.html")
def classifier_tile(item, detailed):
    return {"item": item, "detailed": detailed}


@register.inclusion_tag(f"{OBPAGES_TILES_PATH}/tile_sequence.html")
def sequence_tile(sequence, user):
    return {
        "sequence": sequence,
        "owner": sequence.owner,
        "user_is_owner": user == sequence.owner,
    }


@register.inclusion_tag(f"{OBPAGES_TILES_PATH}/tile_sequencemember.html")
def sequencemember_tile(sequence, item, order, user, editable=False):
    return {
        "sequence": sequence,
        "item": item,
        "order": order,
        "user": user,
        "editable": editable,
    }


@register.inclusion_tag(f"{OBPAGES_TILES_PATH}/tile_more.html")
def more_tile(url, more_count, verbose_name):
    return {"url": url, "more_count": more_count, "verbose_name": verbose_name}
