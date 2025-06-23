from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.admin.views.reports import ReportView
from wagtail.admin.ui.tables import Column
from django.urls import path, reverse
from django.utils.html import format_html

from .models import Event


class EventReportView(ReportView):
    index_url_name = "event_report"
    index_results_url_name = "event_report_results"
    page_title = "Events Report"
    header_icon = "date"

    def get_queryset(self):
        return Event.objects.live().order_by("start_date")

    def get_filename(self):
        return "events-report"

    columns = [
        Column(
            "title",
            label="Title",
            sort_key="title",
            accessor=lambda obj: format_html(
                '<a href="{}">{}</a>',
                reverse("wagtailadmin_pages:edit", args=[obj.id]),
                obj.title,
            ),
        ),
        Column("date_range", label="Date", sort_key="start_date"),
        Column("location", label="Location", sort_key="location"),
        Column("newsletter_campaign", label="Newsletter"),
    ]

    list_export = [
        "title",
        "date_range",
        "location",
        "organiser",
        "newsletter_campaign",
    ]

    export_headings = {
        "title": "Event Title",
        "date_range": "Date",
        "location": "Location",
        "organiser": "Organiser",
        "newsletter_campaign": "Newsletter Campaign",
    }


@hooks.register("register_admin_urls")
def register_event_report_url():
    return [
        path("reports/events/", EventReportView.as_view(), name="event_report"),
        path(
            "reports/events/results/",
            EventReportView.as_view(results_only=True),
            name="event_report_results",
        ),
    ]


@hooks.register("register_admin_menu_item")
def register_event_report_menu_item():
    return MenuItem(
        "Events Report", reverse("event_report"), icon_name="date", order=800
    )
