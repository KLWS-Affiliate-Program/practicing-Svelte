from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SystemConfig


@receiver(post_save, sender=SystemConfig)
def invalidate_system_config_cache(sender, **kwargs):
    """Invalidate cache when system config changes."""
    from django.core.cache import cache

    cache.delete("system_config")
