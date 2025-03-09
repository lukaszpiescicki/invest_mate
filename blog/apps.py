from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_supervisors_group(sender, **kwargs) -> None:
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType

    from .models import Article

    supervisor_group, created = Group.objects.get_or_create(name="Supervisors")

    content_type = ContentType.objects.get_for_model(Article)
    article_permission = Permission.objects.filter(content_type=content_type)

    for perm in article_permission:
        supervisor_group.permissions.add(perm)


class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"

    def ready(self):
        post_migrate.connect(create_supervisors_group, sender=self)
