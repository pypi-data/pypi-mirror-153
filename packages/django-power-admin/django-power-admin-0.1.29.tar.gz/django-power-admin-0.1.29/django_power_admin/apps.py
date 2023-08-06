
import logging

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django.conf import settings

logger = logging.getLogger(__name__)

class DjangoPowerAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_power_admin'
    verbose_name = _("Django Power Admin")

    def ready(self):
        from django.contrib.admin import ModelAdmin
        if not getattr(ModelAdmin, "_list_filter_extra_media_enabled", False):
            self.enable_list_filter_extra_media()
    
    def enable_list_filter_extra_media(self):
        from django.contrib.admin import ModelAdmin
        from django import forms
        from django_middleware_global_request.middleware import get_request

        filter_specs_cache_key = "django_power_admin_cached_filter_specs"
        changelist_instance_cache_key = "django_power_admin_cached_changelist_instance"

        ModelAdmin._django_power_admin_old_media = ModelAdmin.media
        ModelAdmin._django_power_admin_old_get_changelist_instance = ModelAdmin.get_changelist_instance

        def get_changelist_instance(self, request):
            if hasattr(request, changelist_instance_cache_key):
                return getattr(request, changelist_instance_cache_key)
            result = self._django_power_admin_old_get_changelist_instance(request)
            setattr(request, changelist_instance_cache_key, result)
            # get the changelist's filter_specs and cache it into request instance
            try:
                get_filters_result = result.get_filters(request)
                if get_filters_result:
                    filter_specs = get_filters_result[0]
                else:
                    logger.error("django_power_admin.enable_list_filter_extra_media.get_changelist_instance.get_filters got NONE filters")
                    filter_specs = []
            except Exception as error:
                logger.exception("django_power_admin.enable_list_filter_extra_media.get_changelist_instance.get_filters failed: {error}".format(error=error))
                filter_specs = []
            setattr(request, filter_specs_cache_key, filter_specs)

            return result
        
        @property
        def media(self):
            request = get_request()
            filter_specs = getattr(request, filter_specs_cache_key, None)
            result = self._django_power_admin_old_media
            if filter_specs:
                for spec in filter_specs:
                    media_class = getattr(spec, "Media", None)
                    if media_class:
                        result += forms.Media(media=media_class)
            return result
    
        ModelAdmin.get_changelist_instance = get_changelist_instance
        ModelAdmin.media = media
