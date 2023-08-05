import datetime

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from obapi.models import (
    SEQUENCE_SLUG_MAX_LENGTH,
    AudioContentItem,
    TextContentItem,
    VideoContentItem,
)

from obpages.models import User, UserSequence
from obpages.utils import to_slug


@pytest.fixture
def james():
    return User.objects.create_user("James", "james@example.com", "jamespassword")


@pytest.fixture
def alice():
    return User.objects.create_user("Alice", "alice@example.com", "alicepassword")


@pytest.mark.django_db
class TestCreateUserSequence:
    def test_can_create_empty_sequence(self, james):
        # Arrange
        seq_title = "Empty UserSequence"
        # Act
        james.sequences.create(title=seq_title, abstract="Description")
        # Assert
        seq = james.sequences.get(title=seq_title)
        assert seq.slug == to_slug(seq_title, SEQUENCE_SLUG_MAX_LENGTH)
        assert not seq.items.all().exists()

        # Act - modify title
        new_title = "New Title"
        seq.title = new_title
        seq.save()
        assert seq.slug == to_slug(new_title, SEQUENCE_SLUG_MAX_LENGTH)

    def test_can_create_normal_sequence(self, james, alice):
        # Arrange
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        video = VideoContentItem.objects.create(title="Video Item", publish_date=now)
        audio = AudioContentItem.objects.create(title="Audio Item", publish_date=now)
        text = TextContentItem.objects.create(title="Text Item", publish_date=now)
        seq_title = "Example UserSequence"

        # Act - create basic sequence
        seq = james.sequences.create(title=seq_title)
        seq.items.add(video, audio, text)

        # Assert
        seq = UserSequence.objects.get(title=seq_title)
        assert seq.title == seq_title
        assert seq.items.count() == 3

        # Act - change user
        seq.owner = alice
        seq.save()

        # Assert
        seq = UserSequence.objects.get(title=seq_title)
        assert seq.owner.username == "Alice"

        # Act - delete the user
        alice.delete()
        del alice

        # Assert
        assert not UserSequence.objects.filter(title=seq_title).exists()


@pytest.mark.django_db
class TestSlugUniquenessIsEnforced:
    def test_different_users_can_use_same_slug(self, james, alice):
        # Act and assert - create sequences
        james_seq = james.sequences.create(title="Fake UserSequence")
        try:
            alice_seq = alice.sequences.create(title="Fake UserSequence")
        except IntegrityError:
            pytest.fail("IntegrityError raised when creating fake sequence.")

        assert james_seq.slug == alice_seq.slug
        try:
            alice_seq.full_clean()
        except ValidationError:
            pytest.fail("ValidationError raised when validating fake sequence.")

    def test_duplicate_slug_does_not_save(self, james):
        # Act & Assert - sequence with owner
        james.sequences.create(title="Example UserSequence")
        with pytest.raises(IntegrityError):
            james.sequences.create(title="example-UserSequence")

    def test_duplicate_slug_does_not_validate(self, james):
        # Act & Assert
        james.sequences.create(title="Example UserSequence")
        seq2 = UserSequence(title="example-usersequence", owner=james)
        with pytest.raises(ValidationError):
            seq2.full_clean()
