from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from obapi.modelfields import SimpleSlugField
from obapi.models import BaseSequence, BaseSequenceMember, ContentItem

from obpages.utils import to_slug

USER_SLUG_MAX_LENGTH = 150


class User(AbstractUser):
    slug = SimpleSlugField(
        max_length=USER_SLUG_MAX_LENGTH,
        unique=True,
        editable=False,
    )

    def clean(self):
        # Set slug from username
        self.slug = to_slug(self.username, max_length=USER_SLUG_MAX_LENGTH)
        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"user_slug": self.slug})

    def __str__(self):
        return self.username


class SearchIndex(models.Model):
    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            ("update_search_index", "Can update the search index"),
            ("rebuild_search_index", "Can rebuild the search index"),
        )
        verbose_name_plural = "Search Indexes"


class UserSequence(BaseSequence):
    items = models.ManyToManyField(ContentItem, through="UserSequenceMember")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
        related_name="sequences",
    )
    public = models.BooleanField(
        default=False, help_text="Whether the sequence is public or private."
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "slug"], name="unique_usersequence_slug"
            )
        ]


class UserSequenceMember(BaseSequenceMember):
    sequence = models.ForeignKey(
        UserSequence,
        on_delete=models.CASCADE,
        related_name="members",
        related_query_name="members",
    )
    content_item = models.ForeignKey(
        ContentItem,
        on_delete=models.CASCADE,
        related_name="user_sequence_members",
        related_query_name="user_sequence_members",
    )
