import datetime

from haystack import indexes
from obapi.models import OBContentItem, SpotifyContentItem, YoutubeContentItem

INDEX_TEMPLATES_PATH = "obpages/indexes"


class DurationField(indexes.IntegerField):
    """Field which represents durations as integer numbers of seconds."""

    def convert(self, value):
        if value is None:
            return None

        if isinstance(value, datetime.timedelta):
            return int(value.total_seconds())

        return int(value)


class ContentItemIndex(indexes.SearchIndex):
    text = indexes.CharField(
        document=True,
        use_template=True,
        template_name=f"{INDEX_TEMPLATES_PATH}/contentitem_text.txt",
    )
    title = indexes.CharField(model_attr="title")
    publish_date = indexes.DateTimeField(
        model_attr="publish_date", stored=True, indexed=False
    )
    authors = indexes.MultiValueField(stored=True, indexed=False)
    ideas = indexes.MultiValueField(stored=True, indexed=False)
    topics = indexes.MultiValueField(stored=True, indexed=False)

    def prepare_authors(self, obj):
        return self.prepare_many_to_many(obj, field="authors")

    def prepare_ideas(self, obj):
        return self.prepare_many_to_many(obj, field="ideas")

    def prepare_topics(self, obj):
        return self.prepare_many_to_many(obj, field="topics")

    def prepare_many_to_many(self, obj, field):
        return [item.slug for item in getattr(obj, field).all()]


class OBContentItemIndex(ContentItemIndex, indexes.Indexable):

    word_count = indexes.IntegerField(
        model_attr="word_count", stored=True, indexed=False
    )

    def get_model(self):
        return OBContentItem


class SpotifyContentItemIndex(ContentItemIndex, indexes.Indexable):

    duration = DurationField(model_attr="duration", stored=True, indexed=False)

    def get_model(self):
        return SpotifyContentItem


class YoutubeContentItemIndex(ContentItemIndex, indexes.Indexable):

    duration = DurationField(model_attr="duration", stored=True, indexed=False)

    def get_model(self):
        return YoutubeContentItem
