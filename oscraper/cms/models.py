from django.db import models
from django.utils import timezone
from django.utils.formats import date_format
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail_newsletter.models import NewsletterPageMixin


class HomePage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        "intro",
    ]

    def get_future_events(self):
        today = timezone.now().date()
        return (
            self.get_children()
            .live()
            .type(Event)
            .filter(event__end_date__gte=today)
            .order_by("event__start_date")
            .specific()
        )


class Event(NewsletterPageMixin, Page):
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

    @property
    def date_range(self):
        if self.start_date == self.end_date:
            return date_format(self.start_date)
        return f"{date_format(self.start_date)} - {date_format(self.end_date)}"

    newsletter_template = "cms/event_newsletter_email.html"
