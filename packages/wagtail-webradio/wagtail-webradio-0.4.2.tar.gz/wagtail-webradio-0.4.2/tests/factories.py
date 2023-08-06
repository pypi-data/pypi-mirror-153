from wagtail.images.tests.utils import Image, get_test_image_file

import factory
from factory.django import DjangoModelFactory
from taggit.models import Tag

from wagtail_webradio import models


class CleanModelFactory(DjangoModelFactory):
    """
    Ensures that created instances pass Django's `full_clean` checks.
    """

    class Meta:
        abstract = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        obj = model_class(*args, **kwargs)
        obj.full_clean()
        obj.save()
        return obj


class RadioShowFactory(CleanModelFactory):
    title = factory.Sequence(lambda n: "Radio Show #%d" % (n + 1))
    description = "<p>This is the radio show description.</p>"
    contact_phone = factory.Faker('phone_number', locale='fr_FR')
    contact_email = factory.Faker('email')

    class Meta:
        model = models.RadioShow


class PodcastFactory(CleanModelFactory):
    title = factory.Sequence(lambda n: "Podcast #%d" % (n + 1))
    description = "<p>This is the podcast description.</p>"
    sound_url = factory.Faker('uri')
    radio_show = factory.SubFactory(RadioShowFactory)

    class Meta:
        model = models.Podcast


class TagFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: "Tag #%d" % (n + 1))

    class Meta:
        model = Tag


class TaggedPodcastFactory(DjangoModelFactory):
    content_object = factory.SubFactory(PodcastFactory)
    tag = factory.SubFactory(TagFactory)

    class Meta:
        model = models.TaggedPodcast


class ImageFactory(DjangoModelFactory):
    title = "Image title"
    file = get_test_image_file()

    class Meta:
        model = Image
