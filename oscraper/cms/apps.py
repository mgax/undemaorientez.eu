from django.apps import AppConfig


class CMSConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "oscraper.cms"
    label = "cms"
    verbose_name = "CMS"
