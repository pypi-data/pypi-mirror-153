from slugify import slugify


def to_slug(text, max_length):
    return slugify(text, max_length=max_length)
