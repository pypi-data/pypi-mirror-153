from django import forms
from django.core.exceptions import ValidationError
from haystack.query import SQ, AutoQuery, SearchQuerySet
from obapi.formfields import PandocWriterField
from obapi.models import (
    Author,
    Idea,
    OBContentItem,
    SpotifyContentItem,
    Topic,
    YoutubeContentItem,
)

from obpages.fields import (
    ClassifierMultipleChoiceField,
    ContentMultipleChoiceField,
    SortOptionsField,
)
from obpages.models import UserSequence, UserSequenceMember


class DefaultSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label="Search",
        widget=forms.HiddenInput(),
    )

    sort = SortOptionsField(
        options={
            "relevance": ("Relevance", "-_score"),  # "_score" is ElasticSearch-specific
            "newest": ("Newest First", "-publish_date"),
            "oldest": ("Oldest First", "publish_date"),
        },
        required=False,
        label="Sort By",
        widget=forms.Select(attrs={"onchange": "this.form.submit()"}),
    )
    authors = ClassifierMultipleChoiceField(Author)
    ideas = ClassifierMultipleChoiceField(Idea)
    topics = ClassifierMultipleChoiceField(Topic)
    start_date = forms.DateTimeField(
        required=False,
        label="Start Date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    end_date = forms.DateTimeField(
        required=False,
        label="End Date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    content_type = ContentMultipleChoiceField(
        models=(SpotifyContentItem, YoutubeContentItem, OBContentItem),
        required=False,
        label="Content Type",
    )
    min_word_count = forms.IntegerField(
        label="Minimum Word Count", required=False, min_value=0, max_value=10000
    )
    max_word_count = forms.IntegerField(
        label="Maximum Word Count", required=False, min_value=0, max_value=10000
    )
    min_duration = forms.DurationField(label="Minimum Duration", required=False)
    max_duration = forms.DurationField(label="Maximum Duration", required=False)

    def __init__(self, *args, **kwargs):
        self.searchqueryset = kwargs.pop("searchqueryset", None)
        self.load_all = kwargs.pop("load_all", False)

        if self.searchqueryset is None:
            self.searchqueryset = SearchQuerySet()

        super().__init__(*args, **kwargs)

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        sqs = self.searchqueryset

        if query := self.cleaned_data.get("query"):
            sqs = sqs.filter(SQ(content=AutoQuery(query)) | SQ(title=AutoQuery(query)))

        if order_field := self.cleaned_data.get("sort"):
            sqs = sqs.order_by(order_field)

        if authors := self.cleaned_data.get("authors"):
            sqs = sqs.filter(authors__in=authors)

        if ideas := self.cleaned_data.get("ideas"):
            sqs = sqs.filter(ideas__in=ideas)

        if topics := self.cleaned_data.get("topics"):
            sqs = sqs.filter(topics__in=topics)

        if start_date := self.cleaned_data.get("start_date"):
            sqs = sqs.filter(publish_date__gte=start_date)

        if end_date := self.cleaned_data.get("end_date"):
            sqs = sqs.filter(publish_date__lte=end_date)

        if content_type := self.cleaned_data.get("content_type"):
            sqs = sqs.filter(django_ct__in=content_type)

        if min_word_count := self.cleaned_data.get("min_word_count"):
            sqs = sqs.filter(word_count__gte=min_word_count)

        if max_word_count := self.cleaned_data.get("max_word_count"):
            sqs = sqs.filter(word_count__lte=max_word_count)

        if min_duration := self.cleaned_data.get("min_duration"):
            sqs = sqs.filter(duration__gte=min_duration.total_seconds())

        if max_duration := self.cleaned_data.get("max_duration"):
            sqs = sqs.filter(duration__lte=max_duration.total_seconds())

        if self.load_all:
            sqs = sqs.load_all()

        return sqs

    def no_query_found(self):
        return self.searchqueryset.all()

    def clean(self):
        cleaned_data = super().clean()

        # Date range
        self.validate_range(
            cleaned_data,
            "start_date",
            "end_date",
            message="End date must be after start date.",
        )
        self.validate_range(
            cleaned_data,
            "min_word_count",
            "max_word_count",
            message="Minimum word count must be less than maximum word count.",
        )
        self.validate_range(
            cleaned_data,
            "min_duration",
            "max_duration",
            message="Minimum duration must be less than maximum duration.",
        )

        return cleaned_data

    def validate_range(self, cleaned_data, lower_field, upper_field, message=None):
        """Ensure the value of one field is more than another."""
        lower = cleaned_data.get(lower_field)
        upper = cleaned_data.get(upper_field)
        if lower and upper and lower > upper:
            if message is None:
                message = f"{lower_field} must be less than {upper_field}."
            raise ValidationError(
                message,
                code="invalid",
            )


class ExportSequenceForm(forms.Form):
    writer = PandocWriterField(label="Export To", initial="epub")


class SequenceChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["abstract"].widget.attrs.pop("cols")

    class Meta:
        model = UserSequence
        fields = ("title", "abstract", "public")

    def _get_validation_exclusions(self):
        exclude = super()._get_validation_exclusions()
        exclude.remove("owner")
        exclude.remove("slug")
        return exclude


class SequenceMemberMoveForm(forms.Form):
    SEQUENCEMEMBER_MOVE_CHOICES = [
        ("top", "Top"),
        ("up", "Up"),
        ("down", "Down"),
        ("bottom", "Bottom"),
    ]

    move = forms.ChoiceField(choices=SEQUENCEMEMBER_MOVE_CHOICES)


class UserSequenceMemberAddForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["sequence"].queryset = user.sequences.all()

    class Meta:
        model = UserSequenceMember
        fields = ("sequence",)
