from django.urls.converters import StringConverter
from obapi.converters import (
    OB_POST_NAME_REGEX,
    SPOTIFY_EPISODE_ID_REGEX,
    YOUTUBE_VIDEO_ID_REGEX,
)


class ClassifierNameConverter(StringConverter):
    regex = r"(author|idea|topic|tag)s"

    def to_python(self, value):
        return value.removesuffix("s")

    def to_url(self, value):
        return f"{value}s"


class YoutubeVideoIDConverter(StringConverter):
    regex = YOUTUBE_VIDEO_ID_REGEX


class SpotifyEpisodeIDConverter(StringConverter):
    regex = SPOTIFY_EPISODE_ID_REGEX


class OBPostNameConverter(StringConverter):
    regex = OB_POST_NAME_REGEX
