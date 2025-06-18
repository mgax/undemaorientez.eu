from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        "intro",
    ]


class Event(Page):
    organiser = models.CharField(max_length=1000)
    location = models.CharField(max_length=1000, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    original_text = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        "organiser",
        "location",
        "start_date",
        "end_date",
        FieldPanel("original_text", read_only=True),
    ]
